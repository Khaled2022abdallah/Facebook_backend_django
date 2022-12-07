import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from userapp.models import *


@csrf_exempt
def resource(request):
    if request.method == "POST":
        data = list(Resource.objects.all().values("id", "name", "year",
                                                  "color", "pantone_value", 'likes', 'comments', "user"))
        support = list(Resource.objects.all().values("urlSupport", "textSupport"))
        my_data = {"data": data, "support": support}
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
        user = Users.objects.get(id=user_id)
        resource = Resource(name=name, year=year, color=color, pantone_value=pantone_value,
                            urlSupport=urlSupport, textSupport=text, user=user)
        resource.save()
        my_data = {"data": resource.serialize(), "support": resource.serialize2()}
    return JsonResponse(my_data)


@csrf_exempt
def checkResource(request, pk):
    if request.method == "POST":
        if Resource.objects.filter(id=pk).exists():
            posts = Resource.objects.get(id=pk)
            my_data = {"data": posts.serialize(), "support": posts.serialize2()}
        else:
            my_data = {}
    return JsonResponse(my_data)


@csrf_exempt
def getResource(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_id = data["user_id"]
        user = Users.objects.get(id=user_id)
        if Resource.objects.filter(user=user).exists():
            posts = list(
                Resource.objects.filter(user=user).values("id", "name", "year", "color", "pantone_value", "user"))
            support = list(Resource.objects.filter(user_id=user_id).values("urlSupport", "textSupport"))
            my_data = {"data": posts, "support": support}
        else:
            my_data = {}
        return JsonResponse(my_data)


@csrf_exempt
def like(request, pk):
    if request.method == "POST":
        data = json.loads(request.body)
        my_id = data['my_id']
        id_post = data["id_post"]
        status = data["status"]
        if Friends1.objects.filter(id=pk).exists():
            myUser = Users.objects.get(id=my_id)
            post = Resource.objects.get(id=id_post)
            if Like.objects.filter(user=myUser, resource=post).exists():
                likePost = Like.objects.get(user=myUser, resource=post)
                like_post = likePost.likes - 1
                likePost.likes = like_post
                likePost.delete()
                like = post.countLikes - 1
                post.countLikes = like
                post.save()
                my_data = {"message": "you unliked this post"}
            else:
                new_like, created = Like.objects.create(user=myUser, resource=post)
                like_post = new_like.likes + 1
                new_like.likes = like_post
                new_like.save()
                like = post.countLikes + 1
                post.countLikes = like
                post.save()
                my_data = {"message": f"your liked {post.name}"}
        else:
            my_data = {"message": "your not friends"}

    return JsonResponse(my_data)


@csrf_exempt
def comment(request, pk):
    if request.method == "POST":
        data = json.loads(request.body)
        my_id = data['my_id']
        id_post = data["id_post"]
        comment = data["comment"]
        id_comment = data["id_comment"]
        if Friends1.objects.filter(id=pk).exists():
            myUser = Users.objects.get(id=my_id)
            post = Resource.objects.get(id=id_post)
            new_comment = Comment.objects.create(id=id_comment, user=myUser, resource=post)
            comment_post = new_comment.comment + comment
            new_comment.comment = comment_post
            new_comment.save()
            count_comment = post.comments + 1
            post.comments = count_comment
            post.save()
            my_data = {"message": "Thanks for comment"}
        else:
            my_data = {"message": "your not friends"}
    return JsonResponse(my_data)


@csrf_exempt
def deleteComment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        id_post = data["id_post"]
        id_comment = data["id_comment"]
        if Comment.objects.filter(id=id_comment).exists():
            post = Resource.objects.get(id=id_post)
            coment = Comment.objects.get(id=id_comment)
            coment.delete()
            count_comment = post.comments - 1
            post.comments = count_comment
            post.save()
            my_data = {"Message": "you delete your comment"}
        else:
            my_data = {"Message": "no comment for you"}
    return JsonResponse(my_data)
