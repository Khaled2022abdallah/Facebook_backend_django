import json

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from userapp.models import *


@csrf_exempt
def sendRequest(request):
    if request.method == "POST":
        data = json.loads(request.body)
        my_id = data['my_id']
        id_recive = data['id_recive']
        if Users.objects.filter(id=id_recive).exists():
            sender = Users.objects.get(id=my_id)
            recipient = Users.objects.get(id=id_recive)
            model = Friends1.objects.create(current_user=recipient, status=1)
            model.users1.add(sender)
            model.save()
            my_data = {"message": "send successful"}
        else:
            my_data = {"error": "The user is not found"}
    return JsonResponse(my_data)


@csrf_exempt
def delete_request(request):
    if request.method == "POST":
        data = json.loads(request.body)
        id_sender = data['id_sender']
        id_recive = data['id_recive']
        operation = data["operation"]
        if Users.objects.filter(id=id_recive).exists():
            sender = Users.objects.get(id=id_sender)
            recipient = Users.objects.get(id=id_recive)
            if operation == 'Sender_deleting':
                model1 = FriendRequest.objects.get(sender=sender, receiver=recipient)
                model1.delete()
                my_data = {"message": "Sender is deleting"}
            elif operation == 'Receiver_deleting':
                model2 = FriendRequest.objects.get(sender=id_sender, receivers=id_recive)
                model2.delete()
                my_data = {"message": "Receiver is deleting"}
        else:
            my_data = {"message": "This user is not found"}
    return JsonResponse(my_data)


@csrf_exempt
def add_or_remove_friend(request):
    if request.method == "POST":
        data = json.loads(request.body)
        id_sender = data['id_sender']
        my_id = data['my_id']
        operation = data["operation"]
        if Users.objects.filter(id=id_sender).exists():
            myUser = Users.objects.get(id=my_id)
            new_friend = Users.objects.get(id=id_sender)
            if operation == 'add':
                fq = FriendRequest.objects.get(sender=new_friend, receiver=myUser)
                Friends1.make_friend(myUser, new_friend)
                Friends1.make_friend(new_friend, myUser)
                fq.delete()
                my_data = {"message": f"you add {new_friend} "}
            elif operation == 'remove':
                Friends1.lose_friend(myUser, new_friend)
                Friends1.lose_friend(new_friend, myUser)

                my_data = {"message": f"you remove {new_friend}"}

        return JsonResponse(my_data)


@csrf_exempt
def getresource(request, pk):
    if request.method == "POST":
        if Friends1.objects.filter(id=pk).exists():
            if Resource.objects.filter(id_user=pk).exists():
                data = list(Resource.objects.filter(id_user=pk).values("id", "name", "year", "color", "pantone_value"))
                support = list(Resource.objects.all().values("urlSupport", "textSupport"))
                my_data = {"data": data, "support": support}
            else:
                my_data = {}
        else:
            my_data = {"message": "this account is private!!"}
        return JsonResponse(my_data)
