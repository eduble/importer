This repository shows how one can hook python import mechanism, to load code at any location.

# How to try it

Running `importer.py` will call its `test()` function.

```
$ python3 importer.py
mod.py has been loaded
$
```

You should see the same message.

Function `test()` starts by creating the following small file tree:
```
  <tmpdir> / subdir / __init__.py
  <tmpdir> / subdir / mod.py
```

File `__init__.py` is written with the following content:
```
from . import mod
```

File `mod.py` is written with the following content:
```
print('mod.py has been loaded')
```

After having built this testing environment, `test()` runs the following:
```
# activate our mechanism
sys.meta_path = sys.meta_path + [ Finder(env_root) ]
# try to import 'subdir', which will import mod.py because
# of its __init__.py file.
import subdir
```

# Going further

You may have noticed that `env_root` is a `pathlib.Path` object.
So it's really simple to target another location.
But you can do even more: if you provide a custom class which implements the same interface as `pathlib.Path`, then it will still work.
That means you can implement any sort of virtual filesystem, such as a filesystem stored on a remote node.

