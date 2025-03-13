"""i18n handling"""

import contextlib
import contextvars
import gettext
import logging

from .settings import I18N_DIR

log = logging.getLogger(__name__)


DEFAULT_LANGUAGE = "en"


# a cache of loaded translations
_translations = {}


def get_translation(lang):
    """Load a translations object, caching them"""
    if lang not in _translations:
        lang_translations = gettext.translation(
            "knowledge-panel",
            localedir=str(I18N_DIR),
            languages=[lang, DEFAULT_LANGUAGE],
        )
        _translations[lang] = lang_translations
    return _translations[lang]


# current language context vars manage the current language
_current_language = contextvars.ContextVar("current_language", default=None)


@contextlib.contextmanager
def active_translation(lang=None):
    """A context manager to set the language"""
    if lang is None:
        lang = DEFAULT_LANGUAGE
    # set current language
    token = _current_language.set(lang)
    yield
    # restore context
    _current_language.reset(token)


def get_current_lang():
    lang = _current_language.get()
    if lang is None:
        # warn
        log.warning(
            "Looking up a translation while language was not set. "
            "Use active_translation context manager",
            stack_info=True,
        )
        lang = DEFAULT_LANGUAGE
    return lang


def get_current_translation():
    """function to get translation object for current language"""
    return get_translation(get_current_lang())


def translate(message):
    """return getext translated message for current translation language"""
    return get_current_translation().gettext(message)
