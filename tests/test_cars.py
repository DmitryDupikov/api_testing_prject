import allure
import pytest

from clients.base_client import ApiClient, NewCar
from constants import StatusCodes


@allure.feature('Car api test')
class TestCarApi:

    def setup_class(self):
        self.client = ApiClient()
        self.token = None
        self.headers = None

    @pytest.fixture(autouse=True)
    def setup_token(self, get_token):
        self.token = get_token.json()['access_token']
        self.headers = {'Authorization': f'Bearer {self.token}'}

    def test_add_new_car(self):
        response = self.client.post(
            path='/car',
            json=NewCar.new_car_data,
            headers=self.headers
        )
        with allure.step('If status code is 201'):
            assert response.status_code == StatusCodes.CREATED.value

        created_car = response.json()
        NewCar.created_id = created_car["id"]

    def test_get_car_by_id(self):
        response = self.client.get(
            path=f'/car/{NewCar.created_id}',
            headers=self.headers
        )
        with allure.step('Check response status'):
            assert response.status_code in (
                StatusCodes.OK.value,
                StatusCodes.NO_CONTENT.value
            )

    def test_change_car_data_by_id(self):
        response = self.client.put(
            path=f'/car/{NewCar.created_id}',
            headers=self.headers,
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

    def test_get_all_cars_list(self):
        response = self.client.get(
            path='/cars/',
            headers=self.headers
        )
        with allure.step('Check response status'):
            assert response.status_code in (
                StatusCodes.OK.value,
                StatusCodes.NO_CONTENT.value,
                StatusCodes.SERVICE_UNAVAILIBLE.value
            )

    def test_delete_car_by_id(self):
        response = self.client.delete(
            path=f'/car/{NewCar.created_id}',
            headers=self.headers
        )
        with allure.step('if status code is 204'):
            assert response.status_code == StatusCodes.NO_CONTENT.value
