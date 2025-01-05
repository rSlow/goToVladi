class ColumnListEqualFiltersMixin:
    column_filters: list | None

    def __new__(cls, *args, **kwargs):
        view = super().__new__(cls)
        view.column_list = view.column_filters
        return view
