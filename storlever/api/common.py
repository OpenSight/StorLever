def version2float(context, request):
    request.matchdict['api_version'] = float(request.matchdict['api_version'])
    return True

