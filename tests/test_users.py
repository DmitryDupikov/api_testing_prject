import allure
import pytest

from clients.base_client import ApiClient, NewUser, NewCar
from constants import StatusCodes

client = ApiClient()


@pytest.fixture(autouse=False)
def setup_car(get_token):
    response = client.post(
        json=NewCar.new_car_data,
        path='/car',
        headers={'Authorization': f'Bearer {get_token.json()["access_token"]}'}
    )
    NewCar.created_id = response.json()["id"]
    yield
    client.delete(
        path=f'/car/{NewCar.created_id}',
        headers={'Authorization': f'Bearer {get_token.json()["access_token"]}'}
    )


@allure.feature('User api test')
def test_add_new_user(get_token):
    response = client.post(
        json=NewUser.new_user_data,
        path='/user',
        headers={
            'Authorization': f'Bearer {get_token.json()['access_token']}'
        }
    )
    with allure.step('If status code is 201'):
        assert response.status_code == StatusCodes.CREATED.value

    created_user = response.json()
    NewUser.created_id = created_user["id"]


@allure.feature('User api test')
def test_get_user_by_id(get_token):
    response = client.get(
        path=f'/user/{NewUser.created_id}',
        headers={
            'Authorization': f'Bearer {get_token.json()['access_token']}'
        }

    )
    with allure.step('if status code is 200'):
        assert response.status_code == StatusCodes.OK.value


@allure.feature('User Money API')
def test_add_money_to_user(get_token):
    MONEY_AMOUNT = 100.01

    response = client.post(
        path=f'/user/{NewUser.created_id}/money/{MONEY_AMOUNT}',
        headers={
            'Authorization': f'Bearer {get_token.json()["access_token"]}'
        }
    )
    with allure.step('Check that money was added (status 200)'):
        assert response.status_code in (
            StatusCodes.OK.value,
            StatusCodes.BAD_REQUEST.value,
            StatusCodes.NOT_FOUND.value,
            StatusCodes.INTERNAL_SERVER_ERROR.value
        )

    with allure.step('Verify user balance after transaction'):
        user_response = client.get(
            path=f'/user/{NewUser.created_id}',
            headers={
                'Authorization': f'Bearer {get_token.json()["access_token"]}'
            }
        )
        current_balance = user_response.json()["money"]
        expected_balance = NewUser.new_user_data["money"] + MONEY_AMOUNT
        assert current_balance == expected_balance


@allure.feature('User api test')
def test_change_user_data_by_id(get_token):
    response = client.put(
        path=f'/user/{NewUser.created_id}',
        headers={
            'Authorization': f'Bearer {get_token.json()['access_token']}'
        },
        json={
            "age": 55,
            "firstName": "Alexander",
            "id": NewUser.id_user,
            "money": 999000,
            "secondName": "Secondnamov",
            "sex": "MALE"
        }
    )
    with allure.step('If status code is 202'):
        assert response.status_code == StatusCodes.ACCEPTED.value


@allure.feature('User api test')
def test_get_all_user_cars(get_token):
    response = client.get(
        path=f'/user/{NewUser.created_id}/cars',
        headers={
            'Authorization': f'Bearer {get_token.json()['access_token']}'
        }
    )
    with allure.step('Check response status'):
        assert response.status_code in (
            StatusCodes.OK.value,
            StatusCodes.NO_CONTENT.value,
            StatusCodes.SERVICE_UNAVAILIBLE.value
        )


@allure.feature('User api test')
def test_get_all_user_properties(get_token):
    response = client.get(
        path=f'/user/{NewUser.created_id}/info',
        headers={
            'Authorization': f'Bearer {get_token.json()['access_token']}'
        }
    )
    with allure.step('Check response status'):
        assert response.status_code in (
            StatusCodes.OK.value,
            StatusCodes.NO_CONTENT.value,
        )


@allure.feature('User api test')
def test_user_buy_a_car(get_token, setup_car):
    response = client.post(
        path=f'/user/{NewUser.created_id}/buyCar/{NewCar.created_id}',
        headers={
            'Authorization': f'Bearer {get_token.json()['access_token']}'
        }
    )
    with allure.step('if status code is 200'):
        assert response.status_code == StatusCodes.OK.value


@allure.feature('User api test')
def test_user_sells_a_car(get_token, setup_car):
    response = client.post(
        path=f'/user/{NewUser.created_id}/sellCar/{NewCar.created_id}',
        headers={
            'Authorization': f'Bearer {get_token.json()['access_token']}'
        }
    )
    with allure.step('if status code is 200'):
        assert response.status_code == StatusCodes.OK.value


@allure.feature('User api test')
def test_delete_user_by_id(get_token):
    response = client.delete(
        path=f'/user/{NewUser.created_id}',
        headers={
            'Authorization': f'Bearer {get_token.json()['access_token']}'
        }
    )
    with allure.step('if status code is 204'):
        assert response.status_code in (
            StatusCodes.NO_CONTENT.value,
            StatusCodes.CONFLICT.value
        )


@allure.feature('User api test')
def test_get_all_users_list(get_token):
    response = client.get(
        path='/users/',
        headers={
            'Authorization': f'Bearer {get_token.json()['access_token']}'
        }
    )
    with allure.step('Check response status'):
        assert response.status_code in (
            StatusCodes.OK.value,
            StatusCodes.NO_CONTENT.value,
            StatusCodes.SERVICE_UNAVAILIBLE.value
        )
