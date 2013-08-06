from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'storlever'}

@view_config(route_name='test', renderer='json')
def test_view(request):
    return {'a':[1,2,3,4,5], 'b':{1:'a', 2:'b'}}

@view_config(route_name='fail', renderer='json')
def fail_view(request):
    raise Exception('Failure')
    return {'project': 'storlever'}


