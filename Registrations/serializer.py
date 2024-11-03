from rest_framework import serializers
from .models import Registrations,Branche

class RegistrationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registrations
        fields = '__all__'

class BrancheGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branche
        fields = '__all__'


class ChooseRedirectedBranche(serializers.ModelSerializer):
    class Meta:
        model = Registrations
        fields = ['branche']
        
