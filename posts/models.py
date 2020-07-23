from django.db import models

# Create your models here.

class Post(models.Model):
    
    author = models.CharField(max_length=50)
    body = models.TextField()
    #auto_now=수정시마다 반영, auto_now_add=생성일자로 고정
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    #ManytoManyField로 태그 저장.
    taginpost = models.ManyToManyField("Tag", related_name='taged_post')

    def __str__(self):
        return f'author{self.author} : body{self.body} / tag {self.taginpost.all()}'

class Comment(models.Model):
    
    #post와 1:N관계로 하나의 포스트에는 여러개의 코멘트 가능. 그리고 원글 삭제시 댓글 삭제도 필요함)
    post = models.ForeignKey("Post", on_delete=models.CASCADE, null=True)
    author = models.CharField(max_length=50)
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    #ManytoManyField로 태그 저장.
    tagincomment = models.ManyToManyField("Tag", related_name='taged_comment')

    def __str__(self):
        return f'author{self.author} : body{self.body}'

class Tag(models.Model):

    tag = models.CharField(max_length=15)
        
    def __str__(self):
        
        return f'{self.tag}'




