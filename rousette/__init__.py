from rousette import api

def create_app(config=None):
    app = api.app
    if config:
        app.config.from_object(config)
    else:
        app.config.from_envvar("ROUSETTE_ENV")
    
    return app