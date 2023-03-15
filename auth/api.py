from rest_framework import routers
from auth.views import LoginView, RegisterView,SecurityView


auth_router = routers.DefaultRouter()

auth_router.register(r'login',LoginView,basename="login")
auth_router.register(r'register',RegisterView,basename="register")
auth_router.register(r'security',SecurityView,basename="security")