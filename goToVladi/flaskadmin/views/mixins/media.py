from typing import Any, Generic, TypeVar

from goToVladi.core.data.db.models.mixins import AttachmentProtocol
from goToVladi.core.utils.functools import get_generic_types
from goToVladi.flaskadmin.fields.file import SQLAlchemyMultipleFileUploadField
from goToVladi.flaskadmin.utils.media_inline import MediaInline

MediaRelation = TypeVar(
    "MediaRelation", bound=AttachmentProtocol,
    covariant=True, contravariant=False
)


class MediaFilesMixin(Generic[MediaRelation]):
    form_extra_fields: dict[str, Any] | None
    column_labels: dict[str, str] | None

    def __new__(cls, *args, **kwargs):
        view = super().__new__(cls)
        relation_class: type[MediaRelation] = get_generic_types(cls)[0]  # noqa

        if view.form_extra_fields is None:
            view.form_extra_fields = {}
        view.form_extra_fields["multi_media"] = SQLAlchemyMultipleFileUploadField(
            field_name="medias", relation_class=relation_class,
            label="Загрузка медиафайлов"
        )

        if view.column_labels is None:
            view.column_labels = {}
        view.column_labels["medias"] = "Медиафайлы"

        if view.inline_models is None:
            view.inline_models = []
        view.inline_models.append(MediaInline(relation_class))

        return view
