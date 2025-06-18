from dishka import Scope, Provider, provide_all

from goToVladi.core.data.db import dao


class DaoProvider(Provider):
    scope = Scope.REQUEST

    dao = provide_all(
        dao.UserDao,
        dao.RoleDao,
        dao.RegionDao,
        dao.EventLogDao,
        dao.RestaurantDao,
        dao.HotelDao,
        dao.TripDao,
        dao.MassageDao,
        dao.CarRentDao,
        dao.MessageTextDao,
        dao.DeliveryDao,
        dao.BarDao,
        dao.BreakfastDao,
        dao.SeaRecreationDao,
        dao.CooperationDao,
        dao.SettingsDao,
    )
