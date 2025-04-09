from django.contrib import admin
from django.urls import path
from myapp.views import ProcessReceiptsView, GetReceiptPointsView

urlpatterns = [
    path('receipts/process', ProcessReceiptsView.as_view()),
    path('receipts/<str:receipt_id>/points', GetReceiptPointsView.as_view())
]
