

class Tag:
    def from_string(self, key, val):
        txt = val.split(',')
        self.id = key
        self.persistence = txt[0]
        self.name = txt[1]
        self.trigger_id = txt[2]

    def serialize(self):
        txt = '{},{},{}'.format(self.persistence, self.name, self.trigger_id)
        return txt

    def __str__(self):
        return '{}\n\tPERSISTENCE: {}\n\tNAME: {}\n\tTRIGGER_ID: {}\n'.format(
            self.id, self.persistence, self.name, self.trigger_id
        )
    
    def __lt__(self, other):
        return (self.name < other.name)


class TagList():
    def __init__(self, section):
        self.tags = []
        for key in section:
            tag = Tag()
            tag.from_string(key, section[key])
            self.tags.append(tag)

    def sort(self):
        return sorted(self.tags)
    
    def get_by_id(self, id):
        for tag in self.tags:
            if id == tag.id:
                return tag
        return None

    def write_to_ini(self, ini):
        ini.remove_section('Tags')
        ini.add_section('Tags')
        for t in self.tags:
            ini.set('Tags', str(t.id), t.serialize())
    