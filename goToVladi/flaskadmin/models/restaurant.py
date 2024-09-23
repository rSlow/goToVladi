from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.form import InlineOneToOneModelConverter
from flask_admin.model import InlineFormAdmin

from goToVladi.core.data.db.models import RestaurantCuisine


class RestaurantView(ModelView):
    inline_models = [
        InlineOneToOneModelConverter(RestaurantCuisine),
    ]


class RestaurantCuisineInline(InlineFormAdmin):
    form_columns = ('title', 'date')
    inline_converter = InlineOneToOneModelConverter
