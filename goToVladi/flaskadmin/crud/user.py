from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from goToVladi.core.data.db import dto
from goToVladi.core.data.db import models as db


def upsert_user(user: dto.User, session: Session) -> dto.User:
    kwargs = {
        "tg_id": user.tg_id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "is_bot": user.is_bot,
    }
    session.execute(
        insert(db.User)
        .values(**kwargs)
        .on_conflict_do_update(
            index_elements=(db.User.tg_id,),
            set_=kwargs,
            where=db.User.tg_id == user.tg_id
        )
    )
    session.commit()

    saved_user = session.scalars(
        select(db.User)
        .where(db.User.tg_id == user.tg_id)
    ).one()
    return saved_user
