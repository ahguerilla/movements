from storages.backends.s3boto import S3BotoStorage

# StaticRootS3BotoStorage = lambda: S3BotoStorage(location='static')
# MediaRootS3BotoStorage = lambda: S3BotoStorage(location='media')

class StaticRootS3BotoStorage(S3BotoStorage):
    """
    Storage for static files.
    """

    def __init__(self, *args, **kwargs):
        kwargs['location'] = 'static'
        super(StaticRootS3BotoStorage, self).__init__(*args, **kwargs)


class MediaRootS3BotoStorage(S3BotoStorage):
    """
    Storage for uploaded media files.
    """

    def __init__(self, *args, **kwargs):
        kwargs['location'] = 'media'
        super(MediaRootS3BotoStorage, self).__init__(*args, **kwargs)