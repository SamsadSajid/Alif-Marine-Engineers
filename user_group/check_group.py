from django.contrib.auth.decorators import user_passes_test
from django.http import Http404


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        raise Http404
    return user_passes_test(in_groups)