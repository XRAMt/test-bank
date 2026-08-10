import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.steps.db_steps import DbSteps
from src.main.api.generators.deposit_request_generator import DepositRequestGenerator



@pytest.mark.api
class TestDeposit:
    def test_deposit(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, create_account_response: CreateAccountResponse):
        deposit_request = DepositRequestGenerator.valid(
            create_account_response.id
        )

        response = api_manager.user_steps.deposit(
            create_user_request,
            deposit_request
        )

        assert response.balance == deposit_request.amount, \
            "Баланс в ответе должен совпадать с суммой пополнения"

        db_steps = DbSteps(db_session)

        account = db_steps.get_account(
            create_account_response.id
        )

        assert account.balance == response.balance, \
            "Баланс счета в БД должен совпадать с ответом API"

        db_steps.assert_deposit_transaction_created(
            account_id=create_account_response.id,
            request=deposit_request
        )

    def test_deposit_invalid_amount(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, create_account_response: CreateAccountResponse):
        deposit_request = DepositRequestGenerator.invalid_min_amount(
            create_account_response.id
        )

        db_steps = DbSteps(db_session)

        account_before = db_steps.get_account(
            create_account_response.id
        )

        api_manager.user_steps.deposit_invalid(
            create_user_request,
            deposit_request
        )

        account_after = db_steps.get_account(
            create_account_response.id
        )

        assert account_after.balance == account_before.balance, \
            "Баланс счета не должен измениться!"

        db_steps.assert_deposit_transaction_not_created(
            create_account_response.id
        )