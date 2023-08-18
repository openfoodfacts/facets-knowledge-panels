import os
import re
import unicodedata

import inflect
import pycountry

# Adapted from werkzeug source code (BSD-3-Clause license)
# to allow validating without transforming value tags

_filename_ascii_strip_re = re.compile(r"[^A-Za-z0-9_.\-:]")


def secure_filename(filename: str) -> str:
    r"""Pass it a filename and it will return a secure version of it.  This
    filename can then safely be stored on a regular file system and passed
    to :func:`os.path.join`.  The filename returned is an ASCII only string
    for maximum portability.

    >>> secure_filename("My cool movie.mov")
    'My_cool_movie.mov'
    >>> secure_filename("../../../etc/passwd")
    'etc_passwd'
    >>> secure_filename('i contain cool \xfcml\xe4uts.txt')
    'i_contain_cool_umlauts.txt'

    The function might return an empty filename.  It's your responsibility
    to ensure that the filename is unique and that you abort or
    generate a random filename if the function returned an empty one.

    :param filename: the filename to secure
    """
    filename = unicodedata.normalize("NFKD", filename)
    filename = filename.encode("ascii", "ignore").decode("ascii")

    for sep in os.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, " ")
    filename = str(_filename_ascii_strip_re.sub("", "_".join(filename.split()))).strip("._")

    return filename


def alpha2_to_country_name(value: str | None):
    """
    Helper function to return country name for aplha2 code
    """
    if value is not None and len(value) == 2:
        country = pycountry.countries.get(alpha_2=value)
        if country is not None:
            return f"{country.name}"
    return value


def country_name_to_alpha2(value: str | None):
    """
    Helper function that return alpha2 code for country name
    """
    country = pycountry.countries.get(name=value)
    if country is not None:
        return f"{(country.alpha_2).lower()}-en"
    return "world"


inflectEngine = inflect.engine()


def pluralize(facet: str):
    """Return plural form of facet."""
    return facet if facet == "packaging" else inflectEngine.plural_noun(facet)


def singularize(facet: str | None = None):
    """Return singular form of facet."""
    if facet is not None:
        singular_value = inflectEngine.singular_noun(facet)
        return facet if not singular_value else singular_value
