from dishka import Scope, Provider, provide_all

from goToVladi.core.data.db.dao import UserDao, RegionDao, EventLogDao, RestaurantDao, HotelDao, \
    TripDao, MassageDao, CarRentDao, MessageTextDao, DeliveryDao, BarDao, BreakfastDao, \
    SeaRecreationDao, CooperationDao, SettingsDao


class DaoProvider(Provider):
    scope = Scope.REQUEST

    dao = provide_all(
        UserDao,
        RegionDao,
        EventLogDao,
        RestaurantDao,
        HotelDao,
        TripDao,
        MassageDao,
        CarRentDao,
        MessageTextDao,
        DeliveryDao,
        BarDao,
        BreakfastDao,
        SeaRecreationDao,
        CooperationDao,
        SettingsDao,
    )
