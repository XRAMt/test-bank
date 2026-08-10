from sqlalchemy.orm import Session

from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.models.transfer_request import TransferRequest


class DbSteps:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_account(self, account_id):
        return AccountCrudDb.get_account_by_id(
            self.db_session,
            account_id
        )

    def get_last_credit(self, account_id):
        return CreditCrudDb.get_last_credit_by_account_id(
            self.db_session,
            account_id
        )

    def get_last_transaction(self, account_id):
        return TransactionCrudDb.get_last_transaction_by_account_id(
            self.db_session,
            account_id
        )

    def assert_credit_created(self, account_id, response, request):
        credit = self.get_last_credit(account_id)

        assert credit is not None, \
            "В базе данных должна быть создана запись о кредите"

        assert credit.id == response.creditId, \
            "ID кредита в БД должен совпадать с ответом API"

        assert credit.account_id == account_id, \
            "Кредит должен принадлежать указанному счету"

        assert credit.amount == request.amount, \
            "Сумма кредита в БД должна совпадать с запросом"

        assert credit.term_months == request.termMonths, \
            "Срок кредита в БД должен совпадать с запросом"

        assert credit.balance == -request.amount, \
            "Остаток по кредиту должен быть отрицательным и равен сумме кредита"

    def assert_credit_transaction_created(self, account_id, request):
        transaction = self.get_last_transaction(account_id)

        assert transaction is not None, \
            "Должна быть создана транзакция выдачи кредита"

        assert transaction.to_account_id == account_id, \
            "Получателем транзакции должен быть счет пользователя"

        assert transaction.from_account_id is None, \
            "У транзакции выдачи кредита не должно быть счета отправителя"

        assert transaction.credit_id is None, \
            "Поле credit_id должно быть пустым"

        assert transaction.amount == request.amount, \
            "Сумма транзакции должна совпадать с суммой кредита"

        assert transaction.transaction_type == "credit_issuance", \
            "Тип транзакции должен быть credit_issuance"

    def assert_credit_not_created(self, account_id):
        credit = self.get_last_credit(account_id)
        transaction = self.get_last_transaction(account_id)

        assert credit is None, \
            "Кредит не должен быть создан"

        assert transaction is None, \
            "Транзакция выдачи кредита не должна быть создана"


    def assert_deposit_transaction_created(self, account_id, request):
        transaction = self.get_last_transaction(account_id)

        assert transaction is not None, \
            "Должна быть создана транзакция пополнения"

        assert transaction.to_account_id == account_id, \
            "Получателем транзакции должен быть указанный счет"

        assert transaction.from_account_id is None, \
            "У транзакции пополнения не должно быть счета отправителя"

        assert transaction.credit_id is None, \
            "Поле credit_id должно быть пустым"

        assert transaction.amount == request.amount, \
            "Сумма транзакции должна совпадать с суммой пополнения"

        assert transaction.transaction_type == "deposit", \
            "Тип транзакции должен быть deposit"


    def assert_deposit_transaction_not_created(self, account_id):
        transaction = self.get_last_transaction(account_id)

        assert transaction is None, \
            "Транзакция пополнения не должна быть создана"


    def assert_transfer_transaction_created(self, transfer_request: TransferRequest):
        transaction = self.get_last_transaction(transfer_request.fromAccountId)

        assert transaction is not None, \
            "Транзакция перевода не была создана"

        assert transaction.from_account_id == transfer_request.fromAccountId, \
            "Неверный счет отправителя"

        assert transaction.to_account_id == transfer_request.toAccountId, \
            "Неверный счет получателя"

        assert transaction.credit_id is None, \
            "credit_id должен быть пустым"

        assert transaction.amount == transfer_request.amount, \
            "Сумма перевода записана неверно"

        assert transaction.transaction_type == "transfer", \
            "Тип транзакции должен быть transfer"


    def assert_transfer_transaction_not_created(self,account_id: int):
        transaction = self.get_last_transaction(account_id)

        assert transaction is None, \
            "Транзакция перевода не должна быть создана"

    def get_credit_repayment_state(self, account_id):
        account = self.get_account(account_id)
        credit = self.get_last_credit(account_id)
        transaction = self.get_last_transaction(account_id)

        return {
            "account_balance": account.balance,
            "credit_balance": credit.balance,
            "transaction_id": transaction.id
        }


    def assert_credit_repayment_created(self, account_id, credit_id, request, before_state):
        account = self.get_account(account_id)
        credit = self.get_last_credit(account_id)
        transaction = self.get_last_transaction(account_id)

        assert account.balance == (
                before_state["account_balance"] - request.amount
        ), "Баланс счета после погашения кредита рассчитан неверно"

        assert credit.balance == (
                before_state["credit_balance"] + request.amount
        ), "Остаток по кредиту рассчитан неверно"

        assert transaction.id != before_state["transaction_id"], \
            "Должна быть создана новая транзакция"

        assert transaction.transaction_type == "credit_repayment", \
            "Тип транзакции должен быть credit_repayment"

        assert transaction.credit_id == credit_id, \
            "Транзакция должна ссылаться на погашаемый кредит"

        assert transaction.from_account_id == account_id, \
            "Отправителем должен быть счет пользователя"

        assert transaction.to_account_id is None, \
            "Получатель у транзакции погашения должен отсутствовать"

        assert transaction.amount == request.amount, \
            "Сумма транзакции должна совпадать с суммой погашения"


    def assert_credit_repayment_not_created(self,account_id, before_state):
        account = self.get_account(account_id)
        credit = self.get_last_credit(account_id)
        transaction = self.get_last_transaction(account_id)

        assert account.balance == before_state["account_balance"], \
            "Баланс счета не должен измениться"

        assert credit.balance == before_state["credit_balance"], \
            "Остаток по кредиту не должен измениться"

        assert transaction.id == before_state["transaction_id"], \
            "Новая транзакция не должна быть создана"

