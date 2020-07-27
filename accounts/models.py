from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from annoying.fields import AutoOneToOneField


class UserManager(BaseUserManager):
    """User 에서 사용하기 위한 UserManager 생성"""
    def create_user(self, email, password=None, **extra_fields):
        """일반 유저로 생성할 경우"""
        if not email:
            raise ValueError('이메일을 입력해주세요')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """superuser 로 user 를 생성할 경우 필드값을 True 로 변경"""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):

    """UserManager 를 objects 필드에 사용"""
    
    CHOICE_GENDER = (
        ('man', '남성'),
        ('woman', '여성'),
        ('human', '선택하지 않음')
    )
    

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    nickname = models.CharField(max_length=20, null=True)
    gender = models.CharField(max_length=10, choices=CHOICE_GENDER)
    

    # UserManager 을 재정의하여 사용
    objects = UserManager()
    # USERNAME 를 email 로 사용
    USERNAME_FIELD = 'email'


class User_profile(models.Model):

    #성민 my_page용 followers model추가(우택 accounts로 옮김)
    user = AutoOneToOneField("accounts.User", on_delete=models.CASCADE, null=True)
    follow = models.ManyToManyField("accounts.User", related_name='follower', blank=True)
    introduce = models.CharField(max_length=300, null=True)
    main_viliage = models.CharField(max_length=10, null=True)
    second_viliage = models.CharField(max_length=10, null=True)
    third_viliage = models.CharField(max_length=10, null=True)
    interrest_tag1 = models.CharField(max_length=15, null=True)
    interrest_tag2 = models.CharField(max_length=15, null=True)
    interrest_tag3 = models.CharField(max_length=15, null=True)


    def __str__(self):
        
        return f'user : {self.user.nickname} 주 동네: {self.main_viliage}' 