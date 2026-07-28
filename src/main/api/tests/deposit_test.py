import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.db.crud.account_crud import AccountCrudDb

@pytest.mark.api
class TestDeposit:
    def test_deposit(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, create_account_response: CreateAccountResponse):
        deposit_request = DepositRequest(
            accountId=create_account_response.id,
            amount=1000
        )

        response = api_manager.user_steps.deposit(
            create_user_request,
            deposit_request
        )

        account =  AccountCrudDb.get_account_by_id(
            db_session,
            create_account_response.id
        )

        transaction = TransactionCrudDb.get_last_transaction_by_account_id(
            db_session,
            create_account_response.id
        )

        assert response.balance == deposit_request.amount
        assert account.balance == deposit_request.amount
        assert account.balance == response.balance

        assert transaction.to_account_id == create_account_response.id
        assert transaction.from_account_id is None
        assert transaction.credit_id is None
        assert transaction.amount == deposit_request.amount
        assert transaction.transaction_type == "deposit"
        assert transaction is not None, 'Проведенной транзакции нет в БД!'

    def test_deposit_invalid_amount(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, create_account_response: CreateAccountResponse):
        deposit_request = DepositRequest(
            accountId=create_account_response.id,
            amount=228
        )

        account_before = AccountCrudDb.get_account_by_id(
            db_session,
            create_account_response.id
        )

        transaction_before = TransactionCrudDb.get_last_transaction_by_account_id(
            db_session,
            create_account_response.id
        )

        api_manager.user_steps.deposit_invalid(
            create_user_request,
            deposit_request
        )

        account_after = AccountCrudDb.get_account_by_id(
            db_session,
            create_account_response.id
        )

        transaction_after = TransactionCrudDb.get_last_transaction_by_account_id(
            db_session,
            create_account_response.id
        )

        assert account_after.balance == account_before.balance

        #assert transaction_before is None, 'Транзакция есть в БД, ошибка!'
        assert transaction_after is None, 'Транзакция есть в БД, ошибка!'