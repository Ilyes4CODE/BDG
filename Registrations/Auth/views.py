from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from .seriliazers import CustomTokenObtainPairSerializer,BrancheSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from django.contrib.auth.models import User,Group
from .decorators import group_required
from Registrations.models import Branche , Registrations
from Registrations.serializer import RegistrationsSerializer

class CustomTokenObtainPairView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed as e:
            return Response({
                'status': False,
                'message': "Incorrect username or password"
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@group_required('admin')
def add_new_branches(request):
    data = request.data
    serializer = BrancheSerializer(data=data)
    if serializer.is_valid():
        user = User.objects.create(
            username = data['email'],
            password = make_password(data['password'])
        )
        group, created = Group.objects.get_or_create(name='branch')
        user.groups.add(group)
        Branche.objects.create(
            user=user,
            Trainer =data['Trainer'],
            address =data['address'],
            email = data['email']
        )
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@group_required('admin')
def delete_branche(request,pk):
    branche = Branche.objects.get(pk=pk)
    branche.delete()
    return Response({'detail':'Brranch Deleted succesfully'},status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@group_required('branch')
def Get_Branch_Registrations(request):
    user = request.user
    branch = Branche.objects.get(user=user)
    exacted_registrations = Registrations.objects.filter(branche=branch)
    serializer = RegistrationsSerializer(exacted_registrations,many=True)
    return Response(serializer.data)
