from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
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


class BlogView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            blogs = Blog.objects.filter(user = request.user)
            serializer = BlogSerializer(blogs, many = True)
            username = request.user.username
            return Response({
                'success' : True,
                'message' : f'Blogs by {username}',
                'data' : serializer.data
            }, status = status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
            return Response({
                'success' : False,
                'message' : 'Something went wrong.',
                'error' : str(ex)
            }, status = status.HTTP_400_BAD_REQUEST)

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