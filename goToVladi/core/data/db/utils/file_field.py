from pathlib import Path

from libcloud.storage.drivers.local import LocalStorageDriver
from libcloud.storage.types import ContainerAlreadyExistsError
from sqlalchemy_file.storage import StorageManager


def configure_storage(upload_path: Path):
    upload_path.mkdir(parents=True, exist_ok=True)
    driver = LocalStorageDriver(upload_path.as_posix())

    container_name = "images"
    try:
        driver.create_container(container_name="images")
    except ContainerAlreadyExistsError:
        pass

    StorageManager.add_storage(
        name="restaurant_photos",
        container=driver.get_container(container_name)
    )
