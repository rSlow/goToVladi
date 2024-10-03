from aiogram.enums import ContentType

TYPES_MATCHING = {
    ContentType.VIDEO: [
        "video/mpeg",
        "video/webm",
        "video/3gpp",
        "video/mp4",
    ],
    ContentType.PHOTO: [
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/bmp",
        "image/gif",
        "image/tiff",

    ],
    ContentType.AUDIO: [
        "audio/mpeg",
        "audio/wav",
        "audio/webm",
        "audio/aac",
        "audio/ogg",
        "audio/opus",
        "audio/3gpp"

    ],
    ContentType.DOCUMENT: [
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/pdf",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
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
        # if file_content_type.startswith("document"):
        #     return ContentType.DOCUMENT
        raise TypeError(f"Unknown content type '{file_content_type}'")
    return matched_content_type
