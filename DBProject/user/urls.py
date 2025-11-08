# user/urls.py
from django.urls import path
from . import views

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


]