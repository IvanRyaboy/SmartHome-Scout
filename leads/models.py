from django.contrib.auth import get_user_model
from django.db import models


class Lead(models.Model):
    """Contact request / lead for a listing (sale or rent)."""
    class ListingType(models.TextChoices):
        SALE = 'sale', 'Sale'
        RENT = 'rent', 'Rent'

    class Status(models.TextChoices):
        NEW = 'new', 'New'
        CONTACTED = 'contacted', 'Contacted'
        CLOSED = 'closed', 'Closed'

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='leads'
    )
    apartment = models.ForeignKey(
        'apartments.Apartment',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='leads'
    )
    rent = models.ForeignKey(
        'rent.Rent',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='leads'
    )
    listing_type = models.CharField(
        max_length=10,
        choices=ListingType.choices
    )
    contact_info = models.TextField(blank=True)
    message = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'leads_lead'
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(apartment__isnull=False, rent__isnull=True)
                    | models.Q(apartment__isnull=True, rent__isnull=False)
                ),
                name='lead_one_of_apartment_rent',
            )
        ]

    def __str__(self):
        return f"Lead #{self.pk} ({self.listing_type}) by {self.user_id}"
