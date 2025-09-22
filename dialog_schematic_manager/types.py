from aiogram.fsm.state import State

from .window_schema import WindowSchema

DialogSchematic = dict[State, WindowSchema]
