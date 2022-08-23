import gettext
import os
from .settings import I18N_DIR


_default_lang = None
DEFAULT_LANGUAGE = "en"


def active_translation(lang=None):
    global _default_lang
    if lang is None:
        _default_lang = DEFAULT_LANGUAGE
    else:
        os.environ["LANGUAGE"] = lang
        supported_language = gettext.find("knowledge-panel", "i18n")
        _default_lang = DEFAULT_LANGUAGE if supported_language is None else lang


def get_translation():
    lang_translations = gettext.translation(
        "knowledge-panel",
        localedir=str(I18N_DIR),
        languages=[_default_lang],
    )
    _ = lang_translations.gettext
    return _
