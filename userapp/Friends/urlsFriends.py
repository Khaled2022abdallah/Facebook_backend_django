from django.urls import path
from userapp.Friends import viewsFreinds

urlpatterns = [

    path('sendRequest', viewsFreinds.sendRequest),
    path('delete_request', viewsFreinds.delete_request),
    path('add_or_remove_friend', viewsFreinds.add_or_remove_friend),
    path('resourceUser/<str:pk>', viewsFreinds.getresource),
]
