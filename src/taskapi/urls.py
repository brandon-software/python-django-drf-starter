from rest_framework.routers import SimpleRouter

from src.taskapi.views import TaskViewSet, TaskFilterAPIView


tasks_router = SimpleRouter()
tasks_router.register(r'tasks/filter', TaskFilterAPIView, basename='tasks/filter')
tasks_router.register(r'tasks', TaskViewSet)
