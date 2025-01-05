from typing import Any


class DescriptionMixin:
    form_widget_args: dict[str, Any]

    def __new__(cls, *args, **kwargs):
        view = super().__new__(cls)

        if view.form_widget_args is None:
            view.form_widget_args = {}
        view.form_widget_args.setdefault("description", {})["rows"] = 8

        return view
