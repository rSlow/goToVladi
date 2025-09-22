from fastapi import FastAPI, APIRouter

from dialog_schematic_manager import DialogSchematicManager


def register_manager(app: FastAPI, manager: DialogSchematicManager):
    schematic_router = APIRouter()

    async def get_schematic():
        ...

    
    app.state.schematic_manager = manager
