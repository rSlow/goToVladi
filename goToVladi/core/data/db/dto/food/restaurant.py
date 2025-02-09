from goToVladi.core.data.db.dto import BaseAttachment, FoodCuisine
from goToVladi.core.data.db.dto.base import BaseCardDto, BaseListCardDto
from goToVladi.core.data.db.dto.region import RegionMixin
from goToVladi.core.data.db.utils.dto_types import PhoneNumberType


class RestaurantMedia(BaseAttachment):
    restaurant_id: int


class ListRestaurant(BaseListCardDto, RegionMixin):
    rating: float
    cuisine: FoodCuisine

    priority: float | None = None


class Restaurant(BaseCardDto, RegionMixin):
    average_check: int
    rating: float
    cuisine: FoodCuisine
    medias: list[RestaurantMedia]
    priority: float | None = None
    site_url: str | None = None
    phone: PhoneNumberType | None = None
