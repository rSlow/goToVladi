from fastadmin import settings

from goToVladi.api.config.models.admin import AdminConfig


def set_admin_settings(config: AdminConfig):
    setattr(settings, "settings", config)
