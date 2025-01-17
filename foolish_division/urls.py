"""foolish_division URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views

from foolish_division.expense_auth.views import UserAuthenticationViewSet
from foolish_division.expenses.views import ExpenseGroupViewset, ExpenseViewset, StatusViewset
from foolish_division.profiles.views import UserExpenseProfileViewset, ContactedExpenseProfileViewset

router = routers.DefaultRouter()
router.register(r'eauth', UserAuthenticationViewSet, 'eauth')
router.register(r'groups', ExpenseGroupViewset, 'groups')
router.register(r'expenses', ExpenseViewset, 'expenses')
router.register(r'status', StatusViewset, 'status'),
router.register(r'profiles', UserExpenseProfileViewset, 'profiles')
router.register(r'friends', ContactedExpenseProfileViewset, 'friends')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("__reload__/", include("django_browser_reload.urls")),
    path('token-expense_auth/', views.obtain_auth_token)
]
