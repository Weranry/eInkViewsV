import sys
sys.dont_write_bytecode = True

from flask import Flask
import os
from modules.plugins.plugin_loader import register_plugins
from modules.errors.errors import register_error_handlers
from modules.register.random_view_route import bp_random
from modules.register.template_routes import bp_templates
from modules.evkey_auth import check_auth

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
public_dir = os.path.join(project_root, 'public')
app = Flask(__name__, template_folder=public_dir)
app.config['JSON_AS_ASCII'] = False
app.json.ensure_ascii = False
register_plugins(app)
register_error_handlers(app)
app.register_blueprint(bp_random)
app.register_blueprint(bp_templates)
app.before_request(check_auth)

@app.after_request
def set_charset(response):
    if response.mimetype == 'application/json':
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

if __name__ == '__main__':
    app.run()

