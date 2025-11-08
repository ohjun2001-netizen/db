# user/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm  # Django 내장 로그인 폼
from .forms import SignupForm, TermsForm
from django.contrib.auth.decorators import login_required
from .forms import DimcTestForm # 방금 만든 폼을 import
from .models import DIMC # DIMC 모델을 import
from .forms import UserUpdateForm, DIMCForm
from django.conf import settings

def term_view(request):
    """약관 동의 페이지 뷰"""
    if request.method == 'POST':
        # POST 요청 시, 제출된 데이터로 TermsForm을 인스턴스화합니다.
        form = TermsForm(request.POST)
        # 폼 데이터가 유효한지 검사합니다 (agree 체크박스가 선택되었는지).
        if form.is_valid():
            # 약관에 동의했음을 세션에 기록합니다.
            request.session['agreed_to_terms'] = True
            # 회원가입 정보 입력 페이지로 리다이렉트합니다.
            return redirect('user:signup')
    else:
        # GET 요청 시, 비어있는 TermsForm을 생성합니다.
        form = TermsForm()

    # term.html 템플릿을 렌더링하며 form 객체를 전달합니다.
    return render(request, 'user/term.html', {'form': form})


def signup_view(request):
    """회원 정보 입력 페이지 뷰"""
    # 세션에 'agreed_to_terms' 키가 없거나 값이 False이면,
    # 약관에 동의하지 않은 것으로 간주하고 약관 동의 페이지로 보냅니다.
    if not request.session.get('agreed_to_terms', False):
        return redirect('user:term')

    if request.method == 'POST':
        # POST 요청 시, 제출된 회원 정보로 SignupForm을 인스턴스화합니다.
        form = SignupForm(request.POST)
        if form.is_valid():
            # 폼 데이터가 유효하면, User 객체를 생성하되 DB에는 아직 저장하지 않습니다 (commit=False).
            user = form.save(commit=False)
            # 폼에서 검증된 비밀번호를 가져와 안전하게 해싱하여 설정합니다.
            user.set_password(form.cleaned_data['password'])
            # 이제 User 객체를 데이터베이스에 저장합니다.
            # 이때 User 모델에 정의된 save() 메서드가 호출되어 'code'에 따른 역할이 부여됩니다.
            user.save()

            # 회원가입이 완료되었으므로, 보안을 위해 세션에 저장된 동의 기록을 삭제합니다.
            # 약관 동의 세션이 있다면 삭제
            if 'agreed_to_terms' in request.session:
                del request.session['agreed_to_terms']

            # 👇 [추가] 회원가입 완료 플래그를 세션에 저장
            request.session['signup_done'] = True

            return redirect('user:signup_complete')
    else:
        # GET 요청 시, 비어있는 SignupForm을 생성합니다.
        form = SignupForm()

    # signup.html 템플릿을 렌더링하며 form 객체를 전달합니다.
    return render(request, 'user/signup.html', {'form': form})


# 임시 코드를 삭제하고, 원래의 올바른 뷰 코드로 복원합니다.
def signup_complete_view(request):
    """회원가입 완료 페이지 뷰"""

    # 👇 [수정] 세션에 'signup_done' 플래그가 없으면 메인 페이지로 리다이렉트 (규칙 #1)
    if not request.session.get('signup_done', False):
        return redirect('index')

    # 플래그가 있다면, 사용 후 즉시 삭제하여 재접근을 막습니다.
    # 이렇게 하면 사용자가 이 페이지를 새로고침해도 다시 볼 수 없습니다.
    del request.session['signup_done']

    # 정상적인 접근일 경우에만 템플릿을 렌더링
    return render(request, 'user/signup_complete.html')


def login_view(request):
    """로그인 뷰"""
    if request.method == 'POST':
        # Django의 기본 인증 폼(AuthenticationForm) 사용
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # 폼 데이터에서 username(여기서는 email)과 password 추출
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # 사용자 인증
            user = authenticate(request, username=email, password=password)

            if user is not None:
                # 인증 성공 시 로그인 처리
                login(request, user)
                return redirect('index')  # 로그인 성공 후 메인 페이지로 이동
    else:
        form = AuthenticationForm()

    return render(request, 'user/login.html', {'form': form})


def logout_view(request):
    """로그아웃 뷰"""
    logout(request)
    return redirect('index')  # 로그아웃 후 메인 페이지로 이동


'''@login_required  # 로그인이 필수인 페이지
def dimc_test_view(request):
    """DIMC 진단 폼을 보여주고 제출을 처리하는 뷰"""
    if request.method == 'POST':
        form = DimcTestForm(request.POST)
        if form.is_valid():
            # commit=False: DB에 바로 저장하지 않고, 인스턴스만 생성
            dimc_instance = form.save(commit=False)
            # student 필드에 현재 로그인한 사용자를 할당
            dimc_instance.student = request.user
            # 이제 모든 필드가 채워졌으므로 DB에 저장
            dimc_instance.save()
            # 저장 후 결과 목록 페이지로 이동
            return redirect('user:dimc_results')
    else:
        form = DimcTestForm()

    return render(request, 'user/DIMC.html', {'form': form})'''


@login_required
def dimc_results_view(request):
    """로그인한 사용자의 모든 DIMC 진단 결과를 보여주는 뷰"""
    # 현재 로그인한 사용자의 DIMC 결과만 필터링하여 가져옵니다.
    # 최신순으로 정렬합니다.
    user_results = DIMC.objects.filter(student=request.user).order_by('-tested_at')

    return render(request, 'user/dimc_results.html', {'results': user_results})


@login_required # 로그인한 사용자만 접근 가능
def mypage_view(request):
    """마이페이지를 보여주는 뷰"""
    return render(request, 'user/mypage.html')


@login_required
def mypage_update_view(request):
    if request.method == 'POST':
        # POST 요청 시, 제출된 데이터와 현재 사용자 정보(instance)로 폼을 채움
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()  # 변경사항 저장
            return redirect('user:mypage')  # 마이페이지로 복귀
    else:
        # GET 요청 시, 현재 사용자 정보로 채워진 폼을 보여줌
        form = UserUpdateForm(instance=request.user)

    return render(request, 'user/mypage_update.html', {'form': form})


# user/views.py 에 아래 함수 추가
from django.contrib.auth import logout # 추가

@login_required
def user_delete_view(request):
    if request.method == 'POST':
        user = request.user
        user.is_active = False # 계정 비활성화
        user.save()
        logout(request) # 로그아웃 처리
        return redirect('index') # 메인 페이지로 이동

    return render(request, 'user/mypage_delete.html')


@login_required
def DIMC_archive_view(request):
    if request.method == 'POST':
        form = DIMCForm(request.POST)
        if form.is_valid():
            dimc = form.save(commit=False)
            dimc.student = request.user  # 로그인 사용자로 설정
            dimc.save()
            return redirect('user:DIMC_archive')  # 저장 후 다시 목록 혹은 동일 페이지로 리다이렉트
    else:
        form = DIMCForm()
    return render(request, 'user/DIMC_archive.html', {'form': form})

def DIMC_view(request):
    return render(request, 'user/DIMC.html')

@login_required
def community_view(request):
    return render(request, 'user/community.html')


@login_required
def courses_view(request):
    return render(request, 'user/courses.html')