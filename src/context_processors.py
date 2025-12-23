from src.const import IMAGE_ALLOWED_TYPES, IMAGE_MAX_SIZE_MB


def configure_context_processors(request):  # noqa: ARG001
    return {
        "image_max_size_mb": IMAGE_MAX_SIZE_MB,
        "allowed_image_types": ", ".join(IMAGE_ALLOWED_TYPES),
    }
