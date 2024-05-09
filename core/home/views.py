from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from .serializers import *


class RegisterView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = RegisterSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success' : True,
                    'message' : 'Your account is created.',
                    'data' : serializer.data
                }, status = status.HTTP_201_CREATED)
            
            return Response({
                    'success' : False,
                    'message' : 'Error occured.',
                    'error' : serializer.errors
                }, status = status.HTTP_400_BAD_REQUEST)
        
        except Exception as ex:
            return Response({
                    'success' : False,
                    'message' : 'Something went wrong.',
                    'error' : str(ex)
                }, status = status.HTTP_400_BAD_REQUEST)
        

class LoginView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)

            if serializer.is_valid():
                response = serializer.get_jwt_token(serializer.validated_data)
                return Response(response, status=status.HTTP_200_OK)
            
            return Response({
                    'success' : False,
                    'message' : 'Error occured.',
                    'error' : serializer.errors
                }, status = status.HTTP_400_BAD_REQUEST)
        
        except Exception as ex:
            print(ex)
            return Response({
                    'success' : False,
                    'message' : 'Something went wrong.',
                    'error' : str(ex)
                }, status = status.HTTP_400_BAD_REQUEST)


class CreateBlog(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            data['user'] = request.user.id
            serializer = BlogSerializer(data = data)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success' : True,
                    'message' : 'Blog created successfully.',
                    'data' : serializer.data
                }, status = status.HTTP_201_CREATED)
            
            return Response({
                'success' : False,
                'message' : 'Error occured.',
                'error' : serializer.errors
            }, status = status.HTTP_400_BAD_REQUEST)
        
        except Exception as ex:
            print(ex)
            return Response({
                'success' : False,
                'message' : 'Something went wrong.',
                'error' : str(ex)
            }, status = status.HTTP_400_BAD_REQUEST)
        

class ViewUserBlogs(APIView):
    def get(self, request, pk):
        try:
            user = request
            blogs = Blog.objects.filter(user = pk)
            search_query = request.GET.get('search')

            if search_query:
                blogs = blogs.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))

            serializer = BlogSerializer(blogs, many = True)
            user = User.objects.get(id = pk)

            return Response({
                'success' : True,
                'message' : f'Blogs by {user}',
                'data' : serializer.data
            }, status = status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({
                'success' : False,
                'message' : 'User not found.',
            }, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as ex:
            print(ex)
            return Response({
                'success' : False,
                'message' : 'Something went wrong.',
                'error' : str(ex)
            }, status = status.HTTP_400_BAD_REQUEST)
        
