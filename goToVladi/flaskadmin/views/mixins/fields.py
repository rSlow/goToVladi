from flask_admin import expose
from flask_admin.model import BaseModelView


class NoReadonlyCreateView(BaseModelView):
    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        args_to_return_readonly: list[str] = []
        for field_name, args in self.form_widget_args.items():
            if args.get("readonly") is True:
                args["readonly"] = False
                args_to_return_readonly.append(field_name)
        view = super().create_view()
        for field_name in args_to_return_readonly:
            self.form_widget_args[field_name]["readonly"] = True
        return view
