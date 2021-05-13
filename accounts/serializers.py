from random import randint

from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from allauth.account.adapter import get_adapter
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken

from .fields import CustomPhoneNumberField
from .exceptions import NonUniqueEmailException, NonUniquePhoneNumberException
from .models import Profile, Setting


User = get_user_model()


class LoginSerializer(serializers.Serializer):
    """
    Custom serializer to log users with phone number or email
    and password.
    """
    username = serializers.CharField(help_text='Phone number or email')
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            err_message = _('Wrong username or password.')
            raise serializers.ValidationError(err_message)

        if not user.is_active:
            err_message = _('User account is disabled.')
            raise serializers.ValidationError(err_message)

        validated_data['user'] = user
        return validated_data


class ValidEmailSerialzier(serializers.Serializer):
    """
    Check email address for valid email format and non-duplication.
    """
    email = serializers.EmailField()

    def validate_email(self, value):
        queryset = User.objects.filter(email=value)
        if queryset.exists():
            raise NonUniqueEmailException()
        return value


class ValidPhoneNumberSerialzier(serializers.Serializer):
    """
    Check phone number for valid phone number format and non-duplication.
    """
    phone_number = CustomPhoneNumberField()
    otp = serializers.SerializerMethodField()

    def validate_phone_number(self, value):
        queryset = User.objects.filter(phone_number=value)
        if queryset.exists():
            raise NonUniquePhoneNumberException()
        return value

    def get_otp(self, obj):
        """
        Returns an 6-digit OTP (One-Time Password) code.
        """
        return randint(100000, 999999)


class NestedProfileSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for the user profile model to be nested
    is user detail serializers.
    """
    user = serializers.ReadOnlyField(
        source='user.full_name',
        help_text=_('User\'s full name')
    )

    class Meta:
        model = Profile
        fields = '__all__'
        ref_name = 'Profile'


class NestedSettingSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for the user setting model to be nested
    is user detail serializers.
    """
    user = serializers.ReadOnlyField(
        source='user.full_name',
        help_text=_('User\'s full name')
    )

    class Meta:
        model = Setting
        fields = '__all__'
        ref_name = 'Settings'


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registrating new users.
    """
    first_name = serializers.CharField(max_length=100, write_only=True)
    last_name = serializers.CharField(max_length=100, write_only=True)
    password = serializers.CharField(
        max_length=120,
        write_only=True,
        style={'input_type': 'password'}
    )
    phone_number = CustomPhoneNumberField(
        required=True,
        error_messages={
            'invalid': _('Enter a valid phone number.')
        }
    )
    is_active = serializers.BooleanField(read_only=True)
    tokens = serializers.SerializerMethodField()
    profile = NestedProfileSerializer(read_only=True)
    settings = NestedSettingSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'phone_number', 'email', 'password',
            'first_name', 'last_name', 'is_active',
            'tokens', 'profile', 'settings'
        )

    def validate_password(self, password):
        return get_adapter().clean_password(password)

    def validate_phone_number(self, value):
        """
        Validate phone number is unique.
        """
        if User.objects.filter(phone_number=value).exists():
            err_message = _('user with this phone number already exists.')
            raise serializers.ValidationError(err_message)
        return value

    def get_tokens(self, obj):
        jwt = RefreshToken.for_user(obj)
        return {
            'refresh': str(jwt),
            'access': str(jwt.access_token)
        }

    def create(self, validated_data):
        raw_password = validated_data.pop('password')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')

        # User Object
        user = User(
            phone_number=validated_data['phone_number'],
            email=validated_data.get('email')
        )
        user.set_password(raw_password)
        user.save()

        # User Profile
        user.profile.first_name = first_name
        user.profile.last_name = last_name
        user.profile.save()

        return user


class TokenResponseSerializer(serializers.Serializer):
    """
    A read-only representation of the token response for including
    in the API documentation.
    """
    access = serializers.ReadOnlyField()
    refresh = serializers.ReadOnlyField()


class UserResponseSerializer(UserRegistrationSerializer):
    """
    Read-only representation of the `User` model in a successful response.
    """
    tokens = TokenResponseSerializer(read_only=True)
    profile = NestedProfileSerializer(read_only=True)
    settings = NestedSettingSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'phone_number', 'email', 'is_active', 'tokens',
            'profile', 'settings'
        )


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for a User model serializer.
    """
    email = serializers.EmailField()
    profile = NestedProfileSerializer(
        read_only=True,
        help_text=_('A read-only representation of the user profile.')
    )
    settings = NestedSettingSerializer(
        read_only=True,
        help_text=_('A read-only representation of the user profile.')
    )

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'email', 'is_active', 'profile', 'settings')
        read_only_fields = ('phone_number', )

    def validate_email(self, value):
        """
        Check if email is unique or raise `409 Conflict` error.
        """
        queryset = User.objects.filter(email=value)
        if queryset.exists():
            raise NonUniqueEmailException()
        return value



class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for changing user password.
    """
    current_password = serializers.CharField(
        max_length=120, write_only=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        max_length=120, write_only=True,
        style={'input_type': 'password'}
    )

    def validate_current_password(self, value, *args, **kwargs):
        user = self.context.get('user')
        if not user.check_password(value):
            err_message = _('Wrong current password.')
            raise serializers.ValidationError(err_message)
        return value

    def validate_new_password(self, value, *args, **kwargs):
        user = self.context.get('user')
        try:
            validate_password(value, user=user)
            return value
        except ValidationError as e:
            raise

    def save(self, *args, **kwargs):
        user = self.context.get('user')
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()


class TokenVerifySerializer(serializers.Serializer):
    """
    Serializer for verifying access tokens.

    This serializer is adapation of the `TokenVerifySerializer` from
    the `django-rest-simplejwt` library.
    """
    token = serializers.CharField()

    def validate(self, attrs):
        UntypedToken(attrs['token'])
        return {'detail': _('Token is valid')}
