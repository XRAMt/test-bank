import random

from src.main.api.models.deposit_request import DepositRequest


class DepositRequestGenerator:

    @staticmethod
    def valid(account_id: int) -> DepositRequest:
        return DepositRequest(
            accountId=account_id,
            amount=random.randint(1000, 8000)
        )

    @staticmethod
    def invalid_min_amount(account_id: int) -> DepositRequest:
        return DepositRequest(
            accountId=account_id,
            amount=999
        )

