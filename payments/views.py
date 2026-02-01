from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from .db_utils import execute_query
import uuid
import random

def process_payment_gateway(amount, currency):
    """
    Simulate payment gateway processing.
    Returns transaction_id if success, None if failed.
    """
    # Simulate failure for amounts ending in .99
    if str(amount).endswith('.99'):
        return None
    return str(uuid.uuid4())

class CreatePaymentView(APIView):
    def get(self, request):
        """List all payments"""
        payments = execute_query("SELECT * FROM payments ORDER BY id DESC", fetch_all=True)
        return Response(payments)

    def post(self, request):
        order_id = request.data.get('order_id')
        amount = request.data.get('amount')
        currency = request.data.get('currency', 'USD')
        idempotency_key = request.data.get('idempotency_key')

        if not all([order_id, amount, idempotency_key]):
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        # Check idempotency
        existing_payment = execute_query(
            "SELECT * FROM payments WHERE idempotency_key = %s",
            [idempotency_key],
            fetch_one=True
        )
        if existing_payment:
            return Response(existing_payment, status=status.HTTP_200_OK)

        # Check for duplicate successful payment for order
        successful_payment = execute_query(
            "SELECT * FROM payments WHERE order_id = %s AND status = 'success'",
            [order_id],
            fetch_one=True
        )
        if successful_payment:
             return Response({"error": "Order already paid"}, status=status.HTTP_400_BAD_REQUEST)

        # Insert pending payment
        transaction_id = process_payment_gateway(amount, currency)
        payment_status = 'success' if transaction_id else 'failed'
        
        # MySQL doesn't support RETURNING, so we insert and then select
        query = """
            INSERT INTO payments (order_id, amount, currency, status, transaction_id, idempotency_key)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        try:
            execute_query(
                query, 
                [order_id, amount, currency, payment_status, transaction_id, idempotency_key]
            )
            
            # Fetch the created payment
            payment = execute_query(
                "SELECT * FROM payments WHERE idempotency_key = %s",
                [idempotency_key],
                fetch_one=True
            )
            return Response(payment, status=status.HTTP_201_CREATED)
            
        except IntegrityError:
            # Handle race condition: Valid idempotency key might have been inserted by another thread
            existing_payment = execute_query(
                "SELECT * FROM payments WHERE idempotency_key = %s",
                [idempotency_key],
                fetch_one=True
            )
            if existing_payment:
                 return Response(existing_payment, status=status.HTTP_200_OK)
            
            # If not idempotency conflict (e.g. transaction_id or other), re-raise or return error
            return Response({"error": "Integrity Error: processing payment failed"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PaymentDetailView(APIView):
    def get(self, request, pk):
        payment = execute_query(
            "SELECT * FROM payments WHERE id = %s",
            [pk],
            fetch_one=True
        )
        if not payment:
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(payment)

    def patch(self, request, pk):
        """
        Update payment status (e.g. for webhook updates or manual overrides)
        """
        new_status = request.data.get('status')
        if not new_status:
             return Response({"error": "Status is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verify payment exists
        payment = execute_query("SELECT * FROM payments WHERE id = %s", [pk], fetch_one=True)
        if not payment:
             return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)

        # Update status
        execute_query(
            "UPDATE payments SET status = %s WHERE id = %s",
            [new_status, pk]
        )
        
        updated_payment = execute_query("SELECT * FROM payments WHERE id = %s", [pk], fetch_one=True)
        return Response(updated_payment)

class OrderPaymentsView(APIView):
    def get(self, request, order_id):
        payments = execute_query(
            "SELECT * FROM payments WHERE order_id = %s",
            [order_id],
            fetch_all=True
        )
        return Response(payments)

class RefundPaymentView(APIView):
    def post(self, request, pk):
        payment = execute_query(
            "SELECT * FROM payments WHERE id = %s",
            [pk],
            fetch_one=True
        )
        if not payment:
             return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if payment['status'] != 'success':
            return Response({"error": "Payment cannot be refunded"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update status to refunded
        execute_query(
            "UPDATE payments SET status = 'refunded' WHERE id = %s",
            [pk]
        )
        
        updated_payment = execute_query(
            "SELECT * FROM payments WHERE id = %s",
            [pk],
            fetch_one=True
        )
        return Response(updated_payment)
