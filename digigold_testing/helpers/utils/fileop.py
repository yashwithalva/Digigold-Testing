def write_new_value(filename, value):
    f_extra = open(filename, 'w')
    f_extra.write(str(value))
    f_extra.close()


def read_order_value(filename):
    f_extra = open(filename, 'r')
    n = int(f_extra.readline())
    return n
