from rest_framework import serializers
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from Registrations.models import Branche

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # You can add custom claims to the token here if needed
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if user is None:
            raise AuthenticationFailed("Incorrect username or password")

        # Assuming your user model has 'first_name' and 'last_name' fields
        refresh = self.get_token(user)
        # data.pop('refresh', None)
        # data.pop('access', None)
        data['user'] = {
            'id': user.id,
            'first_name': user.first_name,  # Corrected field name to 'first_name'
            'last_name': user.last_name,    # Corrected field name to 'last_name'
            'username': user.username,
            'email': user.email,
            'groups': list(user.groups.values_list('name', flat=True)),
            # 'token': str(refresh.access_token)
        }
        data['status'] = True
        data['Code'] = status.HTTP_200_OK
        return data
    
class BrancheSerializer(serializers.ModelSerializer): 
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Branche
        fields = ['Trainer', 'address','password','email']