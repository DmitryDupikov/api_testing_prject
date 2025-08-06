import allure
import pytest

from clients.base_client import ApiClient, NewHouse, NewUser
from constants import StatusCodes

client = ApiClient()


@pytest.fixture(autouse=False)
def setup_user(get_token):
    response = client.post(
        json=NewUser.new_user_data,
        path='/user',
        headers={'Authorization': f'Bearer {get_token.json()["access_token"]}'}
    )
    NewUser.created_id = response.json()["id"]
    yield
    client.delete(
        path=f'/user/{NewUser.created_id}',
        headers={'Authorization': f'Bearer {get_token.json()["access_token"]}'}
    )


@allure.feature('House api test')
def test_add_new_house(get_token):
    response = client.post(
        json=NewHouse.new_house_data,
        path='/house',
        headers={
            'Authorization': f'Bearer {get_token.json()['access_token']}'
        }
    )
    with allure.step('If status code is 201'):
        assert response.status_code == StatusCodes.CREATED.value

    created_user = response.json()
    NewHouse.created_id = created_user["id"]


@allure.feature('House api test')
def test_get_house_by_id(get_token):
    response = client.get(
        path=f'/house/{NewHouse.created_id}',
        headers={
            'Authorization': f'Bearer {get_token.json()['access_token']}'
        }
    )
    with allure.step('Check response status'):
        assert response.status_code in (
            StatusCodes.OK.value,
            StatusCodes.NO_CONTENT.value
        )


@allure.feature('House api test')
def test_change_house_data_by_id(get_token):
    response = client.put(
        path=f'/house/{NewHouse.created_id}',
        headers={
            'Authorization': f'Bearer {get_token.json()['access_token']}'
        },
        json={
            "floorCount": 55,
            "id": NewHouse.id_house,
            "parkingPlaces": [
                {
                    "id": 5,
                    "isCovered": True,
                    "isWarm": True,
                    "placesCount": 50
                }
            ],
            "price": 100000
        }
    )
    with allure.step('If status code is 202'):
        assert response.status_code == StatusCodes.ACCEPTED.value


@allure.feature('House api test')
def test_settle_user_to_the_house(get_token, setup_user):
    response = client.post(
        path=f'/house/{NewHouse.created_id}/settle/{NewUser.created_id}',
        headers={
            'Authorization': f'Bearer {get_token.json()['access_token']}'
        }
    )

    with allure.step('Check response status'):
        assert response.status_code in (
            StatusCodes.OK.value,
            StatusCodes.NOT_FOUND.value,
            StatusCodes.NOT_ACCEPTABLE.value,
            StatusCodes.INTERNAL_SERVER_ERROR.value
        )


@allure.feature('House api test')
def test_evict_user_from_the_house(get_token, setup_user):
    response = client.post(
        path=f'/house/{NewHouse.created_id}/evict/{NewUser.created_id}',
        headers={
            'Authorization': f'Bearer {get_token.json()['access_token']}'
        }
    )

    with allure.step('Check response status'):
        assert response.status_code in (
            StatusCodes.OK.value,
            StatusCodes.NOT_FOUND.value,
            StatusCodes.NOT_ACCEPTABLE.value,
            StatusCodes.INTERNAL_SERVER_ERROR.value
        )


@allure.feature('House api test')
def test_delete_house_by_id(get_token):
    response = client.delete(
        path=f'/house/{NewHouse.created_id}',
        headers={
            'Authorization': f'Bearer {get_token.json()['access_token']}'
        }
    )
    with allure.step('Check the response status'):
        assert response.status_code in (
            StatusCodes.OK.value,
            StatusCodes.CONFLICT.value
        )


@allure.feature('House api test')
def test_get_list_of_all_houses(get_token):
    response = client.get(
        path='/houses',
        headers={
            'Authorization': f'Bearer {get_token.json()['access_token']}'
        }
    )
    with allure.step('Check the response status'):
        assert response.status_code in (
            StatusCodes.OK.value,
            StatusCodes.NO_CONTENT.value,
            StatusCodes.SERVICE_UNAVAILIBLE.value
        )
