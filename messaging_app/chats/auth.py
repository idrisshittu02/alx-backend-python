from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        
        def validate_password(self, value):
            validate_password(value)
            return value
        
        def create(self, validated_data):
            user = User.objects.create_user(
                username=validated_date['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )
            return user
        
class UserRegistrationView(APIView):
    """View for user registration."""
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User registered successfully',
                'username': user.username,},status=status.HTTP_201_CREATED
            })
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)