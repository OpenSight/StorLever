class Block(object):
    def __init__(self):
        self.size = 0
        self.dev_name = ''
        self.vendor = ''
        self.model = ''
        self.scsi = None
        self.raid = None


class SCSI(object):
    def __init__(self):
        self.host = 0
        self.channel = 0
        self.target = 0
        self.lun = 0

    def rescan(self):
        pass


class Raid(object):
    def __init__(self):
        self.raid_level = 0
        self.size = 0
        self.adapter = None


class Adapter(object):
    def __init__(self):
        self.type = ''
        self.vendor = ''
        self.pdisks = []
        self.vdisks = []

    def create_vdisk(self):
        pass

    def delete_vdisk(self):
        pass


class LSI(Adapter):
    def __init__(self):
        super(LSI, self).__init__()

    def create_vdisk(self):
        pass

    def delete_vdisk(self):
        pass


class MD(Adapter):
    def __init__(self):
        super(MD, self).__init__()

    def create_vdisk(self):
        pass

    def delete_vdisk(self):
        pass


