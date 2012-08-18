import codecs
import os
import shutil
import StringIO
import tempfile


class Filelike(StringIO.StringIO):
    def __enter__(self):
        return self

    def __exit__(self, error_type, error_value, error_traceback):
        self.close()

    def seek(self, offset, whence=None):
        pass

    def read(self):
        return self.getvalue()


class FileModification(object):
    def __init__(self, transaction, filename):
        self.transaction = transaction
        self.filename = filename
        self.backup_path = None

    def execute(self):
        self.backup_path = self.transaction.generate_path()
        shutil.copy2(self.filename, self.backup_path)
        self.transaction.msg('backup', self.filename)

    def rollback(self):
        if not self.transaction.is_dry_run:
            shutil.copy2(self.backup_path, self.filename)
        self.transaction.msg('revert', self.filename)

    def commit(self):
        self.transaction.msg('append', self.filename)
        os.remove(self.backup_path)


class FileCreation(object):
    def __init__(self, transaction, filename):
        self.transaction = transaction
        self.filename = filename

    def execute(self):
        pass

    def commit(self):
        self.transaction.msg('create', self.filename)

    def rollback(self):
        if not self.transaction.is_dry_run:
            os.remove(self.filename)
        self.transaction.msg('revert', self.filename)


class DirectoryCreation(object):
    def __init__(self, transaction, dirname):
        self.transaction = transaction
        self.dirname = dirname

    def execute(self):
        if not self.transaction.is_dry_run:
            os.mkdir(self.dirname)
        self.transaction.msg('create', self.dirname)

    def commit(self):
        pass

    def rollback(self):
        if not self.transaction.is_dry_run:
            os.rmdir(self.dirname)
        self.transaction.msg('revert', self.dirname)


class FilesystemTransaction(object):
    def __init__(self, is_dry_run=False, delegate=None):
        self.is_dry_run = is_dry_run
        self.delegate = delegate
        self.log = []
        self.counter = 0
        self.temp_directory = tempfile.mkdtemp()

    def __enter__(self):
        return self

    def __exit__(self, error_type, error_value, error_traceback):
        if error_type is None:
            self.commit()
        else:
            self.rollback()

    def msg(self, action, msg):
        if hasattr(self.delegate, 'msg'):
            self.delegate.msg(action, msg)

    def generate_path(self):
        self.counter += 1
        return os.path.join(self.temp_directory, str(self.counter))

    def rollback(self):
        for entry in self.log:
            entry.rollback()

    def commit(self):
        for entry in self.log:
            entry.commit()

    def open(self, filename, mode):
        if os.path.exists(filename):
            modification = FileModification(self, filename)
        else:
            modification = FileCreation(self, filename)
        modification.execute()
        self.log.append(modification)
        if self.is_dry_run:
            return Filelike()
        else:
            return codecs.open(filename, encoding='utf-8', mode=mode)

    def mkdir(self, dirname):
        if os.path.exists(dirname):
            self.msg('exists', dirname)
        else:
            modification = DirectoryCreation(self, dirname)
            modification.execute()
            self.log.append(modification)
