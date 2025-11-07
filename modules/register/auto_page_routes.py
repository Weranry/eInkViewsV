import os
from flask import send_from_directory

def register_page_routes(bp, plugin_name, page_dir):
    if not os.path.exists(page_dir):
        return
    for fname in os.listdir(page_dir):
        if fname.endswith('.html'):
            page_name = fname[:-5]
            def make_page_func(page_name=page_name, page_dir=page_dir, filename=fname):
                def page_func():
                    return send_from_directory(page_dir, filename)
                page_func.__name__ = f'page_{plugin_name}_{page_name}'
                return page_func
            bp.add_url_rule(f'/{plugin_name}/page/{page_name}', view_func=make_page_func())
