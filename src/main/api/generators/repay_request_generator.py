import random

from src.main.api.models.repay_credit_request import RepayCreditRequest


class RepayCreditRequestGenerator:

    @staticmethod
    def valid(credit_id: int, account_id: int, amount: float) -> RepayCreditRequest:
        return RepayCreditRequest(
            creditId=credit_id,
            accountId=account_id,
            amount=amount
        )

    @staticmethod
    def invalid_min_amount(credit_id: int, account_id: int) -> RepayCreditRequest:
        return RepayCreditRequest(
            creditId=credit_id,
            accountId=account_id,
            amount=4999
        )

    @staticmethod
    def invalid_max_amount(credit_id: int, account_id: int) -> RepayCreditRequest:
        return RepayCreditRequest(
            creditId=credit_id,
            accountId=account_id,
            amount=15001
        )