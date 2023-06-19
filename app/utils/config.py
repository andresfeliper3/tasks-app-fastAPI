from routers.task import task_router
from routers.user import user_router
from routers.category import category_router

def create_configuration_fastapi(app, middleware):
    # Changes to the docs
    app.title = "My app with FastAPI"
    app.version = "1.0"
    app.add_middleware(middleware)
    app.include_router(user_router)
    app.include_router(task_router)
    app.include_router(category_router)
