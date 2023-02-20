from rest_framework import serializers
from account.models import User, Follow
from post.models import Post


class UserSerializer(serializers.ModelSerializer):

    def getTotalPost(self, obj):
        uid = obj.uid
        totalPost = Post.objects.filter(author_id = uid).count()
        return totalPost

    def getFollower(self, obj):
        uid = obj.uid
        follwer = Follow.objects.filter(followee = uid).count()
        return follwer

    def getFollowee(self, obj):
        uid = obj.uid
        followee = Follow.objects.filter(follower = uid).count()
        return followee


    
    totalPost = serializers.SerializerMethodField('getTotalPost')
    follower = serializers.SerializerMethodField('getFollower')
    followee = serializers.SerializerMethodField('getFollowee')



    class Meta :
        model = User
        fields = ['uid','email','nickname','introduce','image', 'bgimage', 'totalPost', 'follower', 'followee', 'gender', 'birth', 'is_signed','is_active']

class SwaggerDeleteSerializer(serializers.ModelSerializer):

    class Meta :
        model = User
        fields = ['uid']



class FollowCountSerializer(serializers.ModelSerializer):
    def getFollowerFollower(self, obj):
        user = obj.follower
        follwer = Follow.objects.filter(followee = user).count()
        
        return follwer
    
    def getFollowerFollowee(self, obj):
        user = obj.follower
        followee = Follow.objects.filter(follower = user).count()
        return followee


    def getFolloweeFollower(self, obj):
        user = obj.followee
        follower = Follow.objects.filter(followee = user).count()
        
        return follower
    
    def getFolloweeFollowee(self, obj):
        user = obj.followee
        followee = Follow.objects.filter(follower = user).count()

        return followee
    
    follower_follower = serializers.SerializerMethodField('getFollowerFollower')
    follower_followee = serializers.SerializerMethodField('getFollowerFollowee')
    followee_follower = serializers.SerializerMethodField('getFolloweeFollower')
    followee_followee = serializers.SerializerMethodField('getFolloweeFollowee')

    class Meta:
        model = Follow
        fields = ['follower_follower', 'follower_followee','followee_follower','followee_followee']


class FollowCountDelSerializer(serializers.ModelSerializer):
    def getFollowerFollower(self, obj):
        user = obj.follower
        follwer = Follow.objects.filter(followee = user).count()
        
        return follwer
    
    def getFollowerFollowee(self, obj):
        user = obj.follower
        followee = Follow.objects.filter(follower = user).count()
        return followee


    def getFolloweeFollower(self, obj):
        user = obj.followee
        follower = Follow.objects.filter(followee = user).count()
        
        return follower
    
    def getFolloweeFollowee(self, obj):
        user = obj.followee
        followee = Follow.objects.filter(follower = user).count()

        return followee
    
    follower_follower = serializers.SerializerMethodField('getFollowerFollower')
    follower_followee = serializers.SerializerMethodField('getFollowerFollowee')
    followee_follower = serializers.SerializerMethodField('getFolloweeFollower')
    followee_followee = serializers.SerializerMethodField('getFolloweeFollowee')

    class Meta:
        model = Follow
        fields = ['follower_follower', 'follower_followee','followee_follower','followee_followee']




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