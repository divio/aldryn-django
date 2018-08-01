from aldryn_django.storage.mixins import GZippedStaticFilesMixin
from django.contrib.staticfiles.storage import (
    StaticFilesStorage,
    ManifestStaticFilesStorage,
)

class GZippedStaticFilesStorage(GZippedStaticFilesMixin,
                                StaticFilesStorage):
    pass


class ManifestGZippedStaticFilesStorage(GZippedStaticFilesMixin,
                                        ManifestStaticFilesStorage):
    pass
