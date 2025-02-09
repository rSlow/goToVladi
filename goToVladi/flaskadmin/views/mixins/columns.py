class ColumnListEqualFiltersMixin:
    column_filters: list | None

    def __new__(cls, *args, **kwargs):
        view = super().__new__(cls)

        if view.column_filters is None:
            view.column_filters = []

        if view.column_list is None:
            view.column_list = []

        view.column_list.extend(view.column_filters)

        return view
