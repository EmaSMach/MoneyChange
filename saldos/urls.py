from django.urls import path

from . import views


urlpatterns = [
    path("account/<int:account_id>/", views.operations, name="operations"),
]
