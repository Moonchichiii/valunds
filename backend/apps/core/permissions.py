"""
Custom DRF permissions for role-based access control.
"""

from rest_framework import permissions

from apps.core.choices import UserRole


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission: allow owners or staff to edit.

    Requires the object to have a 'user' field (FK to User).
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions allowed to anyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for owner or staff
        return obj.user == request.user or request.user.is_staff


class IsOrgAdmin(permissions.BasePermission):
    """
    Object-level permission: only org owners/admins can edit.

    Requires the object to have an 'organization' field.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions allowed to anyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if user owns the organization
        if hasattr(obj, "organization"):
            return obj.organization.owner == request.user or request.user.is_staff
        elif hasattr(obj, "owner"):
            return obj.owner == request.user or request.user.is_staff

        return False


class IsEmployer(permissions.BasePermission):
    """
    View-level permission: only employers can access.

    Used for job posting, viewing applications, etc.
    """

    message = "Only employers can access this resource."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, "role")
            and request.user.role == UserRole.EMPLOYER
        )


class IsJobSeeker(permissions.BasePermission):
    """
    View-level permission: only job seekers can access.

    Used for applying to jobs, building CVs, etc.
    """

    message = "Only job seekers can access this resource."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, "role")
            and request.user.role == UserRole.JOB_SEEKER
        )


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    View-level permission: staff can write, others read-only.

    Used for analytics, moderation queues, etc.
    """

    message = "Only staff can modify this resource."

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            request.user.is_authenticated
            and hasattr(request.user, "role")
            and request.user.role == UserRole.STAFF
        )


class IsOwnerOrStaff(permissions.BasePermission):
    """
    Object-level permission: owner or staff can edit.

    Generic version for any model with a 'user' field.
    """

    def has_object_permission(self, request, view, obj):
        # Read allowed for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        # Write for owner or staff
        return obj.user == request.user or (
            hasattr(request.user, "role") and request.user.role == UserRole.STAFF
        )
