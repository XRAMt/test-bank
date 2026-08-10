import pytest

from src.main.api.generators.transfer_request_generator import TransferRequestGenerator
from src.main.api.db.steps.db_steps import DbSteps

@pytest.mark.api
class TestTransfer:

    def test_transfer(self, api_manager, db_session, create_user_request, create_funded_accounts):
        from_account, to_account, balance = create_funded_accounts

        transfer_request = TransferRequestGenerator.valid(
            from_account.id,
            to_account.id,
            balance
        )

        response = api_manager.user_steps.transfer(
            create_user_request,
            transfer_request
        )

        assert response.fromAccountId == from_account.id, \
            "ID счета отправителя должен совпадать!"

        assert response.toAccountId == to_account.id, \
            "ID счета получателя должен совпадать!"

        db_steps = DbSteps(db_session)

        db_steps.assert_transfer_transaction_created(
            transfer_request
        )

        from_account_db = db_steps.get_account(from_account.id)
        to_account_db = db_steps.get_account(to_account.id)

        assert from_account_db.balance == response.fromAccountIdBalance, \
            "Баланс счета отправителя в БД должен совпадать с ответом API"

        assert to_account_db.balance == transfer_request.amount, \
            "Баланс счета получателя в БД должен совпадать с суммой перевода"

    def test_transfer_invalid_amount(self, api_manager, db_session, create_user_request, create_funded_accounts):
        from_account, to_account, balance = create_funded_accounts

        db_steps = DbSteps(db_session)

        from_before = db_steps.get_account(from_account.id)
        to_before = db_steps.get_account(to_account.id)

        transfer_request = TransferRequestGenerator.invalid_min_amount(
            from_account.id,
            to_account.id
        )

        api_manager.user_steps.transfer_invalid(
            create_user_request,
            transfer_request
        )

        from_after = db_steps.get_account(from_account.id)
        to_after = db_steps.get_account(to_account.id)

        assert from_after.balance == from_before.balance, \
            "Баланс счета отправителя не должен измениться"

        assert to_after.balance == to_before.balance, \
            "Баланс счета получателя не должен измениться"





