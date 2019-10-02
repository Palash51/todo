from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from filemanager.models import User, ToDoList, Item


class SignupSerializer(serializers.ModelSerializer):
    """
    signup serializer will validate user input
    unique email and mobile no and return specific message
    """
    class Meta:
        model = User
        fields = ('email',)

    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all(), message="Email already exists")
        ])


    @property
    def sg_errors(self):
        messages = ""
        for error in self.errors:
            messages += self.errors[error][0]
            messages += "\n"

        return messages


class UserSerializer(serializers.ModelSerializer):
    """user serializer"""

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name")


class ItemsSerializer(serializers.ModelSerializer):
    """items serializer"""

    class Meta:
        model = Item
        fields = ("name", "task", "mark_done")


class ToDoListSerializer(serializers.ModelSerializer):
    """to do serializer"""

    items = serializers.SerializerMethodField()
    tags = serializers.ListField(child=serializers.CharField())

    class Meta:
        model =ToDoList
        fields = ("id", "title", "items", "tags")


    def get_items(self, obj):
        """get all the items of to do list"""
        result = Item.objects.filter(todolist=obj).values('name', 'task', 'mark_done')
        return result
