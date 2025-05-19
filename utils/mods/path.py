import os

class path:
    def join(*args):
        os.path.join(*args)

    def basename(path_):
        return os.path.basename(path_)

    def dirname(path_):
        return os.path.dirname(path_)

    def filename(path_):
        y = path.basename(path_)
        return y.split('.')[0]

    def ext(path_):
        y = path.basename(path_)
        return y.split('.')[1]
