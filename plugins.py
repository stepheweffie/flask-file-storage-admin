import os
from flask import render_template_string, current_app
import os.path as op

class Plugins:
    _plugins = None

    @classmethod
    def load_plugins(cls):
        if cls._plugins is None:
            cls._plugins = []
            plugins_dir = os.path.join(op.dirname(__file__), 'templates/plugins')
            for filename in os.listdir(plugins_dir):
                if filename.endswith('.html'):
                    plugin_name = os.path.splitext(filename)[0]
                    with open(os.path.join(plugins_dir, filename), 'r') as file:
                        content = file.read()
                    cls._plugins.append({
                        'name': plugin_name,
                        'content': content
                    })

    @classmethod
    def reload_plugins(cls):
        cls._plugins = None
        cls.load_plugins()

    @classmethod
    def render_plugins(cls):
        cls.load_plugins()  # Ensure plugins are loaded
        rendered_plugins = []
        for plugin in cls._plugins:  # Use cls._plugins instead of self.plugins
            rendered_content = render_template_string(
                plugin['content'],
                csrf_token = current_app.jinja_env.globals.get('csrf_token', lambda: '')

            )
            rendered_plugins.append({
                'name': plugin['name'],
                'content': rendered_content
            })
        return rendered_plugins
