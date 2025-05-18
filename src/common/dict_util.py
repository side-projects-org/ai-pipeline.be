def deep_update(d1, d2):
    """
    Recursively update dictionary d1 with values from dictionary d2.
    """
    for k, v in d2.items():
        if isinstance(v, dict) and k in d1:
            deep_update(d1[k], v)
        else:
            d1[k] = v
    return d1