from django.urls import path

from userapp.Groups import viewsGroups

urlpatterns = [
    path('createGroup/<str:pk>', viewsGroups.createGroup),
    path('group/sendRequest', viewsGroups.sendRequest),
    path('group/delete_request/<str:pk>', viewsGroups.delete_request),
    path('group/add_or_remove_members/<str:pk>', viewsGroups.add_or_remove_members),
    path('group/resource', viewsGroups.resourceGroup),
    path('group/create_resource', viewsGroups.create_resource),
    path('group/addLeader/<str:pk>', viewsGroups.addLeader),
    path('group/exitLeader/<str:pk>', viewsGroups.exitLeader),
]
