class NFS(object):
    def __init__(self):
        self.share = None
        self.hosts = [{
            'host': '',
            'uid': None,
            'gid': None,
            'rootsquash': True,
            'sync': False,
            'params': []
        }]

    @classmethod
    def new(cls):
        pass

    def delete(self):
        pass

    def add_host(self):
        pass

    def delete_host(self):
        pass
