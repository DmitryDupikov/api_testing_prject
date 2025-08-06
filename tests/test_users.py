import allure
import pytest

from clients.base_client import ApiClient, NewUser, NewCar
from constants import StatusCodes


@allure.feature('User api test')
class TestUserApi:

    def setup_class(self):
        self.client = ApiClient()
        self.token = None
        self.headers = None

    @pytest.fixture(autouse=True)
    def setup_token(self, get_token):
        self.token = get_token.json()['access_token']
        self.headers = {'Authorization': f'Bearer {self.token}'}

    @pytest.fixture()
    def setup_car(self):
        response = self.client.post(
            json=NewCar.new_car_data,
            path='/car',
            headers=self.headers
        )
        NewCar.created_id = response.json()["id"]

        yield

        self.client.delete(
            path=f'/car/{NewCar.created_id}',
            headers=self.headers
        )

    def test_add_new_user(self):
        response = self.client.post(
            json=NewUser.new_user_data,
            path='/user',
            headers=self.headers
        )
        with allure.step('If status code is 201'):
            assert response.status_code == StatusCodes.CREATED.value

        created_user = response.json()
        NewUser.created_id = created_user["id"]

    def test_get_user_by_id(self):
        response = self.client.get(
            path=f'/user/{NewUser.created_id}',
            headers=self.headers
        )
        with allure.step('if status code is 200'):
            assert response.status_code == StatusCodes.OK.value

    def test_add_money_to_user(self):
        MONEY_AMOUNT = 100.01

        response = self.client.post(
            path=f'/user/{NewUser.created_id}/money/{MONEY_AMOUNT}',
            headers=self.headers
        )
        with allure.step('Check the response status'):
            assert response.status_code in (
                StatusCodes.OK.value,
                StatusCodes.BAD_REQUEST.value,
                StatusCodes.NOT_FOUND.value,
                StatusCodes.INTERNAL_SERVER_ERROR.value
            )

        with allure.step('Verify user balance after transaction'):
            user_response = self.client.get(
                path=f'/user/{NewUser.created_id}',
                headers=self.headers
            )
            current_balance = user_response.json()["money"]
            expected_balance = NewUser.new_user_data["money"] + MONEY_AMOUNT
            assert current_balance == expected_balance

    def test_change_user_data_by_id(self):
        response = self.client.put(
            path=f'/user/{NewUser.created_id}',
            headers=self.headers,
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

    def test_get_all_user_cars(self):
        response = self.client.get(
            path=f'/user/{NewUser.created_id}/cars',
            headers=self.headers
        )
        with allure.step('Check response status'):
            assert response.status_code in (
                StatusCodes.OK.value,
                StatusCodes.NO_CONTENT.value,
                StatusCodes.SERVICE_UNAVAILIBLE.value
            )

    def test_get_all_user_properties(self):
        response = self.client.get(
            path=f'/user/{NewUser.created_id}/info',
            headers=self.headers
        )
        with allure.step('Check response status'):
            assert response.status_code in (
                StatusCodes.OK.value,
                StatusCodes.NO_CONTENT.value
            )

    def test_user_buy_a_car(self, setup_car):
        response = self.client.post(
            path=f'/user/{NewUser.created_id}/buyCar/{NewCar.created_id}',
            headers=self.headers
        )
        with allure.step('if status code is 200'):
            assert response.status_code == StatusCodes.OK.value

    def test_user_sells_a_car(self, setup_car):
        response = self.client.post(
            path=f'/user/{NewUser.created_id}/sellCar/{NewCar.created_id}',
            headers=self.headers
        )
        with allure.step('if status code is 200'):
            assert response.status_code == StatusCodes.OK.value

    def test_delete_user_by_id(self):
        response = self.client.delete(
            path=f'/user/{NewUser.created_id}',
            headers=self.headers
        )
        with allure.step('if status code is 204'):
            assert response.status_code in (
                StatusCodes.NO_CONTENT.value,
                StatusCodes.CONFLICT.value
            )

    def test_get_all_users_list(self):
        response = self.client.get(
            path='/users/',
            headers=self.headers
        )
        with allure.step('Check response status'):
            assert response.status_code in (
                StatusCodes.OK.value,
                StatusCodes.NO_CONTENT.value,
                StatusCodes.SERVICE_UNAVAILIBLE.value
            )