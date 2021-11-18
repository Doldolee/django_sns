from django.shortcuts import render, redirect
from .models import UserModel
from django.http import HttpResponse
from django.contrib.auth import get_user_model #사용자가 데이터베이스에 있는지 확인하는 함수
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.



def sign_up_view(request):
    if request.method == "GET":
        user = request.user.is_authenticated
        if user:
            return redirect("/")
        else:
            return render(request, "user/signup.html")
    elif request.method == "POST":
        username = request.POST.get("username",'')
        password = request.POST.get("password",'')
        password2 = request.POST.get("password2",'')
        bio = request.POST.get("bio",'')
        if password != password2:

            return render(request, "user/signup.html",{"error":'패스워드를 확인해주세요'})
        else:
            if username == '' or password =='':
                return render(request, 'user/signup.html',{'error': "사용자이름과 비밀번호는 필수값 이야"})
            #계정이 있는지 확인
            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                return render(request, "user/signup.html",{"error":"사용자가 존재합니다."})
            else:
                #계정 생성
                UserModel.objects.create_user(username=username, password=password, bio=bio)
                return redirect("/sign-in")

def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', "")
        password = request.POST.get('password', "")

        #인증 모듈로 사용자 DB검사
        me = auth.authenticate(request,username=username, password=password)
        if me is not None: # 사용자가 비어있지 않다면
            auth.login(request, me)
            return redirect("/")
        else:
            return render(request, "user/signin.html",{"error":"유저이름과 패스워드를 확인해주세요"})

        # me = UserModel.objects.get(username=username)  # 사용자 불러오기
        # if me.password == password:  # 저장된 사용자의 패스워드와 입력받은 패스워드 비교
        #     request.session['user'] = me.username  # 세션에 사용자 이름 저장
        #     return HttpResponse("로그인 성공!")
        # else:  # 로그인이 실패하면 다시 로그인 페이지를 보여주기
        #     return redirect('/sign-in')
    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signin.html')

#사용자가 꼭 로그인이 되어있어야만 접근 가능한 함수
@login_required()
def logout(request):
    auth.logout(request)
    return redirect("/")

# user/views.py

@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})


@login_required
def user_follow(request, id):
    me = request.user
    click_user = UserModel.objects.get(id=id)
    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect('/user')