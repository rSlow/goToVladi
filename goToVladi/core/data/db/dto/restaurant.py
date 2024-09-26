from dataclasses import dataclass, field
from enum import Enum

from .attachment import BaseAttachment


class HintedEnum(Enum):
    @property
    def _hints(self) -> dict[Enum, str]:
        raise {}

    @property
    def hint(self):
        return self._hints[self]


@dataclass
class RestaurantCuisine:
    name: str
    id_: int | None = None


@dataclass
class RestaurantMedia(BaseAttachment):
    restaurant_id: int


@dataclass
class ListRestaurant:
    name: str
    rating: float
    cuisine: RestaurantCuisine

    id_: int | None = None
    priority: float | None = None
    site_url: str | None = None
    phone: str | None = None


@dataclass
class Restaurant:
    name: str
    average_check: int
    rating: float
    cuisine: RestaurantCuisine

    medias: list[RestaurantMedia] = field(default_factory=list)

    is_delivery: bool = False
    is_inner: bool = True

    id_: int | None = None
    priority: float | None = None
    site_url: str | None = None
    description: str | None = None
    phone: str | None = None

    vk: str | None = None
    instagram: str | None = None
    whatsapp: str | None = None
    telegram: str | None = None
