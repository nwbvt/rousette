from rousette import api, env

def create_app(config=None):
    app = api.app
    if config:
        app.config.from_object(config)
    else:
        app.config.from_envvar("ROUSETTE_ENV")
    env.create_queue(app.config)
    
    return app