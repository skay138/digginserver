from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _



class UserManager(BaseUserManager):
    def create_user(self, email, uid, nickname, password=None):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        """
        if not email:
            raise ValueError(_('Users must have an email address'))

        user = self.model(
            email=self.normalize_email(email),
            uid = uid,
            nickname=nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, uid, nickname, password):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        단, 최상위 사용자이므로 권한을 부여한다. 
        """
        user = self.create_user(
            email=email,
            uid=uid,
            password=password,
            nickname=nickname,
        )

        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    uid = models.CharField(
        unique=True,
        null=False,
        max_length=255,
        primary_key=True
    )
    email = models.EmailField(
        verbose_name=_('Email address'),
        max_length=255,
        unique=True
    )
    nickname = models.CharField(
        verbose_name=_('Nickname'),
        max_length=30,
    )
    
    gender = models.TextField(
        max_length=1,
        null=True
    )

    birth = models.DateField(null=True)

    introduce = models.TextField(
        max_length=100,
        null=True
    )

    image = models.TextField(
        null=True
    )

    date_joined = models.DateTimeField(
        verbose_name=_('Date joined'),
        default=timezone.now
    )

    is_active = models.BooleanField(
        verbose_name=_('Is active'),
        default=True
    )



    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['uid','nickname']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('-date_joined',)

    def __str__(self):
        return self.nickname

    def get_full_name(self):        
        return self.nickname

    def get_short_name(self):
        return self.nickname

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All superusers are staff
        return self.is_superuser

    get_full_name.short_description = _('Full name')


# 팔로워 / 팔로우 중개 모델
class Follow(models.Model):
    #나를 팔로우 하는 사람들
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
        )
    #내가 팔로우 하는 사람들
    followee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followee'
        )

    def following(self):
        return f'{self.follower.nickname} is following {self.followee.nickname}'