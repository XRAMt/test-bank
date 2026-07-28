import pytest

from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.generators.model_generator import RandomModelGenerator

@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request


@pytest.fixture
def create_account_response(api_manager, create_user_request):
    return api_manager.user_steps.create_account(create_user_request)

@pytest.fixture
def create_accounts_response(api_manager, create_user_request):
    first_account = api_manager.user_steps.create_account(create_user_request)
    second_account = api_manager.user_steps.create_account(create_user_request)

    return first_account, second_account

@pytest.fixture
def create_credit_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    user_request.role = "ROLE_CREDIT_SECRET"

    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def create_credit_account_response(api_manager, create_credit_user_request):
    return api_manager.user_steps.create_account(create_credit_user_request)

@pytest.fixture
def create_credit_accounts_response(api_manager, create_credit_user_request):
    first_account = api_manager.user_steps.create_account(create_credit_user_request)
    second_account = api_manager.user_steps.create_account(create_credit_user_request)

    return first_account, second_account

@pytest.fixture
def create_active_credit(api_manager, create_credit_user_request, create_credit_account_response):
    credit_request = CreditRequest(
        accountId=create_credit_account_response.id,
        amount=5000,
        termMonths=12
    )

    return api_manager.user_steps.credit(
        create_credit_user_request,
        credit_request
    )



