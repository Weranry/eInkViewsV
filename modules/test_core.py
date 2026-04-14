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
    
    register_plugins(app)
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

    return app

def print_help():
    print("\n 可用命令:")
    print("  help    - 显示此帮助信息")
    print("  routes  - 列出所有详细路由及其参数")
    print("  exit    - 退出程序")

def print_routes(app):
    print("\n" + "="*30 + " 详细路由列表 " + "="*30)
    rules = sorted(list(app.url_map.iter_rules()), key=lambda x: str(x))
    for rule in rules:
        if "static" in rule.endpoint: 
            continue
        methods = ','.join(sorted(rule.methods - {'OPTIONS', 'HEAD'}))
        print(f"[{methods}] {str(rule)}")
        if rule.arguments:
            print(f"      ↳ 参数: {', '.join(rule.arguments)}")
    print("="*74 + "\n")

def console_listener(app):
    while True:
        try:
            cmd = input(">>> ").strip().lower()
            if cmd == 'help':
                print_help()
            elif cmd == 'routes':
                print_routes(app)
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

        plugins_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'plugins')
        plugin_names = []
        if os.path.exists(plugins_dir):
            plugin_names = [
                name for name in os.listdir(plugins_dir)
                if os.path.isdir(os.path.join(plugins_dir, name)) and os.path.exists(os.path.join(plugins_dir, name, 'routes.py'))
            ]
        
        print(f"发现可用插件 {len(plugin_names)} 个: {', '.join(plugin_names) if plugin_names else '无'}")
        
        total_start = time.time()
        try:
            app = create_app()
        except Exception as e:
            print(f"致命错误: Flask 应用初始化失败 - {e}")
            sys.exit(1)
            
        total_elapsed = time.time() - total_start
        print(f"装载耗时: {total_elapsed:.3f}s")
        print(f"注意: 仅供本地测试使用。输入 'help' 获取指令。")
        print("访问地址: http://127.0.0.1:5000")

        t = threading.Thread(target=console_listener, args=(app,), daemon=True)
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
