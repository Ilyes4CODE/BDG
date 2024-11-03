from django.urls import path
from . import views
urlpatterns = [
    path('Create_registration/',views.create_new_registration),
    path('All_Branches/',views.get_branches),
    path('api/generate-certificate/',views.generate_certificate_pdf),
    path('Accepte_Registration/<str:pk>/',views.Accepte_registration),
    path('Delete_registration/<str:pk>/',views.unaccepte_registration),
    path('redirect_registrations/<str:pk>/',views.redirect_registration),


]
