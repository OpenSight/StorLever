from operator import eq, gt, lt, ge, le

def version2float(context, request):
    request.matchdict['api_version'] = float(request.matchdict['api_version'])
    return True


def version_cmp(operator, target_version):
    def version_predicate(context, request):
        ver = float(request.matchdict['api_version'])
        request.matchdict['api_version'] = ver
        return operator(ver, target_version)
    return version_predicate