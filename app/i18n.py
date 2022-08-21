import gettext


class TranslationStore:
    def lang(text=str):
        text = "fr"
        return text

    def load():
        lang_translations = gettext.translation(
            "knowledge-panel", localedir="i18n", languages=[TranslationStore.lang()]
        )
        lang_translations.install()
        _ = lang_translations.gettext
        return _
