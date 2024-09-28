# admin.py
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Payment


# Custom Payment Resource for Import/Export
class PaymentResource(resources.ModelResource):
    class Meta:
        model = Payment
        fields = ('user__username', 'amount', 'job__title', 'email', 'phone', 'ref', 'verified', 'payment_date')  # Customize the fields to be exported

    def dehydrate_user(self, payment):
        # Return the username for the user field
        return payment.user.username if payment.user else 'Anonymous'

    def dehydrate_verified(self, payment):
        # Return "Verified" or "Unverified" instead of 1/0
        return 'Verified' if payment.verified else 'Unverified'


# Customizing the Payment model admin interface with import/export functionality
class PaymentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = PaymentResource  # Use the custom resource
    list_display = ('user', 'amount', 'job', 'email', 'phone', 'ref', 'verified', 'payment_date')  # Fields to display in the list view
    list_filter = ('verified', 'payment_date')  # Filters for the admin panel
    search_fields = ('user__username', 'email', 'phone', 'ref')  # Search fields
    readonly_fields = ('ref', 'payment_date')  # Make these fields read-only
    list_editable = ('verified',)  # Allow inline editing of 'verified' status


# Registering the Payment model with the customized admin
admin.site.register(Payment, PaymentAdmin)
