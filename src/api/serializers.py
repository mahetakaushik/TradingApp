from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import Bond


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]


class RegisterSerializer(serializers.ModelSerializer):
    """
    RegisterSerializer is a model serializer which includes the
    attributes that are required for registering a user.
    """

    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
        )

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class BondSerializer(serializers.ModelSerializer):
    """
    BondSerializer is a model serializer which shows the attributes
    of a Bonds.
    """

    class Meta:
        model = Bond
        fields = [
            "bond_id",
            "bond_type",
            "no_of_bonds",
            "selling_price",
            "seller",
            "status",
            "buyer",
        ]


class BondPriceSerializer(serializers.ModelSerializer):
    """
    BondPriceSerializer is a model serializer which shows the attributes
    of a Bonds with USD rates.
    """

    class Meta:
        model = Bond
        fields = [
            "bond_id",
            "bond_type",
            "no_of_bonds",
            "selling_price",
            "seller",
            "status",
            "price_in_usd",
        ]
