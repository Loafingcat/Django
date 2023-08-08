# URL 경로와 뷰 함수 간의 매핑을 정의하는 파일이다. 이 파일을 통해서 클라이언트의 요청이 어떤 뷰 함수로 연결되는지 결정하게 됨.
# 어떤 URL이 어떤 기능을 수행하는 뷰 함수와 연결되는지를 관리하는 파일이다.

from django.urls import path
from . import views

urlpatterns = [
    path('search/<str:q>/', views.PostSearch.as_view()),
    path('delete_comment/<int:pk>/', views.delete_comment),
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()),
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    path('create_post/', views.PostCreate.as_view()),
    path('tag/<str:slug>/', views.tag_page),
    path('category/<str:slug>/', views.category_page),
    path('<int:pk>/new_comment/', views.new_comment),
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
]
