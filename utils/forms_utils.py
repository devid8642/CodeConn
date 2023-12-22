def add_attr(field, attr: str, value: str) -> None:
    """
    This function adds a value into a attr in forms.

    Ex: add_attr(email, class, email-field) inject a class
    email-field into the email field in .html file.
    """
    field.widget.attrs.update({attr: value})
