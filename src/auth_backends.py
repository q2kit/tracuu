from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.core.cache import cache


def _get_lock_key(username):
    return f"{settings.LOGIN_LOCK_KEY_PREFIX}{username}"


def _get_fail_key(username):
    return f"{settings.LOGIN_FAIL_KEY_PREFIX}{username}"


def is_user_locked(username):
    lock_key = _get_lock_key(username)
    return cache.get(lock_key)


def _record_failure(username):
    fail_key = _get_fail_key(username)
    lock_key = _get_lock_key(username)
    timeout = settings.LOGIN_LOCK_RETRY_AFTER_SECONDS

    try:
        failures = cache.incr(fail_key)
    except ValueError:
        cache.add(fail_key, value=1, timeout=timeout)
        failures = 1

    if failures >= settings.LOGIN_LOCK_MAX_FAILED_ATTEMPTS:
        cache.set(lock_key, value=True, timeout=timeout)


def _reset(username):
    fail_key = _get_fail_key(username)
    lock_key = _get_lock_key(username)
    cache.delete(fail_key)
    cache.delete(lock_key)


class LockableModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or is_user_locked(username):
            return None

        if user := super().authenticate(
            request,
            username=username,
            password=password,
            **kwargs,
        ):
            _reset(username)
            return user

        _record_failure(username)
        return None
