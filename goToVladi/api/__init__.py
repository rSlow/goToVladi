import logging

from asgi_monitor.integrations.fastapi import setup_metrics, MetricsConfig
from fastapi import FastAPI

from goToVladi.api.apps import setup_routes
from goToVladi.api.config.models import ApiAppConfig

logger = logging.getLogger(__name__)


def create_app(config: ApiAppConfig) -> FastAPI:
    app = FastAPI(root_path=config.api.get_real_root_path(config.web.root_path))

    setup_routes(app, config)
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
