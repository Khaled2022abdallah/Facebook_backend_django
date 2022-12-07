from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from datetime import datetime


class Users(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=1000)
    first_name = models.CharField(max_length=1000)
    last_name = models.CharField(max_length=1000)
    avatar = models.URLField()
    job = models.CharField(max_length=1000)
    date_created = models.DateTimeField(default=datetime.now, blank=True)
    urlSupport = models.URLField()
    textSupport = models.TextField()
    token = models.UUIDField()

    def __str__(self):
        return self.first_name

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "avatar": self.avatar,
        }

    def serialize2(self):
        return {
            "url": self.urlSupport,
            "text": self.textSupport,
        }

    def serializePOST(self):
        return {
            "name": self.first_name,
            "job": self.job,
            "id": self.id,
            "createdAt": self.date_created,
        }

    def serializePUT(self):
        return {
            "name": self.first_name,
            "job": self.job,
            "createdAt": self.date_created,
        }


class Groups(models.Model):
    name = models.CharField(max_length=128)
    leader = models.ManyToManyField(Users, related_name='leader')
    members = models.ManyToManyField(Users, through='Membership')

    def __str__(self):
        return self.name


class Membership(models.Model):
    person = models.ForeignKey(Users, on_delete=models.CASCADE)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Group: {self.group.name}, new_member: {self.person.first_name}"


class GroupRequest(models.Model):
    sender = models.ForeignKey(Users, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Groups, on_delete=models.CASCADE)

    def __str__(self):
        return f"Sender : {self.sender.first_name} , Receiver: {self.receiver.name}"


class Resource(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    color = models.CharField(max_length=100)
    pantone_value = models.CharField(max_length=100)
    urlSupport = models.URLField()
    textSupport = models.TextField()
    user = models.ManyToManyField(Users)
    comments = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    countLikes = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "year": self.year,
            "color": self.color,
            "pantone_value": self.pantone_value,
        }

    def serialize2(self):
        return {
            "url": self.urlSupport,
            "text": self.textSupport,
        }


class Friends1(models.Model):
    users1 = models.ManyToManyField(Users)
    current_user = models.ForeignKey(Users, related_name='owner', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Receiver: {self.current_user},"

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, create = cls.objects.get_or_create(current_user=current_user)
        friend.users1.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, create = cls.objects.get_or_create(current_user=current_user)
        friend.users1.remove(new_friend)


class FriendRequest(models.Model):
    sender = models.ForeignKey(Users, default="1", related_name='sender1', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Users, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Sender : {self.sender.first_name} , Receiver: {self.receiver.first_name}"


class Like(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, null=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"user:{self.user.first_name} like {self.resource.name}  "


class Comment(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, null=True)
    comment = models.TextField(max_length=1000)

    def __str__(self):
        return f"user:{self.user.first_name} comment {self.resource.name}  "
