from threading import Timer


def set_interval(func, sec):
    # TODO: export to utils

    def func_wrapper():
        set_interval(func, sec)
        func()
    t = Timer(sec, func_wrapper)
    t.start()
    return t
