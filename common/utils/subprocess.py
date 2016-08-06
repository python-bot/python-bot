import os
from subprocess import PIPE

from psutil import Popen


def popen_wrapper(args, universal_newlines=True):
    p = Popen(args, shell=False, stdout=PIPE, stderr=PIPE,
              close_fds=os.name != 'nt', universal_newlines=universal_newlines)

    output, errors = p.communicate()
    return (
        output,
        errors,
        p.returncode
    )