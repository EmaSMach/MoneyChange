from decimal import Decimal
from django.db import models
from django.conf import settings
# Create your models here.


class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  related_name='accounts', on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=Decimal("00.00"))

    def can_withdraw(self, amount):
        if self.balance - Decimal(amount) >= 0:
            return True
        return False

    def withdraw(self, amount):
        if self.can_withdraw(amount):
            self.balance -= Decimal(amount)
            self.save()
            return True
        return False

    def get_balance(self):
        return self.balance

    def deposit(self, amount):
        self.balance += Decimal(amount)
        self.save()

    def __str__(self) -> str:
        return f"Account(id={self.id}, user={self.user})"



class Transaction(models.Model):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"
    CHOICES = (
        (DEPOSIT, "Deposit"),
        (WITHDRAW, "Withdraw"),
    )
    operation = models.CharField(choices=CHOICES, max_length=15, default=DEPOSIT)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.0"))
    account = models.ForeignKey(Account, blank=False, null=False, related_name="transactions", on_delete=models.CASCADE)

    def execute_transaction(self):
        if self.operation == self.DEPOSIT:
            result = self.account.deposit(self.amount)
        elif self.operation == self.WITHDRAW:
            result = self.account.withdraw(self.amount)
        else:
            result = None
        return result

    def __str__(self) -> str:
        return f"Transaction({self.id}, operation={self.operation}, amount={self.amount}, account={self.account}"
