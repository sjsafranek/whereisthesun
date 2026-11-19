# from typing import Annotated
from dataclasses import dataclass
from litestar import post
from litestar import Controller
from litestar import Response
# from litestar.params import Body
from litestar.status_codes import HTTP_200_OK
from litestar.status_codes import HTTP_400_BAD_REQUEST

from whereisthesun import find_closest_sunny_cities
from models import ApiRequest
from models import ApiResponse


def makeMissingParameterResponse(parameter_name) -> ApiResponse:
    api_response = ApiResponse()
    api_response.status = "error"
    api_response.error = ApiResponseError()
    api_response.error.code = 404
    api_response.error.message = f"Missing Parameter: '{parameter_name}'"
    return api_response


class ApiV1(Controller):
    path = "/api/v1"

    @post("/sun")
    async def find_the_sun(self, data: ApiRequest) -> Response[ApiResponse]:
    # async def find_the_sun(self, data: Annotated[ApiRequest, Body()]) -> ApiResponse:

        latitude = data.params.get('latitude')
        if not latitude:
            # return makeMissingParameterResponse("latitude")
            return Response(
                content= makeMissingParameterResponse("latitude"),
                status_code=HTTP_400_BAD_REQUEST,
            )

        longitude = data.params.get('longitude')
        if not longitude:
            # return makeMissingParameterResponse("longitude")
            return Response(
                content= makeMissingParameterResponse("longitude"),
                status_code=HTTP_400_BAD_REQUEST,
            )

        api_response = ApiResponse()
        cities = find_closest_sunny_cities(latitude, longitude, **data.params)
        api_response.data['cities'] = cities
        # return api_response
        return Response(
            content=api_response,
            status_code=HTTP_200_OK,
        )

