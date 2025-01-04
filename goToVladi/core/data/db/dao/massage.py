from sqlalchemy.orm import selectinload, joinedload

from goToVladi.core.data.db import models as db, dto
from goToVladi.core.data.db.dao import mixins
from goToVladi.core.data.db.dao.base import BaseDao


class MassageDao(BaseDao[db.Massage],
                 mixins.GetListWithRegion[dto.ListMassage],
                 mixins.GetWithRegionAndMedias[dto.Massage]):
    pass


def get_massage_options():
    return (
        joinedload(db.Massage.region),
        selectinload(db.Massage.medias),
    )
