import json
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from userapp.models import *


@csrf_exempt
def index(request):
    if request.method == "POST":
        data = list(Users.objects.all().values("id", "email", "first_name", "last_name", "avatar"))
        support = list(Users.objects.all().values("urlSupport", "textSupport"))
        my_data = {"data": data, "support": support}
    return JsonResponse(my_data)


@csrf_exempt
def checkUsers(request, pk):
    if request.method == "POST":
        if Users.objects.filter(id=pk).exists():
            posts = Users.objects.get(id=pk)
            my_data = {"data": posts.serialize(), "support": posts.serialize2()}
        else:
            my_data = {}
    return JsonResponse(my_data)


@csrf_exempt
def create_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data['name']
        job = data['job']
        user = Users(first_name=name, job=job)
        user.save()
        my_data = user.serializePUT()
    return JsonResponse(my_data)


@csrf_exempt
def update(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data['name']
        job = data['job']
        user = Users(first_name=name, job=job)
        user.save()
        my_data = user.serializePUT()
        return JsonResponse(my_data)


@csrf_exempt
def delete(request):
    if request.method == "POST":
        Users.objects.all().delete()
    my_data = {}
    return JsonResponse(my_data)


@csrf_exempt
def register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data['email']
        first_name = data['first_name']
        last_name = data['last_name']
        avatar = data['avatar']
        urlSupport = data['url']
        textSupport = data['text']
        username = data['username']
        password = data['password']
        if Users.objects.filter(email=email).exists():
            my_data = {"message": "This email is already exists"}
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            user = Users.objects.create(user=user, email=email, first_name=first_name, last_name=last_name,
                                        avatar=avatar,
                                        urlSupport=urlSupport,
                                        textSupport=textSupport, token=uuid.uuid4())
            user.save()
            my_data = {"id": user.id, "token": user.token}
    return JsonResponse(my_data)


@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_id = data["id"]
        token = data["token"]
        if Users.objects.filter(token=token).exists():
            if Resource.objects.filter(user_id=user_id).exists():
                posts = list(Resource.objects.filter(user_id=user_id).values("name", "year", "color",
                                                                             "pantone_value"))
                support = list(Resource.objects.filter(user_id=user_id).values("urlSupport", "textSupport"))

                my_data = {"data": posts, "support": support}
            else:
                my_data = {}
        else:
            my_data = {"error": "this token is invalid"}

    return JsonResponse(my_data)


@csrf_exempt
def getUser(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_id = data["user_id"]
        if Users.objects.filter(id=user_id).exists():
            posts = Users.objects.get(id=user_id)
            my_data = {"data": posts.serialize(), "support": posts.serialize2()}
        else:
            my_data = {}
        return JsonResponse(my_data)


@csrf_exempt
def add_friend(request):
    pass
    # if request.method == "POST":
    #     data = json.loads(request.body)
    #     user_id = data["user_id"]
    #     if Users.objects.filter(id=user_id).exists():
    #         Users.accept = True
    #         pass
    #     else:
    #         my_data = {"error": "this user is not found!!"}
    #
    # return JsonResponse(my_data)
