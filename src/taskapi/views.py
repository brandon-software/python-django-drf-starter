from .models import Task
from .serializers import TaskSerializer, CreateTaskSerializer
from django.shortcuts import get_object_or_404, render

from rest_framework import generics
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from src.taskapi.models import Task

from rest_framework.permissions import IsAuthenticated
from .permissions import IsCreator


class TaskFilterAPIView(generics.ListAPIView, viewsets.GenericViewSet):
    """
    Returns a list of filtered Tasks.
    NOTE: This view intentionally allows anonymous access to all tasks.
    """

    serializer_class = TaskSerializer
    permissions = {'default': (AllowAny,)}  # change to IsAuthenticated to limit to users
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'due_date']

    def get_permissions(self):
        self.permission_classes = self.permissions.get(self.action, self.permissions['default'])
        return super().get_permissions()

    def get_queryset(self):
        """
        Returns a list of filtered Tasks
        """
        queryset = Task.objects.all()
        title = self.request.query_params.get('title')
        if title is not None:
            queryset = queryset.filter(title=title)
        datedue = self.request.query_params.get('due_date')
        if datedue is not None:
            queryset = queryset.filter(due_date=datedue)
        return queryset


class TaskViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Returns a single Task.  Allows creation, retrieval, update and deletion of an authenticated user's Task.
    NOTE: Retrieve/all tasks allows access to any users's task.
    """

    queryset = Task.objects.all()
    serializers = {'default': TaskSerializer, 'create': CreateTaskSerializer}
    permission_classes_by_action = {'retrieve': (IsAuthenticated,), 'update': (IsCreator,), 'partial_update': (IsCreator,)}

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        """
        Returns a list of all Tasks by authenticated user.
        Note: Reports 404 for actions on non-owned tasks
        """
        user = self.request.user
        return Task.objects.filter(created_by=user)

    @action(detail=False, methods=['get'], url_path='alltasks', url_name='alltasks')
    def alltasks(self, request):
        """
        This view should return a list of all Tasks/all Users for authenticated users.
        """
        queryset = Task.objects.all()
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        This view should return a single Task from all users for authenticated users.
        """
        queryset = Task.objects.all()
        task = get_object_or_404(queryset, pk=pk)
        serializer = TaskSerializer(task, many=False)
        return Response(serializer.data)
