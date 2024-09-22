from aiogram.fsm.state import StatesGroup, State


class SGSingleFactory:
    def __init__(self, group_name: str, state_name: str | None = None):
        if state_name is None:
            state_name = group_name
        _states_group: StatesGroup = type(
            group_name, (StatesGroup,), {state_name: State()}
        )
        self.__states_group = _states_group

    @property
    def state(self):
        if self.__states_group is None:
            raise RuntimeError("state group has been not generated")
        _state = self.__states_group.__states__[0]
        return _state
