from dotenv import load_dotenv
import os
from typing import Optional, Dict, Any, Union
from urllib.parse import urljoin

import allure
import httpx
from httpx import Response, QueryParams

load_dotenv()


class ApiClient:
    def __init__(self):
        self.base_adress = os.getenv('URL')
        self.client = httpx.Client(base_url=self.base_adress)
        self.response: Optional[Response] = None

    @allure.step("Make GET request")
    def get(self,
            path:  str = "/",
            headers: Optional[Dict[str, str]] = None,
            params: Optional[Union[Dict[str, Any],
                                   QueryParams]] = None) -> Response:

        url = urljoin(self.base_adress, path)
        return self.client.get(url, headers=headers, params=params)

    @allure.step("Make Post request")
    def post(self,
             path="/", headers: Optional[Dict[str, str]] = None,
             params: Optional[Union[Dict[str, Any], QueryParams]] = None,
             data: Optional[Dict[str, Any]] = None,
             json: Optional[Dict[str, Any]] = None) -> Response:

        url = urljoin(self.base_adress, path)
        return self.client.post(url,
                                headers=headers,
                                params=params,
                                data=data,
                                json=json)

    @allure.step("Make Put request")
    def put(self,
            path: str = "/", headers: Optional[Dict[str, str]] = None,
            params: Optional[Union[Dict[str, Any], QueryParams]] = None,
            data: Optional[Dict[str, Any]] = None,
            json: Optional[Dict[str, Any]] = None) -> Response:

        url = urljoin(self.base_adress, path)
        return self.client.put(url,
                               headers=headers,
                               params=params,
                               data=data,
                               json=json)

    @allure.step("Make Delete request")
    def delete(self,
               path: str = "/",
               headers: Optional[Dict[str, str]] = None,
               params: Optional[Union[Dict[str, Any],
                                      QueryParams]] = None) -> Response:

        url = urljoin(self.base_adress, path)
        return self.client.delete(url, headers=headers, params=params)


class NewUser:
    id_user = 9999
    new_user_data = {
        "age": 99,
        "firstName": "Дмитрий",
        "id": id_user,
        "money": 999000,
        "secondName": "Тестов",
        "sex": "MALE"
    }


class NewHouse:
    id_house = 999
    new_house_data = {
        "floorCount": 55,
        "id": id_house,
        "parkingPlaces": [
            {
                "id": 5,
                "isCovered": True,
                "isWarm": True,
                "placesCount": 24
            }
        ],
        "price": 55000
    }


class NewCar:
    id_car = 4000
    new_car_data = {
        "engineType": "Gasoline",
        "id": id_car,
        "mark": "BMW",
        "model": "W",
        "price": 95000
    }
