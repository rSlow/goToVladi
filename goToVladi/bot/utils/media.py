from aiogram.enums import ContentType

TYPES_MATCHING = {
    ContentType.VIDEO: [
        "video/mp4"
    ],
    ContentType.PHOTO: [
        "image/jpeg",
        "image/png",
        "image/webp",
    ],
    ContentType.AUDIO: [
        "audio/mpeg",
        "audio/wav",
        "audio/x-wav",
    ],
    ContentType.DOCUMENT: [
        "document/pdf",
        "document/docx",
        "document/odt",
    ]
}

GENERATED_TYPE_MATCHING = {
    file_content_type: aiogram_content_type
    for aiogram_content_type, file_content_types in TYPES_MATCHING.items()
    for file_content_type in file_content_types
}


def as_aiogram_content_type(file_content_type: str) -> ContentType:
    matched_content_type = GENERATED_TYPE_MATCHING.get(file_content_type)
    if matched_content_type is None:
        if file_content_type.startswith("image"):
            return ContentType.PHOTO
        if file_content_type.startswith("video"):
            return ContentType.VIDEO
        if file_content_type.startswith("audio"):
            return ContentType.AUDIO
        if file_content_type.startswith("document"):
            return ContentType.DOCUMENT
        raise TypeError(f"Unknown content type '{file_content_type}'")
    return matched_content_type
