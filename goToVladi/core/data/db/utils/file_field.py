from libcloud.storage.drivers.local import LocalStorageDriver
from sqlalchemy_file.storage import StorageManager

from goToVladi.core.config import BaseConfig


def configure_storage(config: BaseConfig):
    container_name = "attachment"
    (config.upload_file_path / container_name).mkdir(
        parents=True, exist_ok=True
    )
    container = LocalStorageDriver(
        config.upload_file_path.as_posix()
    ).get_container(container_name)
    StorageManager.add_storage("default", container)
