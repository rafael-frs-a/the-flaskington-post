from importlib import import_module


def load_config(app):
    app.config.from_object('tfp.ext.config.config_values.Config')
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True


def load_extensions(app):
    for extension in app.config['EXTENSIONS']:
        mod = import_module(extension)
        mod.init_app(app)
