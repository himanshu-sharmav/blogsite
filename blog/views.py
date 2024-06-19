from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Blog, Comment, Like
from .serializers import UserSerializer, BlogSerializer, CommentSerializer, LikeSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.pagination import PageNumberPagination
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        method="post",
        operation_summary="Register User",
        operation_description="Create a new user account",
        request_body=UserSerializer,
        responses={201: UserSerializer()}
    )

    def create(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,status=status.HTTP_201_CREATED,headers=headers)

class BlogPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class BlogViewSet(viewsets.ModelViewSet):
    queryset=Blog.objects.all()
    serializer_class=BlogSerializer
    permission_classes=[permissions.IsAuthenticated]
    pagination_class = BlogPagination

    @swagger_auto_schema(
        method="post",
        operation_summary="Create Blog",
        operation_description="Create a new blog post",
        request_body=BlogSerializer,
        responses={201: BlogSerializer()}
    )

    @swagger_auto_schema(
        method="put",
        operation_summary="Update Blog",
        operation_description="Update an existing blog post",
        request_body=BlogSerializer,
        responses={200: BlogSerializer()}
    )

    @swagger_auto_schema(
        method="delete",
        operation_summary="Delete Blog",
        operation_description="Delete an existing blog post"
    )

    @swagger_auto_schema(
        method="get",
        operation_summary="List Blogs",
        operation_description="List all blog posts",
        responses={200: BlogSerializer(many=True)}
    )

    @swagger_auto_schema(
        method="get",
        operation_summary="Retrieve Blog",
        operation_description="Retrieve a single blog post",
        responses={200: BlogSerializer()}
    )

    def perform_create(self,serializer):
        serializer.save(author=self.request.user)

    @swagger_auto_schema(
        method="post",
        operation_summary="Like Blog",
        operation_description="Like a blog post",
        responses={200: {'status': 'liked'}}
    )            

    @action(detail=True,methods=['post'])
    def like(self,request,pk=None):
        blog=self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, blog=blog)
        if created:
            return Response({'status': 'blog liked'})
        else:
            return Response({'status': 'blog already liked'})
        
    @swagger_auto_schema(
        method="post",
        operation_summary="Unlike Blog",
        operation_description="Unlike a blog post",
        responses={200: {'status': 'unliked'}}
    )    

    @action(detail=True,methods=['post'])
    def unlike(self,request,pk=None):
        blog = self.get_object()
        try:
            like = Like.objects.get(user=request.user, blog=blog)
            like.delete()
            return Response({'status': 'blog unliked'})
        except Like.DoesNotExist:
            return Response({'status': 'blog not liked'}, status=status.HTTP_400_BAD_REQUEST)
    
class CommentPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50

class CommentViewSet(viewsets.ModelViewSet):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    permission_classes=[IsAuthenticated]
    pagination_class=CommentPagination

    @swagger_auto_schema(
        method="post",
        operation_summary="Create Comment",
        operation_description="Create a new comment on a blog post",
        request_body=CommentSerializer,
        responses={201: CommentSerializer()}
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LikeViewSet(viewsets.ModelViewSet):
    queryset=Like.objects.all()
    serializer_class=LikeSerializer
    permission_classes=[IsAuthenticated]


# schema_view = get_schema_view(
#     openapi.Info(
#         title="Blog API",
#         default_version='v1',
#         description="API documentation for the Blog project",
#         terms_of_service="https://www.google.com/policies/terms/",
#         contact=openapi.Contact(email="contact@blog.local"),
#         license=openapi.License(name="BSD License"),
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )


























