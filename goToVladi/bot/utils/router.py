from aiogram import Router, Dispatcher


def print_router_tree(router: Router, indent: int = 0) -> str:
    if isinstance(router, Dispatcher):
        result = " " * indent + "dispatcher"
    else:
        result = " " * indent + router.name

    for sub_router in router.sub_routers:
        result += "\n" + print_router_tree(sub_router, indent + 2)

    return result


def print_middleware_tree(router: Router, indent: int = 0) -> str:
    router_middlewares = []
    outer_router_middlewares = []
    if isinstance(router, Dispatcher):
        result = " " * indent + "dispatcher"
    else:
        result = " " * indent + router.name

    for sub_router in router.sub_routers:
        result += "\n" + print_middleware_tree(sub_router, indent + 2)

    return result
