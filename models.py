from dataclasses import dataclass
from dataclasses import field


@dataclass
class ApiRequest:
    method: str
    params: dict


@dataclass
class ApiResponseError:
    code: int
    message: str
    details: str | None = None


@dataclass
class ApiResponse:
    status: str = 'ok'
    data: dict = field(default_factory=dict)
    error: ApiResponseError | None = None


