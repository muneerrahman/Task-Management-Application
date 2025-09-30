from rest_framework import serializers
from .models import User, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)  

    class Meta:
        model = Task
        fields = [
            'id','title','description','assigned_to','due_date','status','completion_report','worked_hours'
        ]
        read_only_fields = ['status', 'completion_report', 'worked_hours']


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status', 'completion_report', 'worked_hours']

    def validate(self, data):
        if data.get('status') == 'completed':
            if not data.get('completion_report'):
                raise serializers.ValidationError("Completion report is required when marking as completed.")
            if not data.get('worked_hours'):
                raise serializers.ValidationError("Worked hours are required when marking as completed.")
        return data
