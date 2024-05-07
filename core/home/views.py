from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
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
                    'message' : 'Something went wrong.',
                    'error' : serializer.errors
                }, status = status.HTTP_400_BAD_REQUEST)
        except:
            return Response({
                    'success' : False,
                    'message' : 'Something went wrong.',
                    'error' : serializer.errors
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
                    'message' : 'Something went wrong..',
                }, status = status.HTTP_400_BAD_REQUEST)

