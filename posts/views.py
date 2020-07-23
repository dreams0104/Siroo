from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post, Comment, Tag
from django.utils import timezone
from datetime import datetime
#hot_tag를 위해 db.models에서 Count import해옴.
from django.db.models import Count


def index(request):

    posts = Post.objects.all().order_by('-created_at')
    #전체 태그에서 가장 많이 쓰인 태그 불러오기    
    tags = Tag.objects.all().annotate(num_posts=Count('taged_post')).order_by('-num_posts')        
    hot_tags = list(tags)[0:9]
    TAGS = Tag.objects.all()
    #daycount 각각 만들어줌.
    if len(list(posts)) > 0:
        for post in posts:
            past = post.created_at
            now = timezone.now()
            sec = now - past
            countd = int((sec).total_seconds()/3600)
            countday = int((sec).total_seconds()/3600/24)
            daycount = ""
            #past와 now를 문자열로나눈 뒤, 날짜가 보이는 부분을 인덱싱함
            #시간이 경과 되었어도 날짜가 바뀐지를 확인하기 위함.
            a = str(past)[0:10]
            b = str(now)[0:10]
            if a == b:
                daycount = "오늘 "
            elif countd < 24 :
                daycount = "하루 전"
            else :
                daycount = str(countday) + "일 전"  

        daycounts_dic = {}
        daycounts_dic[post] = daycount
        post.daycount = daycounts_dic.get(post)
        daycount = post.daycount
    else:
        daycount = None
        pass

    print(daycount)

    context = {
        'posts' : posts,
        'daycount' : daycount,
        'hot_tags' : hot_tags,
        'TAGS' : TAGS,
    }
    
    return render(request, 'posts/index.html', context)
    

def detail(request, post_id):

    post = Post.objects.get(id=post_id)
    #detail templates에서 사용하기 위해 context에 제공해야하기에 쿼리셋을 리스트형태로 받아옴.
    tags = list(post.taginpost.all())
    print(tags)
    tag_ids =[*map(lambda tag:tag.id, list(post.taginpost.all()))]
    #연관 tag의 id를 int형태로 받아옴.
    print(tag_ids)
    if len(tag_ids) > 0:
        tag_id = tag_ids.pop()
        tag = Tag.objects.get(id=tag_id)
        posts = tag.taged_post.all()
    else:
        pass


    #날짜 계산 기능
    past = post.created_at
    now = timezone.now()
    sec = now - past
    countd = int((sec).total_seconds()/3600)
    countday = int((sec).total_seconds()/3600/24)
    daycount = ""
    #past와 now를 문자열로나눈 뒤, 날짜가 보이는 부분을 인덱싱함
    #시간이 경과 되었어도 날짜가 바뀐지를 확인하기 위함.
    a = str(past)[0:10]
    b = str(now)[0:10]

    if a == b:
        daycount = "오늘 작성됨"
    elif countd < 24 :
        daycount = "1일 전에 작성됨"
    else :
        daycount = str(countday) + "일 전에 작성 됨"

    #댓글 뷰 기능
    comments = post.comment_set.all().order_by('-id')

    context = {
        'post' : post,
        'daycount': daycount,
        'comments' : comments,
        'tags' : tags,
}
    return render(request, 'posts/detail.html', context)

def new(request):

    return render(request, 'posts/new.html')

def create(request):

    author = request.POST['author']
    body = request.POST['body']
    post = Post(author = author, body = body)
    post.save()

    #바로 detail페이지로 가지 않고, tag저장 후 가기 위해서 tagforpost로 이동
    return redirect('posts:tagforpost', post_id=post.id)

def tagforpost(request, post_id):

    post = Post.objects.get(id=post_id)
    #본문을 str으로 바꾼 뒤, 띄어쓰기대로 Split해서 list로 저장함.    
    body = str(post.body).split()

    taglist = list()
    original_tags = list()

    #태그가 있는지 확인하는 과정
    if len(body) > 0 :

        for i in body:
            if i.count('#') > 0:
                taglist.append(i)
            else:
                pass

    #글 수정시 태그 중복 저장 방지(새로 작성된 글은 이 과정이 생략됨)
        if post.taginpost.all():
            for tag in list(post.taginpost.all()):
                original_tags.append(tag)
            if taglist == original_tags:
                return redirect('posts:detail', post_id=post.id)
            else:
                tag = post.taginpost.all()
                tag.delete()
        else:
            pass
    #-------------------------------------------------------------             
    #태그가 있을 시, #을 빼내고 문자열로 바꿔주어서 태그에 저장함.
        for i in taglist: 
            x = i.split('#')
            del x[0]
            tag_text = ''.join(x)

            #태그를 스플릿해서 '#'이 빠진 스트링 형태로 tag에 저장함
            tag=Tag(tag=tag_text)
            post.save()
            "태그"
            
            #태그가 기존에 있는 태그면, 쿼리셋에 추가만 해주고,
            #태그가 기존에 없는 태그라면 태그를 저장한 뒤에 쿼리셋에 추가함.
            try:
                tag = Tag.objects.get(tag=tag_text)
                
            except Tag.DoesNotExist:
                tag.save()

            post.taginpost.add(tag)
    
    return redirect('posts:detail', post_id=post.id)

def edit(request, post_id):

    post = Post.objects.get(id=post_id)
    context = {
        'post' : post
    }
    return render(request, 'posts/edit.html', context)

def update(request, post_id):
        
    post = Post.objects.get(id=post_id)
    post.author = request.POST['author']
    post.body = request.POST['body']
    post.save()

    #바로 detail페이지로 가지 않고, tag저장 후 가기 위해서 tagforpost로 이동
    return redirect('posts:tagforpost', post_id=post.id)    

def delete(request, post_id):

    #post 삭제 시, 연관 tag를 불러오고, 전부 지워버린 후 post를 지움
    post = Post.objects.get(id=post_id)
    tag = post.taginpost.all()
    tag.delete()
    post.delete()

    return redirect('posts:index')

def comment_create(request, post_id):
    
    post = Post.objects.get(id=post_id)
    author = request.POST['author']
    body = request.POST['body']
    comment = Comment(post=post, author=author, body=body)
    comment.save()



    return redirect('posts:detail', post_id=post.id)

def comment_edit(request, comment_id):

    comment = Comment.objects.get(id=comment_id)
    post = comment.post
    
    context = {
        'comment' : comment,
        'post' : post
    }
    return render(request, 'posts/comment_edit.html', context)


def comment_update(request, comment_id):

    comment = Comment.objects.get(id=comment_id)
    post = comment.post
    comment.author = request.POST['author']
    comment.body = request.POST['body']
    comment.save()

    #바로 detail페이지로 가지 않고, tag저장 후 가기 위해서 tagforpost로 이동
    return redirect('posts:detail', post_id=post.id)    

def comment_delete(request, comment_id):
    
    #post 삭제 시, 연관 tag를 불러오고, 전부 지워버린 후 post를 지움
    comment = Comment.objects.get(id=comment_id)
    post = comment.post
    #tag = post.taginpost.all()
    #tag.delete()
    comment.delete()

    return redirect('posts:detail', post_id=post.id)


def tag_filter(request, tag_id):

    tag = Tag.objects.get(id=tag_id)

    return redirect('posts:taged_post_filter', tag_id=tag.id)

def taged_post_filter(request, tag_id):

    tag = Tag.objects.get(id=tag_id)
    posts = tag.taged_post.all().order_by('-created_at')    
    #불러오는 Posts의 숫자를 제한하기
    posts = list(posts)[0:4]
    #전체 태그에서 가장 많이 쓰인 태그 불러오기    
    tags = Tag.objects.all().annotate(num_posts=Count('taged_post')).order_by('-num_posts')        
    hot_tags = list(tags)[0:9]
    print(tags)

    #created_at 간소화 시키기
    for post in posts:
        past = post.created_at
        now = timezone.now()
        sec = now - past
        countd = int((sec).total_seconds()/3600)
        countday = int((sec).total_seconds()/3600/24)
        daycount = ""
        #past와 now를 문자열로나눈 뒤, 날짜가 보이는 부분을 인덱싱함
        #시간이 경과 되었어도 날짜가 바뀐지를 확인하기 위함.
        a = str(past)[0:10]
        b = str(now)[0:10]

        if a == b:
            daycount = "오늘 "
        elif countd < 24 :
            daycount = "하루 전"
        else :
            daycount = str(countday) + "일 전"  

    context = {
        'posts' : posts,
        'daycount' : daycount,
        'hot_tags' : hot_tags,
    }
    
    return render(request, 'posts/taged_post_filter.html', context)

def TAG_filter(request, TAG_id):


    tag = Tag.objects.get(id=TAG_id)
    posts = tag.taged_post.all().order_by('-created_at')    
    #불러오는 Posts의 숫자를 제한하기
    posts = list(posts)[0:4]
    #전체 태그에서 가장 많이 쓰인 태그 불러오기    
 
    #created_at 간소화 시키기
    for post in posts:
        past = post.created_at
        now = timezone.now()
        sec = now - past
        countd = int((sec).total_seconds()/3600)
        countday = int((sec).total_seconds()/3600/24)
        daycount = ""
        #past와 now를 문자열로나눈 뒤, 날짜가 보이는 부분을 인덱싱함
        #시간이 경과 되었어도 날짜가 바뀐지를 확인하기 위함.
        a = str(past)[0:10]
        b = str(now)[0:10]

        if a == b:
            daycount = "오늘 "
        elif countd < 24 :
            daycount = "하루 전"
        else :
            daycount = str(countday) + "일 전"  

    context = {
        'posts' : posts,
        'daycount' : daycount,
    }
    
    return render(request, 'posts/TAG_filter.html', context) 