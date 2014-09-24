def first_or_none(query_set):
    """
    Gets the first element from a query set or returns None is the set is empty (in absence of .first() in django 1.5).

    :param query_set: The query set to interrogate
    :return: The first element if the list is not empty, None otherwise
    """
    try:
        return query_set[0]
    except IndexError:
        return None
