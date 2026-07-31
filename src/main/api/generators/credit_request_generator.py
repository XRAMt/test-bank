import random
from src.main.api.models.credit_request import CreditRequest


class CreditRequestGenerator:

    @staticmethod
    def valid(account_id: int) -> CreditRequest:
        return CreditRequest(
            accountId=account_id,
            amount=random.randint(5000, 10000),
            termMonths=random.choice([6, 12, 24, 36])
        )

    @staticmethod
    def invalid_min_amount(account_id: int) -> CreditRequest:
        return CreditRequest(
            accountId=account_id,
            amount=4999,
            termMonths=12
        )

    @staticmethod
    def invalid_max_amount(account_id: int) -> CreditRequest:
        return CreditRequest(
            accountId=account_id,
            amount=15001,
            termMonths=12
        )
