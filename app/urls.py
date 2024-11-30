from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


router = routers.DefaultRouter()
router.register(r'api/employees', views.EmployeeViewSet, basename='employee')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/login/', obtain_auth_token, name='api_login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/employee/pay/', views.MoveRecordsToArchiveView.as_view(), name='move_records_to_archive'),
]
