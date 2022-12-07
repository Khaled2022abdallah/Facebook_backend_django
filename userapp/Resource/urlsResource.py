from django.urls import path
from userapp.Resource import viewsResource

urlpatterns = [
    path("unknown", viewsResource.resource, name="resource"),
    path("unknown/create", viewsResource.create_resource, name="create_resource"),
    path("unknown/<str:pk>", viewsResource.checkResource, name="checkResource"),
    path("getResource", viewsResource.getResource, name="getResource"),
    path("like/<str:pk>", viewsResource.like, name="like"),
    path("comment/<str:pk>", viewsResource.comment, name="comment"),
    path("deleteComment", viewsResource.deleteComment, name="deleteComment"),
]
