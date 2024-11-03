from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Registrations , Branche
from .serializer import RegistrationsSerializer,BrancheGetSerializer,ChooseRedirectedBranche
from django.http import HttpResponse
from django.template.loader import render_to_string
import datetime
import pdfkit
import qrcode
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
# Create your views here.

@api_view(['POST'])
def create_new_registration(request):
    data = request.data
    serializer = RegistrationsSerializer(data=data)
    
    if serializer.is_valid():
        if Registrations.objects.filter(email=data.get('email')).exists():
            return Response({'email':'email is found'},status=status.HTTP_302_FOUND)
        registration = Registrations.objects.create(
            arabic_first_name=data.get('arabic_first_name'),
            arabic_last_name=data.get('arabic_last_name'),
            latin_fullname=data.get('latin_fullname'),
            birthday=data.get('birthday'),
            branche_id=data.get('branche'),  # Assuming 'branche' is passed as the ID
            address=data.get('address'),
            phone_number = data.get('phone_number'),
            gender = data.get('gender'),
            email = data.get('email'),
            birth_certificat=request.FILES.get('birth_certificat'),  # Handle file upload
            white_pic=request.FILES.get('white_pic'),  # Handle image upload
            blood_type=request.FILES.get('blood_type'), 
            medical_certificat=request.FILES.get('medical_cert')# Handle file upload
        )
        print(f'this is the branch {data.get('branche')}')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def get_branches(request):
    branches = Branche.objects.all()
    serilizer = BrancheGetSerializer(branches,many=True)
    return Response(serilizer.data)


config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\wkhtmltopdf.exe')
@api_view(['POST'])
def generate_certificate_pdf(request):
    data = request.data
    year = datetime.datetime.now().year
    branche = Branche.objects.get(pk=data.get('branche')).address
    print(year)
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    certificate_data = {
        'arabic_first_name': data.get('arabic_first_name'),
        'arabic_last_name': data.get('arabic_last_name'),
        'latin_fullname': data.get('latin_fullname'),
        'birthday': data.get('birthday'),
        'branch_name': branche,  # Assuming the branch name is passed
        'phone_number': data.get('phone_number'),
        'issue_date': current_date  # You can dynamically set this to today's date
    }

    # Generate QR Code with specific codification (e.g., user registration details)
    qr_data = f"{year}/{branche}/{data.get('birthday')}"
    qr_code_img = qrcode.make(qr_data)

    # Convert the QR code image to a binary stream
    qr_stream = BytesIO()
    qr_code_img.save(qr_stream, format='PNG')
    qr_stream.seek(0)  # Reset the stream pointer to the beginning
    
    # Convert the stream to base64 for embedding in the HTML
    import base64
    qr_base64 = base64.b64encode(qr_stream.read()).decode('utf-8')
    qr_image_src = f"data:image/png;base64,{qr_base64}"

    # Add the QR code to the certificate data
    certificate_data['qr_image_src'] = qr_image_src

    # Render the HTML certificate with the QR code and provided data
    html_content = render_to_string('certificate.html', certificate_data)

    # Convert the rendered HTML into a PDF
    pdf = pdfkit.from_string(html_content, False, configuration=config)

    # Create a response to return the PDF as a downloadable attachment
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'
    response['Content-Length'] = len(pdf)

    return response


#create functions of accepte and redirect and unaccpete


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Accepte_registration(request,pk):
    registration = Registrations.objects.get(pk=pk)
    registration.is_accepted = True
    registration.save()
    return Response({'data':'Accepted'},status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unaccepte_registration(request,pk):
    registration = Registrations.objects.get(pk=pk)
    registration.delete()
    return Response({'data':'unaccepted (deleted)'},status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def redirect_registration(request, pk):
    data = request.data
    serializer = ChooseRedirectedBranche(data=data)
    if serializer.is_valid():
        registration = get_object_or_404(Registrations, pk=pk)
        try:
            current_branch = Branche.objects.get(user=request.user)
        except Branche.DoesNotExist:
            return Response({'error': 'User does not belong to any branch'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            to_be_redirected_branche = Branche.objects.get(pk=data.get('branche'))
        except Branche.DoesNotExist:
            return Response({'error': 'Target branch does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        if current_branch == to_be_redirected_branche:
            return Response({'data': 'You are in the same branch'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            registration.branche = to_be_redirected_branche
            registration.save()
            return Response({'data': 'You have successfully changed the branch'}, status=status.HTTP_202_ACCEPTED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

        

        