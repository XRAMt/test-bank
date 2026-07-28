from src.main.api.models import repay_credit_request
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.steps.base_steps import BaseSteps
from src.main.api.foundation.endpoint import Endpoint


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post()
        return response

    def deposit(self, create_user_request: CreateUserRequest, deposit_request: DepositRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.ACCOUNT_DEPOSIT,
            ResponseSpecs.request_ok()
        ).post(deposit_request)
        return response

    def deposit_invalid(self, create_user_request: CreateUserRequest, deposit_request: DepositRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.ACCOUNT_DEPOSIT,
            ResponseSpecs.request_bad()
        ).post(deposit_request)
        return response


    def transfer(self, create_user_request: CreateUserRequest, transfer_request: TransferRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.ACCOUNT_TRANSFER,
            ResponseSpecs.request_ok()
        ).post(transfer_request)
        return response

    def transfer_invalid(self, create_user_request: CreateUserRequest, transfer_request: TransferRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.ACCOUNT_TRANSFER,
            ResponseSpecs.request_bad()
        ).post(transfer_request)
        return response

    def credit(self, create_user_request: CreateUserRequest, credit_request: CreditRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.ACCOUNT_CREDIT,
            ResponseSpecs.request_created()
        ).post(credit_request)
        return response

    def credit_invalid(self, create_user_request: CreateUserRequest, credit_request: CreditRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.ACCOUNT_CREDIT,
            ResponseSpecs.request_bad()
        ).post(credit_request)
        return response

    def credit_forbidden(self, create_user_request: CreateUserRequest, credit_request: CreditRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.ACCOUNT_CREDIT,
            ResponseSpecs.request_forbidden()
        ).post(credit_request)
        return response

    def credit_not_found(self, create_user_request: CreateUserRequest, credit_request: CreditRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.ACCOUNT_CREDIT,
            ResponseSpecs.request_not_found()
        ).post(credit_request)
        return response

    def credit_repay(self, create_user_request: CreateUserRequest, repay_credit_request: RepayCreditRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.ACCOUNT_CREDIT_REPAY,
            ResponseSpecs.request_ok()
        ).post(repay_credit_request)
        return response

    def credit_repay_bad(self, create_user_request: CreateUserRequest, repay_credit_request: RepayCreditRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.ACCOUNT_CREDIT_REPAY,
            ResponseSpecs.request_bad()
        ).post(repay_credit_request)
        return response

    def credit_repay_not_found(self, create_user_request: CreateUserRequest, repay_credit_request: RepayCreditRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.ACCOUNT_CREDIT_REPAY,
            ResponseSpecs.request_not_found()
        ).post(repay_credit_request)
        return response

    def credit_repay_unprocessable(self, create_user_request: CreateUserRequest, repay_credit_request: RepayCreditRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.ACCOUNT_CREDIT_REPAY,
            ResponseSpecs.request_unprocessable_entity()
        ).post(repay_credit_request)
        return response

    """def credit_repay_forbidden(self, create_user_request: CreateUserRequest, repay_credit_request: RepayCreditRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.ACCOUNT_CREDIT_REPAY,
            ResponseSpecs.request_forbidden()
        ).post(repay_credit_request)
        return response"""