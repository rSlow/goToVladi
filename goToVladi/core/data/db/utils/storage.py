import logging
from pathlib import Path

from libcloud.storage.drivers.local import LocalStorageDriver
from libcloud.storage.types import ContainerAlreadyExistsError
from sqlalchemy_file.storage import StorageManager

logger = logging.getLogger(__name__)


def configure_storages(upload_path: Path, storages: list[str]):
    upload_path.mkdir(parents=True, exist_ok=True)
    driver = LocalStorageDriver(upload_path.as_posix())

    container_name = "attachments"
    try:
        driver.create_container(container_name=container_name)
    except ContainerAlreadyExistsError:
        pass

    for storage in storages:
        StorageManager.add_storage(
            name=storage,
            container=driver.get_container(container_name)
        )
    if storages:
        logger.info(
            "Storages configured successfully: %s",
            "".join([f"\n - {storage}" for storage in storages])
        )
