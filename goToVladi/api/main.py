import logging

from asgi_monitor.integrations.fastapi import setup_metrics, MetricsConfig
from fastapi import FastAPI

from goToVladi.api.config.models.api import ApiAppConfig
from goToVladi.core.config.models.paths import Paths
from goToVladi.core.config.parser.paths import get_paths as get_common_paths

logger = logging.getLogger(__name__)


def create_app(config: ApiAppConfig) -> FastAPI:
    app = FastAPI(root_path=config.api.root_path)
    # app.include_router(routes.setup())
    # middlewares.setup(app, config)
    setup_metrics(
        app,
        MetricsConfig(
            app_name=config.app.name,
            include_metrics_endpoint=True,
            include_trace_exemplar=True,
        ),
    )

    return app


def get_paths() -> Paths:
    return get_common_paths("API_PATH")
