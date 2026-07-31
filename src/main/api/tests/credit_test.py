import pytest

from src.main.api.generators.credit_request_generator import CreditRequestGenerator
from src.main.api.db.steps.db_steps import DbSteps
from src.main.api.classes.api_manager import ApiManager
from sqlalchemy.orm import Session


@pytest.mark.api
class TestCredit:
    def test_credit(self, db_session: Session, api_manager: ApiManager, create_credit_user_request, create_credit_account_response):
        credit_request = CreditRequestGenerator.valid(
            create_credit_account_response.id
        )

        expected_balance = (
            create_credit_account_response.balance +
            credit_request.amount
        )

        response = api_manager.user_steps.credit(
            create_credit_user_request,
            credit_request
        )

        assert response.id == create_credit_account_response.id, \
            "ID счета должен совпадать!"

        assert response.amount == credit_request.amount, \
            "Сумма кредита должна совпадать с запросом!"

        assert response.termMonths == credit_request.termMonths, \
            "Срок кредита должен совпадать с запросом!"

        assert response.creditId > 0, \
            "Должен быть возвращен корректный ID кредита!"

        assert response.balance == expected_balance, \
            "Баланс счета после выдачи кредита рассчитан неверно!"

        db_steps = DbSteps(db_session)

        db_steps.assert_credit_created(
            account_id=create_credit_account_response.id,
            response=response,
            request=credit_request
        )

        db_steps.assert_credit_transaction_created(
            account_id=create_credit_account_response.id,
            request=credit_request
        )

        account = db_steps.get_account(
            create_credit_account_response.id
        )

        assert account.balance == response.balance, \
            "Баланс счета в БД должен совпадать с балансом из ответа API!"


    def test_credit_invalid_min_amount(self, db_session: Session, api_manager: ApiManager, create_credit_user_request, create_credit_account_response):
        credit_request = CreditRequestGenerator.invalid_min_amount(
            create_credit_account_response.id
        )

        db_steps = DbSteps(db_session)

        account_before = db_steps.get_account(
            create_credit_account_response.id
        )

        api_manager.user_steps.credit_invalid(
            create_credit_user_request,
            credit_request
        )

        account_after = db_steps.get_account(
            create_credit_account_response.id
        )

        assert account_after.balance == account_before.balance, \
            "Баланс счета не должен измениться!"

        db_steps.assert_credit_not_created(
            create_credit_account_response.id
        )











