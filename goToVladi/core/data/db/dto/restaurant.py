from dataclasses import dataclass, field
from enum import Enum


class RestaurantType(Enum):
    DELIVERY = "DELIVERY"
    INNER = "INNER"


@dataclass
class RestaurantCuisine:
    name: str
    id_: int | None = None


@dataclass
class RestaurantPhone:
    phone: str
    id_: int | None = None


@dataclass
class RestaurantPhoto:
    url: str
    id_: int | None = None


@dataclass
class RestaurantSocial:
    url: str
    id_: int | None = None


@dataclass
class Restaurant:
    name: str
    average_check: int
    type_: RestaurantType
    rating: float
    cuisine: RestaurantCuisine

    id_: int | None = None
    priority: float | None = None
    site_url: str | None = None
    description: str | None = None

    phones: list[RestaurantPhone] = field(default_factory=list)
    photos: list[RestaurantPhoto] = field(default_factory=list)
    socials: list[RestaurantSocial] = field(default_factory=list)
