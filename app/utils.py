def wrap_text(text, wrapper):
    """
    Utility function to wrap the given text in the given wrapper.
    E.g 'text' if wrapper = single_quotes
    """
    if wrapper == "single_quotes":
        return f"'{text}'"
    elif wrapper == "quotes":
        return f'"{text}"'
    elif wrapper == "bold":
        return f"<b>{text}</b>"
    elif wrapper == "italic":
        return f"<i>{text}</i>"
    elif wrapper == "underline":
        return f"<u>{text}</u>"
    else:
        return text  # if given wrapper isn't valid then return the given text.


def format_translation(string, values, wrap=True):
    """
    Utility function that takes a translated string and a dictionary
    containing values to be filled in the given translated string.
    If 'facet_value' key is present in values dict but its value is empty ("") or None.
    It removes that placeholder (i.e {facet_value}) from the translated string along
    with unnecessary spaces so that unnecessary spaces are not present
    if None was directly filled in it.

    For example:
    translated string: Answer robotoff questions about the {facet_value} {facet_name}
    values: {'facet_name': label, 'facet_value': None}

    Then this function makes sure that after formatting, the result is:
    "Answer robotoff questions about the label"
    and not "Answer robotoff questions about the  label"  i.e two spaces before label in this case.
    """

    if "facet_value" in values and not values.get("facet_value"):
        string = string.replace(" {facet_value}", "")
        string = string.replace("{facet_value} ", "")
        values.pop("facet_value")

    if wrap and "facet_value" in values:
        values["facet_value"] = wrap_text(values["facet_value"], "single_quotes")

    return string.format(**values)
