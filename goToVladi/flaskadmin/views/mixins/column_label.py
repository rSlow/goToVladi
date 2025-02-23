from sqlalchemy.orm import InstrumentedAttribute


class ColumnLabelMixin:
    def __new__(cls, *args, **kwargs):
        view = super().__new__(cls)

        if view.column_labels is None:
            view.column_labels = {}
        _sqla_labels = {}
        for column, value in view.column_labels.items():
            if isinstance(column, InstrumentedAttribute):  #
                _sqla_labels[column.key] = value
        view.column_labels.update(_sqla_labels)

        return view
