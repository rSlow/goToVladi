from dataclasses import dataclass

from fastapi import UploadFile, File, Form
from pydantic import AnyHttpUrl

from goToVladi.core.data.db import models as db


@dataclass
class HotelInputForm:
    name: str = Form()
    district_id: int = Form()
    min_price: int = Form()

    site_url: AnyHttpUrl | None = Form(default=None)
    description: str | None = Form(default=None)
    promo_code: str = Form(default=None)

    medias: list[UploadFile] = File(default_factory=list)

    def to_model(self):
        return db.Hotel(
            name=self.name,
            district_id=self.district_id,
            site_url=self.site_url,
            description=self.description,
            min_price=self.min_price,
            promo_code=self.promo_code,
            medias=[db.HotelMedia(content=media) for media in self.medias],
        )
