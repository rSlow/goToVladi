from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from goToVladi.core.data.db import dto
from goToVladi.core.data.db import models as db


def upsert(user: dto.User, session: Session) -> dto.User:
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


def get(user_id: int, session: Session) -> dto.User:
    res = session.scalars(
        select(db.User)
        .where(db.User.tg_id == user_id)
    )
    return res.one().to_dto()


def set_admin_rights(session: Session, ids: list[int], is_superuser: bool):
    session.execute(
        update(db.User)
        .where(db.User.id.in_(ids))
        .values(is_superuser=is_superuser)
    )
    session.commit()
