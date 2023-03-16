from .serializers import RegisterSerializer
from rest_framework import permissions,viewsets,status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from knox.auth import AuthToken
from django.contrib.auth.signals import user_logged_in
from app.models import Source

class RegisterView(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)

    def create(self,request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        Source.objects.create(user = user, name = 'Қарз')
        Source.objects.create(user = user, name = 'Қарз', type = Source.EXPENSE)
        return Response({"message":"user created"})

class LoginView(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)

    def create(self,request,format=None):
        try:
            serializer=AuthTokenSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user=serializer.validated_data['user']
            token = AuthToken.objects.create(user)[1]
            user_logged_in.send(sender=user.__class__,
                        request=request, user=user)
            data = {
                'user':user.id,
                'token':token,
                'is_staff':user.is_staff,
                'username':user.username
                }
            return Response(data,status=status.HTTP_200_OK)
        except:
            return Response({'message':'user not found'},status=status.HTTP_404_NOT_FOUND)

class SecurityView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        try:
            user = request.user
            if not user.check_password(request.data.get('old_password')):
                return Response({"message":"error old password is not match"}, status=status.HTTP_400_BAD_REQUEST)
            password = request.data.get('new_password')
            user.set_password(password)
            user.save()
            return Response({'message':'password saved successfully'})
        except:
            return Response({'message':'something went wrong'})