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
        available_lang = gettext.find("knowledge-panel", "i18n")
        SUPPORTED_LANGUAGE = available_lang
        _default_lang = DEFAULT_LANGUAGE if SUPPORTED_LANGUAGE is None else lang


def get_translation():
    lang_translations = gettext.translation(
        "knowledge-panel",
        localedir=str(I18N_DIR),
        languages=[_default_lang],
    )
    _ = lang_translations.gettext
    return _
