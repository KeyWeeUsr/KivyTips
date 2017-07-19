cdef extern from "hellolib.h":
    cdef char * hello()

def pyhello():
    return hello()

def pycharhello():
    cdef char * st = hello()
    return st
