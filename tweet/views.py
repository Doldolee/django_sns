from django.shortcuts import render, redirect
from .models import TweetModel, TweetComment
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, TemplateView


# Create your views here.
def home(request):
    #user가 로그인 되어있는지 확인
    user = request.user.is_authenticated
    if user:
        return redirect("/tweet")
    else:
        return redirect("/sign-in")

def tweet(request):
    if request.method == "GET":
        user = request.user.is_authenticated
        if user:
            all_tweet = TweetModel.objects.all().order_by("-created_at") #모든 데이터를 불러오겠다. 최신순으로
            return render(request, "tweet/home.html", {'tweet':all_tweet}) #화면으로 데이터 넘겨줌
        else:
            return redirect("/sign-in")
    elif request.method == "POST":
        user = request.user #지금 로그인되어있는 사용자
        content = request.POST.get("my-content","")
        tags = request.POST.get("tag","").split(',')

        if content == "":
            all_tweet = TweetModel.objects.all().order_by("-created_at")  # 모든 데이터를 불러오겠다. 최신순으로
            return render(request, "tweet/home.html",{"error":"글은 공백이면 안된다.","tweet":all_tweet})
        else:
            my_tweet = TweetModel.objects.create(author=user, content=content)
            for tag in tags:
                tag = tag.strip()
                if tag!="":
                    my_tweet.tags.add(tag)
            my_tweet.save()
            # my_tweet = TweetModel()
            # my_tweet.author = user
            # my_tweet.content = request.POST.get('my-content','')
            # my_tweet.save()
            return redirect('/tweet')

@login_required
def delete_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    my_tweet.delete()
    return redirect('/tweet')

@login_required
def detail_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    #댓글 모델 가져오기
    tweet_comment = TweetComment.objects.filter(tweet_id=id).order_by("-created_at")
    return render(request, "tweet/tweet_detail.html",{"tweet":my_tweet, "comment":tweet_comment})

@login_required()
def write_comment(request, id):
    if request.method == "POST":
        comment = request.POST.get('comment',"")
        current_tweet = TweetModel.objects.get(id=id)
        TC = TweetComment()
        TC.comment = comment
        TC.author = request.user
        TC.tweet = current_tweet
        TC.save()
        return redirect("/tweet/"+str(id))

def delete_comment(request, id):
    comment = TweetComment.objects.get(id=id)
    currnt_tweet = comment.tweet.id #comment가 있는 tweet의 아이디 불러오기
    comment.delete()
    return redirect("/tweet/"+str(currnt_tweet))

class TagCloudTV(TemplateView):
    template_name = 'taggit/tag_cloud_view.html'


class TaggedObjectLV(ListView):
    template_name = 'taggit/tag_with_post.html'
    model = TweetModel

    def get_queryset(self):
        return TweetModel.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context