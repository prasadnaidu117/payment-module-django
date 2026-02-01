from django.urls import path
from .views import CreatePaymentView, PaymentDetailView, OrderPaymentsView, RefundPaymentView

urlpatterns = [
    path('payments/', CreatePaymentView.as_view(), name='create-payment'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
    path('payments/order/<str:order_id>/', OrderPaymentsView.as_view(), name='order-payments'),
    path('payments/<int:pk>/refund/', RefundPaymentView.as_view(), name='refund-payment'),
]
