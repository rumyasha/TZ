import fnmatch
from drf_spectacular.settings import spectacular_settings

def preprocess_exclude_path_format(endpoints, **kwargs):
    return [
        (path, path_regex, method, callback)
        for path, path_regex, method, callback in endpoints
        if not any(fnmatch.fnmatch(path, pattern) for pattern in spectacular_settings.EXCLUDE_PATHS)
    ]