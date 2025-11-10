# user/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
    # 회원가입 경로
    path('term/', views.term_view, name='term'),
    path('signup/', views.signup_view, name='signup'),
    path('complete/', views.signup_complete_view, name='signup_complete'),

    # 로그인 및 로그아웃 경로
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    #DIMC 진단 페이지

    #path('dimc/', views.dimc_test_view, name='dimc_test'),
    #path('dimc/results/', views.dimc_results_view, name='dimc_results'),


    #마이페이지
    path('mypage/', views.mypage_view, name='mypage'),
    path('mypage/update/', views.mypage_update_view, name='mypage_update'),
    path('mypage/delete/', views.user_delete_view, name='mypage_delete'),

    #DIMC
    path('DIMC', views.DIMC_view, name='DIMC'),
    path('DIMC_archive', views.DIMC_archive_view, name='DIMC_archive'),

    path('community/', views.community_view, name='community' ),
    path('course/', views.courses_view, name='courses' ),




    path('find_id/', views.find_id_view, name='find_id'),

    # 비밀번호 재설정 절차 (Django 내장 기능 활용)
    # 1. 비밀번호 재설정 요청 (이메일 입력)
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='user/password_reset_form.html', # 우리가 만들 템플릿
             email_template_name='user/password_reset_email.html', # 이메일 내용 템플릿
             success_url='/user/password_reset/done/'),
         name='password_reset'),

    # 2. 재설정 이메일 발송 완료
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='user/password_reset_done.html'),
         name='password_reset_done'),

    # 3. 이메일의 링크를 클릭하여 비밀번호 재설정 (새 비밀번호 입력)
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='user/password_reset_confirm.html',
             success_url='/user/password_reset/complete/'),
         name='password_reset_confirm'),

    # 4. 비밀번호 재설정 완료
    path('reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='user/password_reset_complete.html'),
         name='password_reset_complete'),


]