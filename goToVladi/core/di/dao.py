from dishka import Scope, provide, Provider, provide_all

from goToVladi.core.data.db.dao import DaoHolder, UserDao, RegionDao, EventLogDao, RestaurantDao, \
    HotelDao, TripDao


class DaoProvider(Provider):
    holder = provide(DaoHolder, scope=Scope.REQUEST)

    dao = provide_all(
        UserDao,
        RegionDao,
        EventLogDao,
        RestaurantDao,
        HotelDao,
        TripDao,
    )
