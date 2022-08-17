import gettext

# lang = ["en", "fr"]
lang_translations = gettext.translation(
    "knowledge-panel", localedir="i18n", languages=["fr"]
)
lang_translations.install()
_ = lang_translations.gettext
print(_("Hello World"))
