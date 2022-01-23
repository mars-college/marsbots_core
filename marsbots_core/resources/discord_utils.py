def is_mentioned(message, user):
    """
    Checks if a user is mentioned in a message.
    :param message: The message to check.
    :param user: The user to check.
    :return: True if the user is mentioned, False otherwise.
    """
    return user.id in [m.id for m in message.mentions]
