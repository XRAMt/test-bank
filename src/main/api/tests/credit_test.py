import pytest
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.models.credit_request import CreditRequest
from sqlalchemy.orm import Session


@pytest.mark.api
class TestCredit:
    def test_credit(self,db_session: Session, api_manager: ApiManager, create_credit_user_request, create_credit_account_response):
        credit_request = CreditRequest(
            accountId=create_credit_account_response.id,
            amount=5000,
            termMonths=12
        )

        response = api_manager.user_steps.credit(
            create_credit_user_request,
            credit_request
        )

        account = AccountCrudDb.get_account_by_id(
            db_session,
            create_credit_account_response.id
        )

        credit = CreditCrudDb.get_last_credit_by_account_id(
            db_session,
            create_credit_account_response.id
        )

        transaction = TransactionCrudDb.get_last_transaction_by_account_id(
            db_session,
            create_credit_account_response.id
        )

        assert account.balance == response.balance

        assert response.id == create_credit_account_response.id
        assert response.amount == credit_request.amount
        assert response.termMonths == credit_request.termMonths
        assert response.balance == create_credit_account_response.balance + credit_request.amount
        assert response.creditId > 0

        assert credit is not None
        assert credit.id == response.creditId
        assert credit.account_id == create_credit_account_response.id
        assert credit.amount == credit_request.amount
        assert credit.term_months == credit_request.termMonths
        assert credit.balance == -credit_request.amount

        assert transaction is not None
        assert transaction.to_account_id == create_credit_account_response.id
        assert transaction.from_account_id is None
        assert transaction.credit_id is None
        assert transaction.amount == credit_request.amount
        assert transaction.transaction_type == "credit_issuance"


    def test_credit_invalid_min_amount(self, db_session: Session, api_manager: ApiManager, create_credit_user_request, create_credit_account_response):
        credit_request = CreditRequest(
            accountId=create_credit_account_response.id,
            amount=1488,
            termMonths=12
        )

        account_before = AccountCrudDb.get_account_by_id(
            db_session,
            create_credit_account_response.id
        )

        credit_before = CreditCrudDb.get_last_credit_by_account_id(
            db_session,
            create_credit_account_response.id
        )

        transaction_before = TransactionCrudDb.get_last_transaction_by_account_id(
            db_session,
            create_credit_account_response.id
        )

        api_manager.user_steps.credit_invalid(
            create_credit_user_request,
            credit_request
        )

        account_after = AccountCrudDb.get_account_by_id(
            db_session,
            create_credit_account_response.id
        )

        credit_after = CreditCrudDb.get_last_credit_by_account_id(
            db_session,
            create_credit_account_response.id
        )

        transaction_after = TransactionCrudDb.get_last_transaction_by_account_id(
            db_session,
            create_credit_account_response.id
        )

        assert account_before is not None
        assert account_after is not None
        assert account_after.balance == account_before.balance

        assert credit_before is None
        assert credit_after is None

        assert transaction_before is None
        assert transaction_after is None

    def test_credit_second_account_with_active_credit(self, api_manager, create_credit_user_request, create_credit_accounts_response):
        first_account, second_account = create_credit_accounts_response
        credit_request = CreditRequest(
            accountId=first_account.id,
            amount=5000,
            termMonths=12
        )

        api_manager.user_steps.credit(
            create_credit_user_request,
            credit_request
        )

        credit_request_second = CreditRequest(
            accountId=second_account.id,
            amount=5000,
            termMonths=12
        )
        # TODO: API returns 404 instead of documented 403
        api_manager.user_steps.credit_not_found(
            create_credit_user_request,
            credit_request_second
        )


    def test_credit_invalid_max_amount(self, api_manager, create_credit_user_request, create_credit_account_response):
        credit_request = CreditRequest(
            accountId=create_credit_account_response.id,
            amount=15001,
            termMonths=12
        )

        api_manager.user_steps.credit_invalid(
            create_credit_user_request,
            credit_request
        )

    def test_credit_invalid_role(self, api_manager, create_user_request, create_account_response):
        credit_request = CreditRequest(
            accountId=create_account_response.id,
            amount=5000,
            termMonths=12
        )

        api_manager.user_steps.credit_forbidden(
            create_user_request,
            credit_request
        )

    def test_credit_second_active_credit(self, api_manager, create_credit_user_request, create_credit_account_response):
        credit_request = CreditRequest(
            accountId=create_credit_account_response.id,
            amount=5000,
            termMonths=12
        )

        api_manager.user_steps.credit(
            create_credit_user_request,
            credit_request
        )
        # TODO: API returns 404 instead of documented 403 (Swagger)
        api_manager.user_steps.credit_not_found(
            create_credit_user_request,
            credit_request
        )







