import allure

from clients.base_client import ApiClient, NewCar
from constants import StatusCodes

client = ApiClient()


@allure.feature('Car api test')
def test_add_new_car(get_token):
    response = client.post(
        json=NewCar.new_car_data,
        path='/car',
        headers={
            'Authorization': f'Bearer {get_token.json()['access_token']}'
        }
    )
    with allure.step('If status code is 201'):
        assert response.status_code == StatusCodes.CREATED.value

    created_car = response.json()
    NewCar.created_id = created_car["id"]


@allure.feature('Car api test')
def test_get_car_by_id(get_token):
    response = client.get(
        path=f'/car/{NewCar.created_id}',
        headers={
            'Authorization': f'Bearer {get_token.json()['access_token']}'
        }
    )
    with allure.step('Check response status'):
        assert response.status_code in (
            StatusCodes.OK.value,
            StatusCodes.NO_CONTENT.value
        )


@allure.feature('Car api test')
def test_change_car_data_by_id(get_token):
    response = client.put(
        path=f'/car/{NewCar.created_id}',
        headers={
            'Authorization': f'Bearer {get_token.json()['access_token']}'
        },
        json={
            "engineType": "Gasoline",
            "id": NewCar.id_car,
            "mark": "BMW",
            "model": "N",
            "price": 100.99
        }
    )
    with allure.step('If status code is 202'):
        assert response.status_code == StatusCodes.ACCEPTED.value


@allure.feature('Car api test')
def test_get_all_cars_list(get_token):
    response = client.get(
        path='/cars/',
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


@allure.feature('Car api test')
def test_delete_car_by_id(get_token):
    response = client.delete(
        path=f'/car/{NewCar.created_id}',
        headers={
            'Authorization': f'Bearer {get_token.json()['access_token']}'
        }
    )
    with allure.step('if status code is 204'):
        assert response.status_code == StatusCodes.NO_CONTENT.value
