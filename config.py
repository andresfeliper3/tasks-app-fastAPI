def create_configuration_fastapi(app, middleware):
    # Changes to the docs
    app.title = "My app with FastAPI"
    app.version = "1.0"
    app.add_middleware(middleware)