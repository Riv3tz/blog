from urllib import response, request
from .models import BlogPost, User
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import serializers
from .serializers import *
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import *

class BlogPostList(generics.RetrieveAPIView):
    queryset = BlogPost.objects.all()
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        queryset = BlogPost.objects.all()
        return Response({'posts': queryset}, template_name='blog/index.html')

class PostList(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PostDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class PostDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'blog/post_detail.html'

    def get(self, request, pk):
        post = get_object_or_404(BlogPost, pk=pk)
        serializer = PostSerializer
        return Response({'serializer': serializer, 'post': post})

    def post(self, request, pk):
        post = get_object_or_404(BlogPost, pk=pk)
        if post.owner == request.user:
            serializer = PostSerializer(post, data=request.data)
            if not serializer.is_valid():
                return Response({'serializer': serializer, 'post': post})
            serializer.save()
        return redirect('Home')

class Login(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'blog/login.html'

    def get(self, request):
        return Response()

    def post(self, request):
        pass

def delPost(request, pk):
    post = BlogPost.objects.filter(id = pk).first()
    if post.owner == request.user:
        post.delete()
    return redirect('Home')

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()   
            return redirect('/login')
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})

def create(request):
    if request.method == "POST":
        form = PostCreationForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.owner = request.user
            form.save()
        return redirect('Home')
    else:
        form = PostCreationForm()
    return render(request, "blog/post_create.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('Home')