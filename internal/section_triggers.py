class Trigger:

    def __init__(self):
        self.house = 'Americans'
        self.linked_trigger = '<none>'
        self.easy = '1'
        self.normal = '1'
        self.hard = '1'
        self.persistence = '0' # deprecated in RA2/YR

    def from_string(self, key, val):
        txt = val.split(',')

        self.id = key
        self.house = txt[0]
        self.linked_trigger = txt[1]
        self.name = txt[2]
        self.disabled = txt[3]
        self.easy = txt[4]
        self.normal = txt[5]
        self.hard = txt[6]
        self.persistence = txt[7]
    
    def serialize(self):
        txt = '{},{},{},{},{},{},{},{}'.format(
            self.house,
            self.linked_trigger,
            self.name,
            self.disabled,
            self.easy,
            self.normal,
            self.hard,
            self.persistence,
        )
        return txt

    def __str__(self):
        return '{}\n\tHOUSE: {}\n\tLINKED_TRIGGER: {}\n\tNAME: {}\n\tDISABLED: {}\n\tEASY: {}\n\tNORMAL: {}\n\tHARD: {}\n\tPERSISTENCE: {}'.format(
            self.id, self.house, self.linked_trigger, self.name, self.disabled, self.easy, self.normal, self.hard, self.persistence
        )

    def __lt__(self, other):
        return (self.name < other.name)




class TriggerList():
    def __init__(self, section):
        self.triggers = []
        for key in section:
            trigger = Trigger()
            trigger.from_string(key, section[key])
            self.triggers.append(trigger)

    def sort(self):
        return sorted(self.triggers)

    def get_by_id(self, id):
        for k, v in enumerate(self.triggers):
            if id == v.id:
                return { k: v }
        return None

    def write_to_ini(self, ini):
        ini.remove_section('Triggers')
        ini.add_section('Triggers')
        for trigger in self.triggers:
            ini.set('Triggers', str(trigger.id), trigger.serialize())
    