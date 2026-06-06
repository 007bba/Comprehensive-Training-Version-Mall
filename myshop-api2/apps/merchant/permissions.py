from rest_framework import permissions


class IsMerchant(permissions.BasePermission):
    """仅允许商家角色访问"""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 1
        )


class IsShopOwner(permissions.BasePermission):
    """仅允许店铺所属商家操作"""

    def has_object_permission(self, request, view, obj):
        return obj.merchant == request.user
