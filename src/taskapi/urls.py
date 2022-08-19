from rest_framework.routers import SimpleRouter

from src.taskapi.views import TaskViewSet


tasks_router = SimpleRouter()
tasks_router.register(r'tasks', TaskViewSet)
