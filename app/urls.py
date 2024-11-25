from django.urls import path, include
from rest_framework import routers
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


router = routers.DefaultRouter()
router.register(r'employees', views.EmployeeViewSet, basename='employee')
#router.register(r'login', views.LoginViewSet, basename='login')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('employee/pay/', views.MoveRecordsToArchiveView.as_view(), name='move_records_to_archive'),
]
