import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.api_fixture import api_manager
from src.main.api.fixtures.user_fixture import create_active_credit
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.db.crud.transaction_crud import TransactionCrudDb


@pytest.mark.api
class TestRepayCredit:
    def test_repay_credit(self, db_session: Session, api_manager: ApiManager, create_credit_user_request, create_active_credit):
        repay_credit_request = RepayCreditRequest(
            creditId=create_active_credit.creditId,
            accountId=create_active_credit.id,
            amount=5000
        )

        account_before = AccountCrudDb.get_account_by_id(
            db_session,
            create_active_credit.id
        )

        credit_before = CreditCrudDb.get_last_credit_by_account_id(
            db_session,
            create_active_credit.id
        )

        transaction_before = TransactionCrudDb.get_last_transaction_by_account_id(
            db_session,
            create_active_credit.id
        )

        assert account_before is not None
        assert credit_before is not None
        assert transaction_before is not None

        account_before_balance = account_before.balance
        credit_before_balance = credit_before.balance
        transaction_before_id = transaction_before.id

        response = api_manager.user_steps.credit_repay(
            create_credit_user_request,
            repay_credit_request
        )

        db_session.expire_all()

        account_after = AccountCrudDb.get_account_by_id(
            db_session,
            create_active_credit.id
        )

        credit_after = CreditCrudDb.get_last_credit_by_account_id(
            db_session,
            create_active_credit.id
        )

        transaction_after = TransactionCrudDb.get_last_transaction_by_account_id(
            db_session,
            create_active_credit.id
        )

        assert account_after is not None
        assert credit_after is not None
        assert transaction_after is not None

        assert account_after.balance == account_before_balance - repay_credit_request.amount
        assert credit_after.balance == credit_before_balance + repay_credit_request.amount
        assert transaction_after.id != transaction_before_id

        assert transaction_after.transaction_type == "credit_repayment"
        assert transaction_after.credit_id == create_active_credit.creditId
        assert transaction_after.from_account_id == create_active_credit.id
        assert transaction_after.to_account_id is None
        assert transaction_after.amount == repay_credit_request.amount

        assert response.creditId == create_active_credit.creditId
        assert response.amountDeposited == repay_credit_request.amount

    def test_repay_credit_invalid(self, db_session: Session, api_manager: ApiManager, create_credit_user_request, create_active_credit):
        repay_credit_request = RepayCreditRequest(
            creditId=create_active_credit.creditId,
            accountId=create_active_credit.id,
            amount=0
        )

        account_before = AccountCrudDb.get_account_by_id(
            db_session,
            create_active_credit.id
        )

        credit_before = CreditCrudDb.get_last_credit_by_account_id(
            db_session,
            create_active_credit.id
        )

        transaction_before = TransactionCrudDb.get_last_transaction_by_account_id(
            db_session,
            create_active_credit.id
        )

        assert account_before is not None
        assert credit_before is not None
        assert transaction_before is not None

        account_before_balance = account_before.balance
        credit_before_balance = credit_before.balance
        transaction_before_id = transaction_before.id

        api_manager.user_steps.credit_repay_bad(
            create_credit_user_request,
            repay_credit_request
        )

        db_session.expire_all()

        account_after = AccountCrudDb.get_account_by_id(
            db_session,
            create_active_credit.id
        )

        credit_after = CreditCrudDb.get_last_credit_by_account_id(
            db_session,
            create_active_credit.id
        )

        transaction_after = TransactionCrudDb.get_last_transaction_by_account_id(
            db_session,
            create_active_credit.id
        )

        assert account_after is not None
        assert credit_after is not None
        assert transaction_after is not None

        assert account_after.balance == account_before_balance
        assert credit_after.balance == credit_before_balance
        assert transaction_after.id == transaction_before_id


    def test_repay_credit_forbidden(self, api_manager, create_active_credit):
        second_user = RandomModelGenerator.generate(CreateUserRequest)
        second_user.role = "ROLE_CREDIT_SECRET"

        api_manager.admin_steps.create_user(second_user)

        repay_credit_request = RepayCreditRequest(
            creditId=create_active_credit.creditId,
            accountId=create_active_credit.id,
            amount=5000
        )
        api_manager.user_steps.credit_repay_not_found(
            second_user,
            repay_credit_request
        )

    def test_repay_credit_invalid_amount(self, api_manager, create_credit_user_request, create_active_credit):
        repay_credit_request = RepayCreditRequest(
            creditId=create_active_credit.creditId,
            accountId=create_active_credit.id,
            amount=22800
        )

        api_manager.user_steps.credit_repay_unprocessable(
            create_credit_user_request,
            repay_credit_request
        )








