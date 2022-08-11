import gettext

t = gettext.translation("knowledge-panel", "/i18n")
_ = t.ugettext

print(_("Hello"))
