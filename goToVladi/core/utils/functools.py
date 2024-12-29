import inspect
from functools import wraps
from typing import Callable, TypeVar, ParamSpec, get_type_hints, Any

T = TypeVar("T")
P = ParamSpec("P")


def _get_filtered_kwargs(kwargs: dict[str, Any], hints: dict[str, Any]) -> dict[str, Any]:
    return {name: value for name, value in kwargs.items() if name in hints}


def hide_unused_kwargs(func: Callable[P, T]) -> Callable[P, T]:
    hints = get_type_hints(func)
    is_async = inspect.iscoroutinefunction(func)

    if is_async:
        @wraps(func)
        async def _original_async_func(*args: P.args, **kwargs: P.kwargs) -> T:
            filtered_kwargs = _get_filtered_kwargs(kwargs, hints)
            return await func(*args, **filtered_kwargs)

        return _original_async_func

    else:
        @wraps(func)
        def _original_sync_func(*args: P.args, **kwargs: P.kwargs) -> T:
            filtered_kwargs = _get_filtered_kwargs(kwargs, hints)
            return func(*args, **filtered_kwargs)

        return _original_sync_func
