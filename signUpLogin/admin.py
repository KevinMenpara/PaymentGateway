from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
import csv
from django.core.mail import send_mail
from signUpLogin.models import User, UserPDF
from decouple import config

class UserPDFInline(admin.TabularInline):
    model = UserPDF
    extra = 0  # No extra forms for adding new PDFs
    readonly_fields = ('pdf_file_path',)  # Make fields read-only

    def has_add_permission(self, request, obj=None):
        return False  # Disable adding new PDF files

    def has_change_permission(self, request, obj=None):
        return False  # Disable editing existing PDF files

    def has_delete_permission(self, request, obj=None):
        return False  # Disable deleting PDF files

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'dob', 'expiry', 'ammount', 'created_at', 'updated_at', 'active')
    search_fields = ('name', 'email', 'dob', 'ammount')
    list_editable = ('ammount',)
    actions = ['reset_passwords', 'mark_as_inactive', 'mark_as_active', 'export_as_csv']
    inlines = [UserPDFInline]  # Add UserPDFInline to UserAdmin

    def reset_passwords(self, request, queryset):
        """Action to reset passwords for selected users."""
        for user in queryset:
            user.set_password('new_password')  # Use a secure method for password generation
            user.save()
            send_mail(
                'Password Reset',
                'Your password has been reset. Please contact admin for further instructions.',
                config('EMAIL_HOST_USER'),
                [user.email],
                fail_silently=False,
            )
        self.message_user(request, _("Passwords have been reset for selected users."))

    reset_passwords.short_description = "Reset passwords for selected users"

    def mark_as_inactive(self, request, queryset):
        """Action to mark selected users as inactive."""
        queryset.update(active=False)
        self.message_user(request, _("Selected users have been marked as inactive."))

    mark_as_inactive.short_description = "Mark selected users as inactive"

    def mark_as_active(self, request, queryset):
        """Action to mark selected users as active."""
        queryset.update(active=True)
        self.message_user(request, _("Selected users have been marked as active."))

    mark_as_active.short_description = "Mark selected users as active"

    def export_as_csv(self, request, queryset):
        """Action to export selected users as a CSV file."""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users.csv"'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'DOB', 'Expiry', 'Amount', 'Created At', 'Updated At'])

        for user in queryset:
            writer.writerow([user.name, user.email, user.dob, user.expiry, user.ammount, user.created_at, user.updated_at])

        return response

    def get_queryset(self, request):
        """Override the default queryset to show all users by default."""
        qs = super().get_queryset(request)
        if request.session.get('show_active_users', False):
            return qs.filter(active=True)  # Show only active users
        return qs  # Show all users

    def get_urls(self):
        """Add custom URLs for showing active and all users."""
        urls = super().get_urls()
        custom_urls = [
            path('show-active-users/', self.admin_site.admin_view(self.show_active_users), name='show_active_users'),
            path('show-all-users/', self.admin_site.admin_view(self.show_all_users), name='show_all_users'),
        ]
        return custom_urls + urls

    def show_active_users(self, request):
        """Action to show only active users."""
        request.session['show_active_users'] = True
        self.message_user(request, _("Showing only active users."))
        return redirect('..')  # Redirect to the changelist view

    def show_all_users(self, request):
        """Action to show all users."""
        request.session['show_active_users'] = False
        self.message_user(request, _("Showing all users."))
        return redirect('..')  # Redirect to the changelist view

    def changelist_view(self, request, extra_context=None):
        """Override changelist view to add the 'Show Active Users' and 'Show All Users' buttons."""
        extra_context = extra_context or {}
        extra_context['show_active_users'] = request.session.get('show_active_users', False)
        return super().changelist_view(request, extra_context=extra_context)
