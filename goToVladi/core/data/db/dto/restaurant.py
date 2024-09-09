from dataclasses import dataclass, field
from enum import Enum


class HintedEnum(Enum):
    @property
    def _hints(self) -> dict[Enum, str]:
        raise {}

    @property
    def hint(self):
        return self._hints[self]


class RestaurantType(HintedEnum):
    DELIVERY = "DELIVERY"
    INNER = "INNER"

    @property
    def _hints(self):
        return {
            self.DELIVERY: "Доставка",
            self.INNER: "На месте"
        }


@dataclass
class RestaurantCuisine:
    name: str
    id_: int | None = None


@dataclass
class Restaurant:
    name: str
    average_check: int
    type_: RestaurantType
    rating: float
    cuisine: RestaurantCuisine

    photos: list[str] = field(default_factory=list)

    id_: int | None = None
    priority: float | None = None
    site_url: str | None = None
    description: str | None = None
    phone: str | None = None

    vk: str | None = None
    instagram: str | None = None
    whatsapp: str | None = None
    telegram: str | None = None
