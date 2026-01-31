from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from .serializers import RegistrationSerializer

class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response({'message': 'Logged in successfully'})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

def logout_view(request):
    from django.contrib.auth import logout
    from django.http import JsonResponse
    logout(request)
    return JsonResponse({'message': 'Logged out successfully'})
