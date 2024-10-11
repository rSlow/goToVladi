from faststream.broker.core.abc import ABCBroker

from . import mailing


def setup(broker: ABCBroker):
    broker.include_router(mailing.router)
