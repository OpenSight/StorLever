class VG(object):
    def __init__(self):
        self.name = ''
        self.pvs = []
        self.lvs = []
        self.size = 0

    @property
    def available_size(self):
        pass

    def delete(self):
        pass

    def create_lv(self):
        pass

    def delete_lv(self):
        pass

    def grow(self):
        pass

    def shrink(self):
        pass

    def replace_pv(self):
        pass


class LV(object):
    def __init__(self):
        self.name = ''
        self.size = 0
        self.vg = None
        self.type = 'linear'
        self.stripe_size = 0
        self.stripe_number = 0
        self.mirror_number = 0

    def delete(self):
        pass

    def grow(self):
        pass

    def shrink(self):
        pass


