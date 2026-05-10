import os


DEFAULT_FACTUS_API_VERSION = "v2"


def get_factus_api_version() -> str:
    version = os.getenv("FACTUS_API_VERSION", DEFAULT_FACTUS_API_VERSION).lower()
    return "v1" if version == "v1" else "v2"


def get_support_document_api_version() -> str:
    version = os.getenv("FACTUS_SUPPORT_DOCUMENT_API_VERSION", "v1").lower()
    return "v2" if version == "v2" else "v1"


def get_support_adjustment_api_version() -> str:
    version = os.getenv("FACTUS_SUPPORT_ADJUSTMENT_API_VERSION", "v1").lower()
    return "v2" if version == "v2" else "v1"
