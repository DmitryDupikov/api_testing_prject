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

    def assert_status(self, response, expected_statuses, step_description):
        with allure.step(step_description):
            assert response.status_code in expected_statuses

    def test_add_new_user(self):
        response = self.client.post(
            json=NewUser.new_user_data,
            path='/user',
            headers=self.headers
        )
        self.assert_status(response, 
                           [StatusCodes.CREATED.value], 
                           'Check the response status is 201')

        created_user = response.json()
        NewUser.created_id = created_user["id"]

    def test_get_user_by_id(self):
        response = self.client.get(
            path=f'/user/{NewUser.created_id}',
            headers=self.headers
        )
        self.assert_status(response,
                           [StatusCodes.OK.value],
                           'Check the response status is 200')

    def test_add_money_to_user(self):
        MONEY_AMOUNT = 100.01

        response = self.client.post(
            path=f'/user/{NewUser.created_id}/money/{MONEY_AMOUNT}',
            headers=self.headers
        )
        self.assert_status(response, [
            StatusCodes.OK.value,
            StatusCodes.BAD_REQUEST.value,
            StatusCodes.NOT_FOUND.value,
            StatusCodes.INTERNAL_SERVER_ERROR.value
        ], 'Check response status')

        user_response = self.client.get(
            path=f'/user/{NewUser.created_id}',
            headers=self.headers
        )
        current_balance = user_response.json()["money"]
        expected_balance = NewUser.new_user_data["money"] + MONEY_AMOUNT

        with allure.step('Verify user balance after transaction'):
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
        self.assert_status(response,
                           [StatusCodes.ACCEPTED.value], 
                           'Check the response status is 202')

    def test_get_all_user_cars(self):
        response = self.client.get(
            path=f'/user/{NewUser.created_id}/cars',
            headers=self.headers
        )
        self.assert_status(response, [
            StatusCodes.OK.value,
            StatusCodes.NO_CONTENT.value,
            StatusCodes.SERVICE_UNAVAILIBLE.value
        ], 'Check response status')

    def test_get_all_user_properties(self):
        response = self.client.get(
            path=f'/user/{NewUser.created_id}/info',
            headers=self.headers
        )
        self.assert_status(response, [
            StatusCodes.OK.value,
            StatusCodes.NO_CONTENT.value
        ], 'Check response status')

    def test_user_buy_a_car(self, setup_car):
        response = self.client.post(
            path=f'/user/{NewUser.created_id}/buyCar/{NewCar.created_id}',
            headers=self.headers
        )
        self.assert_status(response, 
                           [StatusCodes.OK.value], 
                           'Check the response status is 200')

    def test_user_sells_a_car(self, setup_car):
        response = self.client.post(
            path=f'/user/{NewUser.created_id}/sellCar/{NewCar.created_id}',
            headers=self.headers
        )
        self.assert_status(response, 
                           [StatusCodes.OK.value], 
                           'Check the response status is 200')

    def test_delete_user_by_id(self):
        response = self.client.delete(
            path=f'/user/{NewUser.created_id}',
            headers=self.headers
        )
        self.assert_status(response, [
            StatusCodes.NO_CONTENT.value,
            StatusCodes.CONFLICT.value
        ], 'Check response status')

    def test_get_all_users_list(self):
        response = self.client.get(
            path='/users/',
            headers=self.headers
        )
        self.assert_status(response, [
            StatusCodes.OK.value,
            StatusCodes.NO_CONTENT.value,
            StatusCodes.SERVICE_UNAVAILIBLE.value
        ], 'Check response status')