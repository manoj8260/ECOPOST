from django.urls import path
from .views import * 
urlpatterns=[
    path('echopost/',user_login,name='echopost'),
    path('',home,name='home'),
    path('register/',register,name='register'),
    path('login/',user_login,name='user_login'),
    path('user_logout/',user_logout,name='user_logout'),
    path('userprofile/',user_profile,name='user_profile'),
    path('createtweet/',create_tweet,name='create_tweet'),
    path('saved/',saved,name='saved'),
    path('update/<pk>/',update,name='update'),
    path('deletetweet/<pk>/',delete,name='deletetweet'),
    path('save<pk>/',save,name='save'),
    path('like<pk>/',like,name='like'),
    path('savecomment/<int:pk>/', savecomment, name='savecomment'),
    path('commentes/<pk>/',commentes,name='commentes'),
    path('deletecomment/<int:pk>',DeleteComment.as_view(),name='deletecomment'),
    path('addstory/',story,name='addstory'),
    path('showstory/<int:pk>/',Showstory.as_view(),name="showstory"),
    path('explore/',Explores.as_view(),name='explore'),
    path('forget_password/',forgot_password.as_view(),name='forgot_password'),
    path('otp/',otp.as_view(),name='otp'),
    path('new_password/',new_password.as_view(),name='new_password'),
    path('change_password/',ChangePassword.as_view(),name='change_password'),
    path('editprofile/',Editprofile.as_view(),name='editprofile'),
    path('deletestory/<int:pk>/',DeleteStory.as_view(),name='deletestory'),
    path('usersearch',search_user,name='search_user'),
    path('finduser/<str:name>',find_user,name='find_user'),
    path('follow/<int:user_id>/', follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow_user'),
    path('followers/<str:username>/', followers_list, name='followers_list'),
    path('following/<str:username>/', following_list, name='following_list'),
]

  

   
   
    
