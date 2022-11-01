from decimal import Decimal
import json

from django.shortcuts import render
from django.http import JsonResponse
from .models import Account, Transaction
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def operations(request, account_id):
    account = Account.objects.filter(id=account_id)
    if not account.exists():
        return JsonResponse({
            "error": {
                "message": f"Account with ID {account_id} not found.",
            }
        })
    account = account.first()
    if request.method == 'GET':
        data = {
            "details": {
                "owner": {
                    "user": account.user.username,
                    "first_name": account.user.first_name,
                    "last_name": account.user.last_name,
                },
                "balance": account.balance
            }
        }
    elif request.method == "POST":
        json_arguments = json.loads(request.body)
        operation = json_arguments.get("operation")
        amount = json_arguments.get("amount")

        if not amount and operation:
            if Decimal(amount) < 0:
                data = {
                    "error": "Invalid arguments",
                }
        amount = Decimal(amount)
        if operation == "deposit":
            transaction = Transaction.objects.create(
                account=account,
                amount=amount,
                operation=operation.upper(),
            )
            transaction.execute_transaction()
            # account.deposit(amount)  # podría usar directamente este método
            data = {
                "success": True,
                "detail": {
                    "operation_type": operation,
                    "amount": amount,
                    "balance": account.balance
                }
            }
        elif operation == "withdraw":
            transaction = Transaction.objects.create(
                account=account,
                amount=amount,
                operation=operation.upper(),
            )
            success = transaction.execute_transaction()
            # success = account.withdraw(amount)  # o este método
            if success:
                data = {
                    "success": True,
                    "detail": {
                        "operation_type": operation,
                        "amount": amount,
                        "balance": account.balance
                    }
                }
            else:
                data = {
                    "success": False,
                    "error": {
                        "message": "No se pudo realizar la operación"
                    }
                }
        else:
            data = {
                "error": {
                    "message": "Operación inválida"
                }
            }
    return JsonResponse(data)
