from faststream.broker.core.usecase import BrokerUsecase

from . import mailing


def setup(broker: BrokerUsecase):
    broker.include_router(mailing.router)
