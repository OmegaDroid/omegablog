def first_or_none(query_set):
    try:
        return query_set[0]
    except IndexError:
        return None
