from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.BlogPostList.as_view(), name = "Home"),
    path('api/', views.PostList.as_view(), name = "api-home"),
    path('create/', views.create, name="create"),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name="post-detail"),
    path('api/posts/<int:pk>/', views.PostDetailAPI.as_view(), name="api-post-detail"),
    path('posts/delete/<int:pk>/', views.delPost, name="post-delete"),
    path('register/', views.register, name = "register"),
    path('logout/', views.logout_view, name = "logout"),
    path('api-auth/', include('rest_framework.urls')),
]