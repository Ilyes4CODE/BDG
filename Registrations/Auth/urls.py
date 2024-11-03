from django.urls import path
from .views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('Add_Branch/',views.add_new_branches),
    path('Branch_Registration/',views.Get_Branch_Registrations),
    path('Delete_Branch/<str:pk>',views.delete_branche),
]
