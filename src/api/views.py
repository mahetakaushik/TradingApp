from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from django.contrib.auth.models import User
from .models import Bond
from .serializers import RegisterSerializer, BondSerializer, BondPriceSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
import requests
from django.db.models import F


class RegisterView(generics.CreateAPIView):
    """
    Register View

    This View allows to register new user into system

    Required Fields:
    1. username -- unique username (Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.)
    2. email -- email of user
    3. password -- user password
    """

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class Bonds(APIView):
    """
    Bond View

    This view allows to list all bonds and add/create new bond.
    user authntication is required for access this apis
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        To get all Bonds list.
        """
        bonds = Bond.objects.all()
        serializer_class = BondSerializer(bonds, many=True)
        return Response(serializer_class.data, status=HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        To add new bond.

        Required Fields:
        1. bond_type -- Type of bond
        2. no_of_bonds -- Number of bonds for sell
        3. selling_price -- Selling price of bond in Mexican Pesos (MXN).
        """
        data = request.data
        bond_type = data.get("bond_type")
        no_of_bonds = data.get("no_of_bonds")
        selling_price = data.get("selling_price")

        if (not bond_type) or (not no_of_bonds) or (not selling_price):
            return Response(
                {"Error": "Please provide all required details of Bond"},
                status=HTTP_400_BAD_REQUEST,
            )

        bond_data = {
            "bond_type": bond_type,
            "no_of_bonds": no_of_bonds,
            "selling_price": selling_price,
            "status": "available",
            "seller": request.user.id,
        }

        serializer = BondSerializer(data=bond_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class SellBond(APIView):
    """
    Sell Bond View

    This view allows user to buy bonds.
    user authntication is required for access this apis
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, bond_id):
        try:
            return Bond.objects.get(bond_id=bond_id)
        except Bond.DoesNotExist:
            return None

    def get(self, request, bond_id, *args, **kwargs):
        """
        To get Bond using bond_id.
        """
        bond = self.get_object(bond_id=bond_id)
        if not bond:
            return Response(
                {"Error": "Bond with given id does not exist"},
                status=HTTP_400_BAD_REQUEST,
            )
        serializer = BondSerializer(bond)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, bond_id, *args, **kwargs):
        """
        To Buy/Purchase bond.

        Conditions:
        - Seller can not buy theier own bonds
        - Only available bonds can be purchased
        """
        bond = self.get_object(bond_id=bond_id)
        if not bond:
            return Response(
                {"Error": "Bond with given id does not exist"},
                status=HTTP_400_BAD_REQUEST,
            )
        if bond.status == "purchased":
            return Response(
                {"Error": "Can not Purchase, Bond is already Sold"},
                status=HTTP_400_BAD_REQUEST,
            )
        if bond.seller == request.user:
            return Response(
                {"Error": "You can not purchase your own Bonds."},
                status=HTTP_400_BAD_REQUEST,
            )
        data = {"status": "purchased", "buyer": request.user.id}
        serializer = BondSerializer(instance=bond, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class BondPrice(APIView):
    """
    Get Bond Price in USD

    This view allows user to get bonds price in USD.
    user authntication is required for access this apis
    """

    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        """
        To update bond price in USD using the most recent exchange rate published by Banco de México.
        """
        url = "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno?locale=en"
        headers = {
            "Bmx-Token": "8221d8893a08d870c69a896598a66f7c7b4b745001a22defa83a325dcf252147",
            "Content-Type": "application/json",
        }
        res = requests.get(url, headers=headers)
        response = res.json()
        usd_rate = response.get("bmx").get("series")[0].get("datos")[0].get("dato")
        Bond.objects.update(price_in_usd=F("selling_price") / usd_rate)
        bonds = Bond.objects.all()
        serializer = BondPriceSerializer(bonds, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
