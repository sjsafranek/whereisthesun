from typing import Annotated
from dataclasses import dataclass
from litestar import Controller
from litestar import post
from litestar.params import Body

from whereisthesun import find_closest_sunny_cities
from models import ApiRequest
from models import ApiResponse


class ApiV1(Controller):
    path = "/api/v1"

    @post("/sun")
    # async def find_the_sun(self, api_request: ApiRequest) -> ApiResponse:
    async def find_the_sun(self, data: Annotated[ApiRequest, Body()]) -> ApiResponse:
        latitude = data.params.get('latitude')
        longitude = data.params.get('longitude')
        cities = find_closest_sunny_cities(latitude, longitude, **data.params)
        api_response = ApiResponse()
        api_response.data['cities'] = cities
        return api_response  

