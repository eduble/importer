#!/usr/bin/env python
from importlib.abc import SourceLoader, MetaPathFinder
from importlib.machinery import ModuleSpec
from pathlib import Path
import sys

class Finder(MetaPathFinder):

    def __init__(self, root):
        MetaPathFinder.__init__(self)
        self.root = root

    def find_spec(self, fullname, path, target = None):
        location = self.root
        for mod in fullname.split("."):
            location = location / mod
        if location.is_dir():
            location = location / '__init__.py'
            return self.build_module_spec(fullname, location, True)
        location = location.with_suffix('.py')
        if location.exists():
            return self.build_module_spec(fullname, location, False)
        else:
            return None

    def build_module_spec(self, fullname, location, is_package):
        return ModuleSpec(  fullname,
                            Loader(self.root, location, is_package),
                            origin=str(location.relative_to(self.root)))

class Loader(SourceLoader):

    def __init__(self, root, location, is_package):
        SourceLoader.__init__(self)
        self.root = root
        self.is_package = is_package
        self.location = location

    def get_data(self, fullname):
        if self.location.exists():
            return self.location.read_bytes()
        else:
            return b''

    def get_filename(self, fullname):
        path = self.location
        return str(path.relative_to(self.root))

    def exec_module(self, module):
        if self.is_package:
            # make it a package
            module.__path__ = []
            module.__package__ = module.__name__
        super().exec_module(module)

def test():
    import tempfile
    with tempfile.TemporaryDirectory() as env_root:
        # create a small file tree to test our importing mechanism
        env_root = Path(env_root)
        subdir = env_root / 'subdir'
        subdir.mkdir()
        init_file = subdir / '__init__.py'
        mod_file = subdir / 'mod.py'
        init_file.write_text('from . import mod')
        mod_file.write_text('''print('mod.py has been loaded')''')
        # activate our mechanism
        sys.meta_path = sys.meta_path + [ Finder(env_root) ]
        # try to import 'subdir', which will import mod.py because
        # of its __init__.py file.
        import subdir

if __name__ == '__main__':
    test()
