import os
from importlib import import_module

from python_bot.common.models import BaseModule


def is_writable(path):
    # Known side effect: updating file access/modified time to current time if
    # it is writable.
    try:
        with open(path, 'a'):
            os.utime(path, None)
    except (IOError, OSError):
        return False
    return True


def find_command(cmd, path=None, pathext=None):
    if path is None:
        path = os.environ.get('PATH', '').split(os.pathsep)
    if isinstance(path, str):
        path = [path]
    # check if there are funny path extensions for executables, e.g. Windows
    if pathext is None:
        pathext = os.environ.get('PATHEXT', '.COM;.EXE;.BAT;.CMD').split(os.pathsep)
    # don't use extensions if the command ends with one of them
    for ext in pathext:
        if cmd.endswith(ext):
            pathext = ['']
            break
    # check if we find the command on PATH
    for p in path:
        f = os.path.join(p, cmd)
        if os.path.isfile(f):
            return f
        for ext in pathext:
            fext = f + ext
            if os.path.isfile(fext):
                return fext
    return None


def load_module(params=None):
    if isinstance(params, str):
        entry = params
        params = None
    else:
        entry = params["entry"]
        params = params.get("params", None)

    try:
        # If import_module succeeds, entry is a path to an app module,
        # which may specify an module class with default_app_config.
        # Otherwise, entry is a path to an module class or an error.
        module = import_module(entry)

    except ImportError:
        # Track that importing as an app module failed. If importing as an
        # module class fails too, we'll trigger the ImportError again.
        module = None

        mod_path, cls_name = entry.rsplit('.', 1)

        # Raise the original exception when entry cannot be a path to an
        # module class.
        if not mod_path:
            raise

    else:
        try:
            # If this works, the app module specifies an module class.
            cls_name = module.default_module
            mod_path = entry
        except AttributeError:
            mod_path, cls_name = entry.rsplit('.', 1)

    # If we're reaching this point, we must attempt to load the module
    # class located at <mod_path>.<cls_name>
    mod = import_module(mod_path)
    try:
        cls = getattr(mod, cls_name)
    except AttributeError:
        if module is None:
            # If importing as an app module failed, that error probably
            # contains the most informative traceback. Trigger it again.
            import_module(entry)
        else:
            raise

    if not params:
        params = {}

    # Check for obvious errors. (This check prevents duck typing, but
    # it could be removed if it became a problem in practice.)
    if callable(cls):
        return cls(**params)

    if not issubclass(cls, BaseModule):
        raise ValueError(
            "'%s' isn't a subclass of BaseModule." % entry)

    # Entry is a path to an module class.
    return cls(**params)
