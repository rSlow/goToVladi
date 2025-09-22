from dialog_schematic_manager.types import DialogSchematic


class DialogSchematicManager:
    def __init__(self, schematic: DialogSchematic):
        self.schematic = schematic

    def get_schematic_as_python(self):
        ...

    def get_schematic_as_json(self) -> dict:
        return {}
