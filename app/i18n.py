import gettext
import os
from .settings import I18N_DIR


class TranslationStore:
    def lang(lang_code=None):
        defualt_lang = "en"
        if lang_code is None:
            return defualt_lang
        else:
            os.environ["LANGUAGE"] = lang_code
            available_lang = gettext.find("knowledge-panel", "i18n")
            if available_lang is None:
                return defualt_lang
            else:
                return lang_code

    def load():
        lang_translations = gettext.translation(
            "knowledge-panel",
            localedir=str(I18N_DIR),
            languages=["fr"],
        )
        lang_translations.install()
        _ = lang_translations.gettext
        return _
