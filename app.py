from pathlib import Path
# import logging
import uvicorn
import traceback
from litestar import Litestar
from litestar import get
from litestar import Request
from litestar import Response
from litestar.response import Template
from litestar.template.config import TemplateConfig
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.logging import LoggingConfig
from litestar.middleware.logging import LoggingMiddlewareConfig
from litestar.status_codes import HTTP_204_NO_CONTENT
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from litestar.static_files import create_static_files_router

from api_v1 import ApiV1
from models import ApiResponse



# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s [%(levelname)s] [%(process)d] %(filename)s %(funcName)s:%(lineno)d %(message)s'
# )


logging_config = LoggingConfig(
    # root={"level": "DEBUG", "handlers": ["queue_listener"]},
    root={"level": "DEBUG", "handlers": ["console"]},
    formatters={
        "standard": {
            "format": '%(asctime)s [%(levelname)s] [%(process)d] %(filename)s %(funcName)s:%(lineno)d %(message)s',
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    loggers={
        "uvicorn": {
            "level": "DEBUG",
            "handlers": [],
            "propagate": True,
        },
        "uvicorn.error": {
            "level": "DEBUG",
            "handlers": [],
            "propagate": True,
        },
        "uvicorn.access": {
            "level": "DEBUG",
            "handlers": [],
            "propagate": True,
        },
    },
    log_exceptions="always",
)


logging_middleware = LoggingMiddlewareConfig(
    request_log_fields=("method", "path", "query"),
    response_log_fields=("status_code",),
)


def internal_server_error_handler(request: Request, exc: Exception) -> Response:
    tb_str = traceback.format_exc()
    
    # Print to console or send to your logging service
    print(tb_str)
    
    return Response(
        content={
            "status": "error",
            "error": {
                "code": 500,
                "message": "Internal Server Error",
                "details": tb_str.splitlines(),  # Remove this line in production
            }
        },
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )


@get(
    "/.well-known/appspecific/com.chrome.devtools.json",
    status_code=HTTP_204_NO_CONTENT,
    include_in_schema=False,
)
async def chrome_devtools_well_known() -> None:
    return None


@get("/")
async def index() -> Template:
    return Template(template_name="index.html")


app = Litestar(
    route_handlers=[
        chrome_devtools_well_known,
        index, 
        ApiV1,
        create_static_files_router(
            path="/static",          # URL prefix to access files
            directories=["static"],  # Local folder(s) relative to working directory
        ),
    ],
    template_config=TemplateConfig(
        directory=Path("templates"),
        engine=JinjaTemplateEngine,
    ),
    exception_handlers={
        HTTP_500_INTERNAL_SERVER_ERROR: internal_server_error_handler,
    },
    middleware=[logging_middleware.middleware],
    logging_config=logging_config
    # debug=True
)


# for route in app.routes:
#     print(route.path, route.methods)


# if __name__ == "__main__":
#     uvicorn.run(app)

