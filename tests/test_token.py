import allure

from constants import StatusCodes


@allure.feature('Get token')
def test_get_token(get_token):
    response = get_token
    with allure.step('if status code is 202'):
        assert response.status_code == StatusCodes.ACCEPTED.value
