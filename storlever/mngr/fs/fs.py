class FS(object):
    def __init__(self):
        self.name = ''
        self.size = 0
        self.avail_size = 0
        self.free_size = 0
        self.lv = None
        self.type = 'ext4'
        self.stripe_size = 0

    @classmethod
    def mkfs(cls):
        pass

    def mount(self):
        pass

    def unmount(self):
        pass


class EXT4FS(FS):
    def __init__(self):
        super(EXT4FS, self).__init__()


class XFS(FS):
    def __init__(self):
        super(XFS, self).__init__()


class Share(object):
    def __init__(self):
        self.name = ''
        self.fs = None

    @classmethod
    def new(cls):
        pass

    def delete(self):
        pass