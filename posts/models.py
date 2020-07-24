from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.

class Post(models.Model):
    
    author = models.CharField(max_length=50)
    body = models.TextField()
    #auto_now=수정시마다 반영, auto_now_add=생성일자로 고정
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    #ManytoManyField로 태그 저장.
    taginpost = models.ManyToManyField("Tag", related_name='taged_post')

    @property
    def daycount(self):

        past = self.created_at
        now = timezone.now()
        sec = now - past
        countminutes = int((sec).total_seconds()/60)
        counttimes = int((sec).total_seconds()/3600)
        countdays = int((sec).total_seconds()/3600/24)
        countmonths = int((sec).total_seconds()/3600/24/744)
        countyears = int((sec).total_seconds()/3600/24/365)
        #past와 now를 문자열로나눈 뒤, 날짜가 보이는 부분을 인덱싱함
        #시간이 경과 되었어도 날짜가 바뀐지를 확인하기 위함.
        a = str(past)[0:10]
        b = str(now)[0:10]
        c = str(past)[11:13]
        d = str(now)[11:13]

        if a == b:
            if c == d:
                return str(countminutes) + "분 전"
            else:
                return str(counttimes) + "시간 전" 
        elif countdays < 24:
            return "1일 전"
        elif countdays < 744: 
            return str(countdays) + "일 전"
        elif countdays < 8760:
            return str(countmonths) + "달 전"
        else:
            return str(countyears) + "년 전"

    def __str__(self):  

        return f'author{self.author} : body{self.body} / tag {self.taginpost.all()} {self.daycount}'

class Comment(models.Model):
    
    #post와 1:N관계로 하나의 포스트에는 여러개의 코멘트 가능. 그리고 원글 삭제시 댓글 삭제도 필요함)
    post = models.ForeignKey("Post", on_delete=models.CASCADE, null=True)
    author = models.CharField(max_length=50)
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    #ManytoManyField로 태그 저장.
    tagincomment = models.ManyToManyField("Tag", related_name='taged_comment')

    @property
    def daycount(self):

        past = self.created_at
        now = timezone.now()
        sec = now - past
        countminutes = int((sec).total_seconds()/60)
        counttimes = int((sec).total_seconds()/3600)
        countdays = int((sec).total_seconds()/3600/24)
        countmonths = int((sec).total_seconds()/3600/24/744)
        countyears = int((sec).total_seconds()/3600/24/365)
        #past와 now를 문자열로나눈 뒤, 날짜가 보이는 부분을 인덱싱함
        #시간이 경과 되었어도 날짜가 바뀐지를 확인하기 위함.
        a = str(past)[0:10]
        b = str(now)[0:10]
        c = str(past)[11:13]
        d = str(now)[11:13]

        if a == b:
            if c == d:
                return str(countminutes) + "분 전"
            else:
                return str(counttimes) + "시간 전" 
        elif countdays < 24:
            return "1일 전"
        elif countdays < 744: 
            return str(countdays) + "일 전"
        elif countdays < 8760:
            return str(countmonths) + "달 전"
        else:
            return str(countyears) + "년 전"

    def __str__(self):
        return f'author{self.author} : body{self.body} {self.daycount}'

class Tag(models.Model):

    tag = models.CharField(max_length=15)
        
    def __str__(self):
        
        return f'{self.tag}'




