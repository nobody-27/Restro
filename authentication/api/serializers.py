from rest_framework import serializers
from authentication.models import User
from django.contrib.auth.hashers import make_password



class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("This field is required.")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        # Remove the confirm_password field since it's not needed for the user creation
        validated_data.pop('confirm_password')
        # Hash password before creating the user
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "confirm_password",
            "first_name",
            "last_name",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "first_name": {"required": False},  # Make first_name optional
            "last_name": {"required": False},  # Make last_name optional
        }
