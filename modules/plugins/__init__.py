import importlib.util
import os
from functools import lru_cache

@lru_cache(maxsize=64)
def load_plugin_config(plugin_name, plugin_dir):
    normalized_dir = os.path.realpath(plugin_dir)
    config_path = os.path.join(normalized_dir, 'plugin_config.py')
    if not os.path.isfile(config_path):
        return {}
    spec = importlib.util.spec_from_file_location(f"{plugin_name}_plugin_config", config_path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as exc:
        # Vercel: 只 print，不抛出
        print(f"插件 {plugin_name} 的 plugin_config.py 加载失败: {exc}")
        return {}
    return {k: getattr(mod, k) for k in dir(mod) if not k.startswith('__')}
