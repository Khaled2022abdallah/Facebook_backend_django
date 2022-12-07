from django.urls import path
from userapp.Users import viewsUser

urlpatterns = [
    path('users/', viewsUser.index, name=" index"),
    path("users/<str:pk>", viewsUser.checkUsers, name="checkUsers"),
    path("login", viewsUser.login, name="login"),
    path("register", viewsUser.register, name="register"),
    path("getUser", viewsUser.getUser, name="getuser"),
    path("create", viewsUser.create_user, name="create_user"),
    path("update", viewsUser.update, name="update"),
    path("delete", viewsUser.delete, name="delete"),
    path("add_friend", viewsUser.add_friend, name="add_friend"),
]
