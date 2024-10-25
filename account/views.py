from django.utils import timezone
from datetime import timedelta

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import LoginSerializer, ResetPasswordSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from rest_framework.response import Response
from django_rest_passwordreset.signals import reset_password_token_created, post_password_reset
from django_rest_passwordreset.models import ResetPasswordToken, get_password_reset_token_expiry_time
from django.contrib.auth.password_validation import validate_password, get_password_validators

from django.dispatch import receiver
from rest_framework import exceptions
from AdminDashboardService import settings as s, settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from rest_framework import parsers, renderers, status, permissions
from .serializers import CustomTokenSerializer, CompanySerializer
from .models import Company



from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
class AdminLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        if user.is_staff:
            auth_login(request, user)  # Start session
            token = RefreshToken.for_user(user)
            return Response({
                'status': 200,
                'msg': 'Admin login successful',
                'token': str(token.access_token),
                'refresh_token': str(token),
            })
        else:
            return Response({'status': 403, 'msg': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

class AdminLogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            auth_logout(request)  # End session
            return Response(
                {
                    'status': 200,
                    'message': 'Logout successful'
                }
            )
        except Exception as e:
            return Response(
                {
                    'status': 500,
                    'error': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CustomPasswordResetView:
    @receiver(reset_password_token_created)
    def password_reset_token_created(sender, reset_password_token, *args, **kwargs):
        """
          Handles password reset tokens
          When a token is created, an e-mail needs to be sent to the user
        """
        # send an e-mail to the user
        context = {
            'current_user': reset_password_token.user,
            'username': reset_password_token.user.username,
            'email': reset_password_token.user.email,
            'reset_password_url': "{}/forgot-password/confirm/{}".format("https://cabriot-admin-frontend.vercel.app", reset_password_token.key),
            'site_name': "localhost",
            'site_domain': "https://cabriot-admin-frontend.vercel.app"
        }

        # render email text
        email_html_message = render_to_string('email/user_reset_password.html', context)
        email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

        msg = EmailMultiAlternatives(
            # title:
            "Password Reset for {}".format("Cabriot - Admin"),
            # message:
            email_plaintext_message,
            # from:
            "noreply@somehost.local",
            # to:
            [reset_password_token.user.email]
        )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()


class CustomPasswordTokenVerificationView(APIView):
    """
      An Api View which provides a method to verifiy that a given pw-reset token is valid before actually confirming the
      reset.
    """
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['password']
        password2 = serializer.validated_data['password2']
        token = serializer.validated_data['token']

        password_reset_token_validation_time = get_password_reset_token_expiry_time()
        # find token
        reset_password_token = ResetPasswordToken.objects.filter(key=token).first()
        if reset_password_token is None:
            return Response({'status': 'Token not found.'}, status=status.HTTP_404_NOT_FOUND)
        # check expiry date
        expiry_date = reset_password_token.created_at + timedelta(hours=password_reset_token_validation_time)
        if timezone.now() > expiry_date:
            # delete expired token
            reset_password_token.delete()
            return Response({'status': 'Token expired'}, status=status.HTTP_404_NOT_FOUND)

        # get password validation
        if password != password2:
            return Response({'status': 'Password mismatch'}, status=status.HTTP_404_NOT_FOUND)

        try:
            # validate the password against existing validators
            validate_password(
                password,
                user=reset_password_token.user,
                password_validators=get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)
            )
        except exceptions.ValidationError as e:
            # raise a validation error for the serializer
            raise exceptions.ValidationError({
                'password': e
            })

        reset_password_token.user.set_password(password)
        reset_password_token.user.save()
        post_password_reset.send(sender=self.__class__, user=reset_password_token.user)

        # Delete all password reset tokens for this user
        ResetPasswordToken.objects.filter(user=reset_password_token.user).delete()

        return Response({'status': 'Password reset successfully'})


class IsAllowedRole(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == 'MENTOR':
                return True
            elif request.user.role == 'BRANCH_MANAGER':
                return True
            elif request.user.role == 'COMPANY_ADMIN':
                return True
        return False
    
class AdminLoginView(APIView):
    permission_classes = [IsAllowedRole]

class CompanyAdminViewSet(APIView):
    permission_classes = [IsAllowedRole]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.company.id)

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from.models import Company, Branch, CustomUser
from.serializers import CompanySerializer, BranchSerializer, CustomUserSerializer

class CompanyList(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyDetail(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class BranchList(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class BranchDetail(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class CustomUserList(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CustomUserDetail(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CompanyBranchList(APIView):
    permission_classes = [AllowAny]
    def get(self, request, company_id):
        company = Company.objects.get(id=company_id)
        branches = Branch.objects.filter(company=company)
        serializer = BranchSerializer(branches, many=True)
        return Response(serializer.data)


class BranchUsersList(APIView):
    permission_classes = [AllowAny]
    def get(self, request, branch_id):
        branch = Branch.objects.get(id=branch_id)
        users = CustomUser.objects.filter(branch=branch)
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
        