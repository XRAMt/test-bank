import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.repay_request_generator import RepayCreditRequestGenerator
from src.main.api.db.steps.db_steps import DbSteps


@pytest.mark.api
class TestRepayCredit:
    def test_repay_credit(self, db_session: Session, api_manager: ApiManager, create_credit_user_request, create_active_credit):
        repay_request = RepayCreditRequestGenerator.valid(
            create_active_credit.creditId,
            create_active_credit.id,
            create_active_credit.amount
        )

        db_steps = DbSteps(db_session)

        before_state = db_steps.get_credit_repayment_state(
            create_active_credit.id
        )

        response = api_manager.user_steps.credit_repay(
            create_credit_user_request,
            repay_request
        )

        db_session.expire_all()

        assert response.creditId == create_active_credit.creditId, \
            "ID кредита должен совпадать"

        assert response.amountDeposited == repay_request.amount, \
            "Сумма погашения должна совпадать с запросом"

        db_steps.assert_credit_repayment_created(
            account_id=create_active_credit.id,
            credit_id=create_active_credit.creditId,
            request=repay_request,
            before_state=before_state
        )

    def test_repay_credit_not_full_amount(self, db_session: Session, api_manager: ApiManager, create_credit_user_request, create_active_credit):
        repay_request = RepayCreditRequestGenerator.invalid_min_amount(
            create_active_credit.creditId,
            create_active_credit.id
        )

        db_steps = DbSteps(db_session)

        before_state = db_steps.get_credit_repayment_state(
            create_active_credit.id
        )

        api_manager.user_steps.credit_repay_bad(
            create_credit_user_request,
            repay_request
        )

        db_session.expire_all()

        db_steps.assert_credit_repayment_not_created(
            account_id=create_active_credit.id,
            before_state=before_state
        )








