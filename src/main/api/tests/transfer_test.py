import pytest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.transfer_request import TransferRequest

@pytest.mark.api
class TestTransfer:
    def test_transfer(self, api_manager, create_user_request, create_accounts_response):
        from_account, to_account = create_accounts_response
        deposit_request = DepositRequest(
            accountId=from_account.id,
            amount=1000
        )

        api_manager.user_steps.deposit(
            create_user_request,
            deposit_request
        )

        transfer_request = TransferRequest(
            fromAccountId=from_account.id,
            toAccountId=to_account.id,
            amount=500
        )

        response = api_manager.user_steps.transfer(
            create_user_request,
            transfer_request
        )

        assert response.fromAccountId == from_account.id
        assert response.toAccountId == to_account.id
        assert response.fromAccountIdBalance == 500

    def test_transfer_invalid_amount(self, api_manager, create_user_request, create_accounts_response):
        from_account, to_account = create_accounts_response
        deposit_request = DepositRequest(
            accountId=from_account.id,
            amount=1000
        )

        api_manager.user_steps.deposit(
            create_user_request,
            deposit_request
        )

        transfer_request = TransferRequest(
            fromAccountId=from_account.id,
            toAccountId=to_account.id,
            amount=228
        )

        api_manager.user_steps.transfer_invalid(
            create_user_request,
            transfer_request
        )





