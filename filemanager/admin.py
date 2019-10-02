from django.contrib import admin

from filemanager.models import User, ToDoList, Item

admin.site.register(User)
admin.site.register(ToDoList)
admin.site.register(Item)