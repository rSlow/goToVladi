from goToVladi.core.data.db.dto import BaseAttachment, FoodCuisine
from goToVladi.core.data.db.dto.base import BaseCardDto, BaseListCardDto
from goToVladi.core.data.db.dto.region import RegionMixin
from goToVladi.core.data.db.utils.dto_types import PhoneNumberType


class DeliveryMedia(BaseAttachment):
    restaurant_id: int


class ListDelivery(BaseListCardDto, RegionMixin):
    rating: float
    cuisine: FoodCuisine
    priority: float | None = None


class Delivery(BaseCardDto, RegionMixin):
    rating: float
    cuisine: FoodCuisine
    site_url: str | None = None
    phone: PhoneNumberType | None = None
    medias: list[DeliveryMedia]
