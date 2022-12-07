import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from userapp.models import *


@csrf_exempt
def createGroup(request, pk):
    if request.method == "POST":
        data = json.loads(request.body)
        name_group = data["name_group"]
        myUser = Users.objects.get(id=pk)
        group = Groups.objects.create(name=name_group)
        group.leader.add(myUser)
        group.save()
    return JsonResponse({"message": f"you create this group {group.name}"})


@csrf_exempt
def sendRequest(request):
    if request.method == "POST":
        data = json.loads(request.body)
        my_id = data['my_id']
        id_group = data['id_group']
        if Groups.objects.filter(id=id_group).exists():
            sender = Users.objects.get(id=my_id)
            recipient = Groups.objects.get(id=id_group)
            model = GroupRequest.objects.create(sender=sender, receiver=recipient)
            model.save()
            my_data = {"message": "send successful"}
        else:
            my_data = {"error": "The group is not found"}
    return JsonResponse(my_data)


@csrf_exempt
def delete_request(request, pk):
    if request.method == "POST":
        data = json.loads(request.body)
        id_sender = data['id_sender']
        id_group = data['id_group']
        if Groups.objects.filter(id=id_group).exists():
            leader = Users.objects.get(id=pk)
            sender = Users.objects.get(id=id_sender)
            recipient = Groups.objects.get(id=id_group, leader=leader)
            model1 = GroupRequest.objects.get(sender=sender, receiver=recipient)
            model1.delete()
            my_data = {"message": "your request is delete"}
        else:
            my_data = {"message": "This group is not found"}
    return JsonResponse(my_data)


@csrf_exempt
def add_or_remove_members(request, pk):
    if request.method == "POST":
        data = json.loads(request.body)
        id_sender = data['id_sender']
        id_group = data['id_group']
        operation = data["operation"]
        if Groups.objects.filter(id=id_group).exists():
            if Users.objects.filter(id=id_sender).exists():
                leader = Users.objects.get(id=pk)
                new_members = Users.objects.get(id=id_sender)
                group = Groups.objects.get(id=id_group, leader=leader)
                if operation == 'add':
                    fq = GroupRequest.objects.get(sender=new_members, receiver=group)
                    group.members.add(new_members)
                    fq.delete()
                    my_data = {"message": f"you add {new_members} "}
                elif operation == 'remove':
                    group.members.remove(new_members)
                    group.leader.remove(new_members)
                    my_data = {"message": f"you remove {new_members}"}
        return JsonResponse(my_data)


@csrf_exempt
def resourceGroup(request):
    if request.method == "POST":
        data = json.loads(request.body)
        my_id = data["my_id"]
        id_group = data["id_group"]
        user = Users.objects.get(id=my_id)
        group = Groups.objects.get(id=id_group)
        if Membership.objects.filter(person=user, group=group).exists():
            if Resource.objects.filter(group=group).exists():
                data = list(Resource.objects.filter(group=group).values("id", "name", "year",
                                                                        "color", "pantone_value", 'likes', 'comments',
                                                                        "group"))
                support = list(Resource.objects.filter(group=group).values("urlSupport", "textSupport"))
                my_data = {"data": data, "support": support}
            else:
                my_data = {}
        else:
            my_data = {"message": "you not member in the group"}
    return JsonResponse(my_data)


@csrf_exempt
def create_resource(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data['name']
        year = data['year']
        color = data['color']
        pantone_value = data['pantone_value']
        urlSupport = data['url']
        text = data['text']
        user_id = data['user_id']
        id_group = data["id_group"]
        if Groups.objects.filter(id=id_group).exists():
            user = Users.objects.get(id=user_id)
            group = Groups.objects.get(id=id_group)
            if Membership.objects.filter(group=group, person=user):
                resource = Resource(name=name, year=year, color=color, pantone_value=pantone_value,
                                    urlSupport=urlSupport, textSupport=text, user_id=user_id, group=group)
                resource.save()
                my_data = {"data": resource.serialize(), "support": resource.serialize2()}
        else:
            my_data = {"message": "the group is not found"}
    return JsonResponse(my_data)


@csrf_exempt
def addLeader(request, pk):
    if request.method == "POST":
        data = json.loads(request.body)
        id_member = data['id_member']
        id_group = data["id_group"]
        leader = Users.objects.get(id=pk)
        member = Users.objects.get(id=id_member)
        if Groups.objects.filter(id=id_group, leader=leader, members=member).exists():
            group = Groups.objects.get(id=id_group)
            group.leader.add(member)
            group.save()
            my_data = {"message": f"your add {member.first_name} group leader"}
        else:
            my_data = {"message": "this group is not found"}
        return JsonResponse(my_data)


@csrf_exempt
def exitLeader(request, pk):
    if request.method == "POST":
        data = json.loads(request.body)
        id_member = data["id_member"]
        id_group = data["id_group"]
        leader = Users.objects.get(id=pk)
        member = Users.objects.get(id=id_member)
        group = Groups.objects.get(id=id_group)
        if Groups.objects.filter(id=id_group, leader=leader).exists():
            if Groups.objects.filter(id=id_group, leader=member).exists():
                group.leader.remove(leader)
                group.save()
                message = {
                    "Message": f"The leader {leader.first_name} left,and the second leader is {member.first_name}"}
            else:
                group.leader.add(member)
                group.leader.remove(leader)
                group.save()
                message = {"Message": f"The leader {leader.first_name} left,and the new leader is {member.first_name}"}
        else:
            message = {"Message": " This group not found "}
        return JsonResponse(message)
