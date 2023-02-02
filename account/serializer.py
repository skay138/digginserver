from rest_framework import serializers
from account.models import User, Follow

class UserSerializer(serializers.ModelSerializer):

    class Meta :
        model = User
        fields = ['uid','email','nickname','introduce','image', 'gender', 'birth', 'is_signed','is_active']

class SwaggerDeleteSerializer(serializers.ModelSerializer):

    class Meta :
        model = User
        fields = ['uid']



class FollowerSerializer(serializers.ModelSerializer):
    def get_nickname(self, obj):
        return obj.follower.nickname

    def get_image(self, obj):
        return obj.follower.image.url
    
    nickname = serializers.SerializerMethodField('get_nickname')
    image = serializers.SerializerMethodField('get_image')

    class Meta :
        model = Follow
        fields = ['follower', 'nickname', 'image']

class FolloweeSerializer(serializers.ModelSerializer):
    def get_nickname(self, obj):
        return obj.followee.nickname

    def get_image(self, obj):
        return obj.followee.image.url

    nickname = serializers.SerializerMethodField('get_nickname')
    image = serializers.SerializerMethodField('get_image')

    class Meta :
        model = Follow
        fields = ['followee', 'nickname', 'image']


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = "__all__"