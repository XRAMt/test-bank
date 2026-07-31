import random
from src.main.api.models.transfer_request import TransferRequest


class TransferRequestGenerator:

    @staticmethod
    def valid(from_account_id: int, to_account_id: int, max_amount: float) -> TransferRequest:
        return TransferRequest(
            fromAccountId=from_account_id,
            toAccountId=to_account_id,
            amount=random.randint(500, int(min(max_amount, 10000)))
        )

    @staticmethod
    def invalid_min_amount(from_account_id: int, to_account_id: int) -> TransferRequest:
        return TransferRequest(
            fromAccountId=from_account_id,
            toAccountId=to_account_id,
            amount=random.randint(1, 499)
        )