from __future__ import print_function
from multiprocessing import util, Process, Manager

import os

import leapp  # noqa: F401; pylint: disable=unused-import


def test_mp_is_patched():

    def child_fun(_lst):
        pid = os.fork()
        if not pid:
            os.execvpe('whatever', [], os.environ)
        else:
            os.wait()

    m = Manager()
    lst = m.list()

    p = Process(target=child_fun, args=(lst,))
    p.start()
    p.join()
    if lst:
        for el in lst:
            print(el)


def test_mp_workaround_applied():
    if getattr(util, 'os', None) is None:
        assert util.Finalize.__name__ == 'FixedFinalize'
