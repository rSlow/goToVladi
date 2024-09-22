from enum import Enum

from aiogram.fsm.state import StatesGroup, State


class AdminSGFactory:
    class AdminStates(Enum):
        main = "main"
        add = "add"
        list = "list"
        delete = "delete"
        edit = "edit"

    def __init__(self, group_name: str):
        _states_group: StatesGroup = type(
            f"{group_name.capitalize()}AdminSG",
            (StatesGroup,),
            {state.name: State() for state in self.AdminStates},
        )
        self.__states_group = _states_group

    @property
    def main(self) -> State:
        return self.__states_group.main

    @property
    def add(self) -> State:
        return self.__states_group.add

    @property
    def edit(self) -> State:
        return self.__states_group.edit

    @property
    def list(self) -> State:
        return self.__states_group.list

    @property
    def delete(self) -> State:
        return self.__states_group.delete
