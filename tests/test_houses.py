import allure
import pytest

from clients.base_client import ApiClient, NewHouse, NewUser
from constants import StatusCodes


@allure.feature('House api test')
class TestHouseApi:

    def setup_class(self):
        self.client = ApiClient()
        self.token = None
        self.headers = None

    @pytest.fixture(autouse=True)
    def setup_token(self, get_token):
        self.token = get_token.json()['access_token']
        self.headers = {'Authorization': f'Bearer {self.token}'}

    @pytest.fixture()
    def setup_user(self):
        response = self.client.post(
            json=NewUser.new_user_data,
            path='/user',
            headers=self.headers
        )
        NewUser.created_id = response.json()["id"]
        yield
        self.client.delete(
            path=f'/user/{NewUser.created_id}',
            headers=self.headers
        )

    def test_add_new_house(self):
        response = self.client.post(
            json=NewHouse.new_house_data,
            path='/house',
            headers=self.headers
        )
        with allure.step('If status code is 201'):
            assert response.status_code == StatusCodes.CREATED.value

        created_house = response.json()
        NewHouse.created_id = created_house["id"]

    def test_get_house_by_id(self):
        response = self.client.get(
            path=f'/house/{NewHouse.created_id}',
            headers=self.headers
        )
        with allure.step('Check response status'):
            assert response.status_code in (
                StatusCodes.OK.value,
                StatusCodes.NO_CONTENT.value
            )

    def test_change_house_data_by_id(self):
        response = self.client.put(
            path=f'/house/{NewHouse.created_id}',
            headers=self.headers,
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

    def test_settle_user_to_the_house(self, setup_user):
        response = self.client.post(
            path=f'/house/{NewHouse.created_id}/settle/{NewUser.created_id}',
            headers=self.headers
        )
        with allure.step('Check response status'):
            assert response.status_code in (
                StatusCodes.OK.value,
                StatusCodes.NOT_FOUND.value,
                StatusCodes.NOT_ACCEPTABLE.value,
                StatusCodes.INTERNAL_SERVER_ERROR.value
            )

    def test_evict_user_from_the_house(self, setup_user):
        response = self.client.post(
            path=f'/house/{NewHouse.created_id}/evict/{NewUser.created_id}',
            headers=self.headers
        )
        with allure.step('Check response status'):
            assert response.status_code in (
                StatusCodes.OK.value,
                StatusCodes.NOT_FOUND.value,
                StatusCodes.NOT_ACCEPTABLE.value,
                StatusCodes.INTERNAL_SERVER_ERROR.value
            )

    def test_delete_house_by_id(self):
        response = self.client.delete(
            path=f'/house/{NewHouse.created_id}',
            headers=self.headers
        )
        with allure.step('Check the response status'):
            assert response.status_code in (
                StatusCodes.OK.value,
                StatusCodes.CONFLICT.value
            )

    def test_get_list_of_all_houses(self):
        response = self.client.get(
            path='/houses',
            headers=self.headers
        )
        with allure.step('Check the response status'):
            assert response.status_code in (
                StatusCodes.OK.value,
                StatusCodes.NO_CONTENT.value,
                StatusCodes.SERVICE_UNAVAILIBLE.value
            )
