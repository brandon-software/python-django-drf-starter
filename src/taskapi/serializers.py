from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'created_by', 'title', 'content', 'created_on', 'due_date')
        read_only_fields = (
            'id',
            'created_by',
            'created_on',
        )


class CreateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'content',
            'created_on',
            'due_date',
        )

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user

        return super().create(validated_data)
