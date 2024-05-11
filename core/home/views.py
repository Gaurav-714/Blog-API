from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from django.core.paginator import Paginator
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
            
        
class UpdateBlog(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        try:
            data = request.data
            blog = Blog.objects.filter(uid = data.get('uid'))

            if not blog.exists():
                return Response({
                    'success' : False,
                    'message' : 'Invalid blog uid.'
                }, status = status.HTTP_404_NOT_FOUND)
            
            if request.user != blog[0].user:
                return Response({
                    'success' : False,
                    'message' : 'You are not authorized for this.'
                }, status = status.HTTP_401_UNAUTHORIZED)
            
            serializer = BlogSerializer(data=data, instance=blog[0], partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success' : True,
                    'message' : 'Blog updated successfully.',
                    'data' : serializer.data
                }, status = status.HTTP_200_OK)
            
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
        

class DeleteBlog(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        try:
            data = request.data
            blog = Blog.objects.filter(uid = data.get('uid'))

            if blog.exists():
                
                if request.user == blog[0].user:
                    blog[0].delete()
                    return Response({
                        'success' : True,
                        'message' : 'Blog deleted successfully.'
                    }, status = status.HTTP_200_OK)

                return Response({
                        'succsss' : False,
                        'message' : 'You are not authorized for this.'
                    }, status = status.HTTP_401_UNAUTHORIZED)
            
            return Response({
                    'success' : False,
                    'message' : 'Invalid blog uid.'
                }, status = status.HTTP_404_NOT_FOUND)
            
        except Exception as ex:
            return Response({
                'success' : False,
                'message' : 'Something went wrong.',
                'error' : str(ex)
            }, status = status.HTTP_400_BAD_REQUEST)
                
            
class PublicBlogs(APIView):
    def get(self, request):
        try:
            blogs = Blog.objects.all().order_by('?')
            search_query = request.GET.get('search')
            if search_query:
                blogs = Blog.objects.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))

            page_number = request.GET.get('page', 1)
            paginator = Paginator(blogs, 5)

            serializer = BlogSerializer(paginator.page(page_number), many=True)
            return Response({
                'success' : True,
                'message' : 'Blogs fetched successfully.',
                'data' : serializer.data
            }, status = status.HTTP_200_OK)
        
        except Exception as ex:
            return Response({
                'success' : False,
                'message' : 'Something went wrong.',
                'error' : str(ex)
            }, status = status.HTTP_400_BAD_REQUEST)
