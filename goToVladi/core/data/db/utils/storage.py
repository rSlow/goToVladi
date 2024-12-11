import logging
from contextlib import suppress
from pathlib import Path

from libcloud.storage.drivers.local import LocalStorageDriver
from libcloud.storage.types import ContainerAlreadyExistsError
from sqlalchemy_file.storage import StorageManager

logger = logging.getLogger(__name__)


def configure_storages(upload_path: Path):
    upload_path.mkdir(parents=True, exist_ok=True)
    driver = LocalStorageDriver(upload_path.as_posix())

    container_name = "attachments"

    with suppress(ContainerAlreadyExistsError):
        driver.create_container(container_name=container_name)

    container = driver.get_container(container_name)
    StorageManager.add_storage(name="default", container=container)

    logger.info(f"File storage with name {container_name} configured successfully")
