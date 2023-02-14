
class Celltag:

    def from_string(self, key, val):
        self.id = str(key) # also is it's position
        self.tag_id = val.split(';')[0] # notice it's semicolon, not comma

    def serialize(self):
        return self.tag_id

    def __str__(self):
        return '{}\tTAG ID: {}'.format(self.id, self.tag_id)





class CelltagList():
    def __init__(self, ini):
        self.celltags = []
        if 'Celltags' in ini:
            for key in ini['Celltags']:
                celltag = Celltag()
                celltag.from_string(key, ini['Celltags'][key])
                self.celltags.append(celltag)


    def get_by_id(self, id):
        for k, v in enumerate(self.celltags):
            if id == v.id:
                return { k: v }
        return None

    def write_to_ini(self, ini):
        ini.remove_section('CellTags')
        ini.add_section('CellTags')
        for celltag in self.celltags:
            ini.set('CellTags', str(celltag.id), celltag.serialize())
    