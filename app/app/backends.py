from ratelimitbackend.backends import RateLimitModelBackend


class MovementsAuthBackend(RateLimitModelBackend):
    minutes = 10
    requests = 50

    def key(self, request, dt):
        return '%s%s-%s-%s' % (
            self.cache_prefix,
            request.META.get('REMOTE_ADDR', ''),
            request.POST['username'],
            dt.strftime('%Y%m%d%H%M'),
        )
