from django.urls import path
from .views import RegisterView, Bonds, SellBond, BondPrice
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="register"),
    path("add-bond/", Bonds.as_view(), name="add_bond"),
    path("bonds/<int:bond_id>", SellBond.as_view(), name="sell_bond"),
    path("usd-rate/", BondPrice.as_view(), name="bond_price"),
]
