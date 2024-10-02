from adaptix import Retort

from goToVladi.flaskadmin.config.models.admin import FlaskAdminConfig


def load_admin_config(data: dict, retort: Retort):
    return retort.load(data, FlaskAdminConfig)
