import sys
import os
import datetime
import logging
import time
import threading
from flask import Flask, request

def startup_banner():
    print(
        "===================================================================\n"
        "███████╗██╗███╗   ██╗██╗  ██╗██╗   ██╗██╗███████╗██╗    ██╗███████╗\n"
        "██╔════╝██║████╗  ██║██║ ██╔╝██║   ██║██║██╔════╝██║    ██║██╔════╝\n"
        "█████╗  ██║██╔██╗ ██║█████╔╝ ██║   ██║██║█████╗  ██║ █╗ ██║███████╗\n"
        "██╔══╝  ██║██║╚██╗██║██╔═██╗ ╚██╗ ██╔╝██║██╔══╝  ██║███╗██║╚════██║\n"
        "███████╗██║██║ ╚████║██║  ██╗ ╚████╔╝ ██║███████╗╚███╔███╔╝███████║\n"
        "╚══════╝╚═╝╚═╝  ╚════╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝ ╚══╝╚══╝ ╚══════╝\n"
        "====================================================================="
    )

def create_app():
    from modules.plugins.plugin_loader import register_plugins
    from modules.errors.errors import register_error_handlers, ParamError
    from modules.register.random_view_route import bp_random
    from modules.register.template_routes import bp_templates

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    public_dir = os.path.join(project_root, 'public')
    
    app = Flask(__name__, template_folder=public_dir)
    app.config['JSON_AS_ASCII'] = False
    app.json.ensure_ascii = False
    
    plugin_result = register_plugins(app)
    register_error_handlers(app)
    app.register_blueprint(bp_random)
    app.register_blueprint(bp_templates)

    @app.errorhandler(ParamError)
    def handle_test_param_error(e):
        app.logger.error(f" [ParamError] 在请求 {request.path} 时发生: {str(e)}")
        return {"success": False, "message": str(e), "code": 400}, 400

    @app.after_request
    def set_charset(response):
        if response.mimetype == 'application/json':
            response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

    return app, plugin_result

def print_help():
    print("\n 可用命令:")
    print("  help     - 显示此帮助信息")
    print("  routes   - 列出所有详细路由及其参数")
    print("  plugins  - 列出所有插件及其描述")
    print("  config   - 显示当前配置参数")
    print("  auth     - 显示鉴权状态与白名单")
    print("  exit     - 退出程序")

def print_routes(app):
    print("\n详细路由列表:")
    rules = sorted(list(app.url_map.iter_rules()), key=lambda x: str(x))
    for rule in rules:
        if "static" in rule.endpoint: 
            continue
        methods = ','.join(sorted(rule.methods - {'OPTIONS', 'HEAD'}))
        print(f"  [{methods}] {str(rule)}")
        if rule.arguments:
            print(f"    ↳ 参数: {', '.join(rule.arguments)}")

def print_plugins(plugin_result):
    plugins = plugin_result.get('plugins', [])
    if not plugins:
        print("\n无已加载插件")
        return
    print(f"已加载插件:")
    for p in plugins:
        print(f"{p['name']}|{p['description']}")

def print_config():
    from config import (
        DEFAULT_ROTATE, DEFAULT_INVERT,
        DEFAULT_JPEG_QUALITY, DEFAULT_WEBP_QUALITY,
        DEFAULT_PNG_COMPRESS_LEVEL, DEFAULT_TIFF_COMPRESSION,
        DEFAULT_IMAGE_FORMAT, DEFAULT_TIMEZONE_OFFSET
    )
    print("参数配置:")
    print(f"  DEFAULT_ROTATE             = {DEFAULT_ROTATE}")
    print(f"  DEFAULT_INVERT             = {DEFAULT_INVERT}")
    print(f"  DEFAULT_JPEG_QUALITY       = {DEFAULT_JPEG_QUALITY}")
    print(f"  DEFAULT_WEBP_QUALITY       = {DEFAULT_WEBP_QUALITY}")
    print(f"  DEFAULT_PNG_COMPRESS_LEVEL = {DEFAULT_PNG_COMPRESS_LEVEL}")
    print(f"  DEFAULT_TIFF_COMPRESSION   = {DEFAULT_TIFF_COMPRESSION}")
    print(f"  DEFAULT_IMAGE_FORMAT       = {DEFAULT_IMAGE_FORMAT}")
    print(f"  DEFAULT_TIMEZONE_OFFSET    = {DEFAULT_TIMEZONE_OFFSET}")

def print_auth():
    from config import AUTH_ENABLE, AUTH_WHITELIST
    import os as _os
    env_key = _os.environ.get('EVKEY')
    print("\n鉴权状态:")
    status = "已启用" if AUTH_ENABLE else "未启用"
    print(f"  鉴权: {status}")
    if AUTH_ENABLE:
        print(f"  EVKEY 环境变量: {'已设置' if env_key else '未设置'}")
    print(f"  白名单路径:")
    for path in AUTH_WHITELIST:
        print(f"    - {path}")

def console_listener(app, plugin_result):
    while True:
        try:
            cmd = input(">>> ").strip().lower()
            if cmd == 'help':
                print_help()
            elif cmd == 'routes':
                print_routes(app)
            elif cmd == 'plugins':
                print_plugins(plugin_result)
            elif cmd == 'config':
                print_config()
            elif cmd == 'auth':
                print_auth()
            elif cmd == 'exit':
                print("正在退出...")
                os._exit(0)
            elif cmd == '':
                continue
            else:
                print(f"未知命令: '{cmd}', 输入 'help' 查看可用命令.")
        except EOFError:
            break

def run_test_server():
    try:
        startup_banner()
        EINKVIEWS_START_TIME = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
        print(f"启动时间: {EINKVIEWS_START_TIME}")

        startup_start = time.time()
        try:
            app, plugin_result = create_app()
        except Exception as e:
            print(f"致命错误: Flask 应用初始化失败 - {e}")
            sys.exit(1)
        startup_elapsed = time.time() - startup_start

        total = plugin_result.get('total', 0)
        success = plugin_result.get('success', 0)
        failed = plugin_result.get('failed', 0)
        print(f"发现插件 {total} 个，加载成功 {success} 个，失败 {failed} 个")

        from config import AUTH_ENABLE
        auth_status = "已启用" if AUTH_ENABLE else "未启用"
        print(f"鉴权状态: {auth_status}")
        print(f"启动耗时: {startup_elapsed:.3f}s")
        print("版本: 26.9.1")
        print("访问地址: http://127.0.0.1:5000")
        print(f"注意: 仅供本地测试使用。输入 'help' 获取指令。")

        t = threading.Thread(target=console_listener, args=(app, plugin_result), daemon=True)
        t.start()

        if (cli := sys.modules.get('flask.cli')):
            cli.show_server_banner = lambda *x: None

        class AccessLogFilter(logging.Filter):
            def filter(self, record):
                return any(m in record.getMessage() for m in ["GET", "POST", "PUT", "DELETE"])

        logging.getLogger('werkzeug').setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.addFilter(AccessLogFilter())
        logging.getLogger('werkzeug').handlers = [handler]

        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n正在通过手动中断退出...")
        sys.exit(0)
    except Exception as e:
        print(f"服务器运行出错: {e}")
        sys.exit(1)