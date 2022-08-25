from app.i18n import active_translation
from app.i18n import translate as _

# note we rely on existing translations as it should not change so much over time.
EN_MSG = "Answer robotoff questions about"
FR_MSG = "Répondez aux questions de robotoff sur"


def test_active_translation():
    with active_translation(lang="fr"):
        assert _(EN_MSG) == FR_MSG
    with active_translation(lang="en"):
        assert _(EN_MSG) == EN_MSG


def test_no_active_translation_warning(caplog):
    assert _(EN_MSG) == EN_MSG
    assert any(
        "Looking up a translation while language was not set" in rec.message
        for rec in caplog.records
    )


def test_translation_fallback():
    with active_translation(lang="fr"):
        # message that is not translated
        assert _("blaaah") == "blaaah"


def test_active_translation_nesting():
    with active_translation(lang="fr"):
        assert _(EN_MSG) == FR_MSG
        with active_translation(lang="en"):
            assert _(EN_MSG) == EN_MSG
            with active_translation(lang="fr"):
                assert _(EN_MSG) == FR_MSG
            assert _(EN_MSG) == EN_MSG
        assert _(EN_MSG) == FR_MSG
