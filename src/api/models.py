from django.db import models
from django.contrib.auth.models import User
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MinLengthValidator,
)

BOND_PURCHASE_CHOICES = [("available", "AVAILABLE"), ("purchased", "PURCHASED")]


class Bond(models.Model):

    bond_id = models.AutoField(primary_key=True)
    bond_type = models.CharField(
        validators=[MinLengthValidator(3)], max_length=40, blank=False, null=False
    )
    no_of_bonds = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10000)],
        blank=False,
        null=False,
    )
    selling_price = models.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(100000000)],
        decimal_places=4,
        max_digits=13,
        blank=False,
        null=False,
    )
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    status = models.CharField(
        default="available",
        choices=BOND_PURCHASE_CHOICES,
        max_length=10,
        blank=False,
        null=True,
    )
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="buyer", blank=True, null=True
    )
    price_in_usd = models.DecimalField(
        decimal_places=4, max_digits=10, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    ordered_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.bond_type, self.seller)
