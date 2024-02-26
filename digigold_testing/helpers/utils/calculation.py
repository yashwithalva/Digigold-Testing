def round_down(num, precision):
    """
    Round down a float value on
    :param num: Double value to round down
    :param precision: Number of decimal places
    :return: double
    """
    s = '{}'.format(num)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(num, precision)
    i, p, d = s.partition('.')
    val = '.'.join([i, (d+'0'*precision)[:precision]])
    return float(val)
