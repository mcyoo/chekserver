from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    # password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("token", "user_os", "user_ver")

    # read_only_fields = ("id", "superhost", "avatar")

    def validate_token(self, value):
        if len(value) < 150:
            raise serializers.ValidationError("invaild token")
        return value

    def create(self, validated_data):
        token = validated_data.get("token")
        try:
            user = User.objects.get(token=token)
        except User.DoesNotExist:
            # to do vaild token
            user = super().create(validated_data)
            user.save()
        return user
