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
