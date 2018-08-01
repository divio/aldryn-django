import os
import shutil
import gzip

from django.core.files.storage import FileSystemStorage


class GZippedStaticFilesMixin(object):
    """
    Static files storage mixin to create a gzipped version of each static
    file, so that web servers (e.g. uWSGI) can take advantage of it and
    serve the optimized version.
    """
    gzip_ext = frozenset([
        '.html',
        '.css',
        '.js',
        '.json',
        '.svg',
        '.txt',
    ])

    def gzip_path(self, path):
        gz_path = path + '.gz'
        with self.open(path) as f_in:
            with self.open(gz_path, 'wb') as f_out:
                with gzip.GzipFile(fileobj=f_out) as gz_out:
                    shutil.copyfileobj(f_in, gz_out)
        return gz_path

    def iterfiles(self, path=''):
        dirs, files = self.listdir(path)
        for dir in dirs:
            for file in self.iterfiles(os.path.join(path, dir)):
                yield file
        for file in files:
            yield os.path.join(path, file)

    def post_process(self, paths, dry_run=False, **options):
        superclass = super(GZippedStaticFilesMixin, self)
        if hasattr(superclass, 'post_process'):
            post_processed = (
                superclass.post_process(paths, dry_run=dry_run, **options)
            )
        else:
            post_processed = []

        for processed in post_processed:
            yield processed

        if dry_run:
            return

        if not isinstance(self, FileSystemStorage):
            return

        for path in self.iterfiles():
            if os.path.splitext(path)[1] in self.gzip_ext:
                self.gzip_path(path)