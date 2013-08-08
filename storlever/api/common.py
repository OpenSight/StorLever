from pyramid.view import view_config

class _rest_view(view_config):
    def __init__(self, **settings):
        method = self.__class__.__name__.split('_')[0].upper()
        ver_cmp_func = settings.pop('api_ver', None)
        custom_predicates = settings.pop('custom_predicates', [])
        custom_predicates.append(_api_ver_predicate(ver_cmp_func))
        super(_rest_view, self).__init__(request_method=method,
                                       custom_predicates=custom_predicates,
                                       **settings)
        

class get_view(_rest_view):
    pass

class post_view(_rest_view):
    pass

class put_view(_rest_view):
    pass

class delete_view(_rest_view):
    pass


def _api_ver_predicate(cmp_func):
    def predicate(context, request):
        ver = float(request.matchdict['api_version'])
        request.matchdict['api_version'] = ver
        if cmp_func:
            return cmp_func(ver)
        return True
    return predicate
