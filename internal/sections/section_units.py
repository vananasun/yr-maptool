
class Unit:

    def from_string(self, key, val):
        """
        OWNER,ID,HEALTH,X,Y,FACING,MISSION,TAG,VETERANCY,GROUP,HIGH,FOLLOWS_INDEX,
        AUTOCREATE_NO_RECRUITABLE,AUTOCREATE_YES_RECRUITABLE
        https://modenc.renegadeprojects.com/Units_(maps)
        """
        txt = val.split(',')
        self.id = key
        self.owner = txt[0]
        self.unit_id = txt[1]
        self.health = txt[2]
        self.x = txt[3]
        self.y = txt[4]
        self.facing = txt[5]
        self.mission = txt[6]
        self.tag_id = txt[7]
        self.veterancy = txt[8]
        self.group = txt[9]
        self.high = txt[10]
        self.follows_index = txt[11]
        self.autocreate_no_recruitable = txt[12]
        self.autocreate_yes_recruitable = txt[13]

    def serialize(self):
        txt = '{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(
            self.owner,
            self.unit_id,
            self.health,
            self.x,
            self.y,
            self.facing,
            self.mission,
            self.tag_id,
            self.veterancy,
            self.group,
            self.high,
            self.follows_index,
            self.autocreate_no_recruitable,
            self.autocreate_yes_recruitable
        )
        return txt
    
    def __str__(self):
        txt  = '{}\n'.format(self.id)
        txt += '\tOWNER: {}\n'.format(self.owner)
        txt += '\tUNIT ID: {}\n'.format(self.unit_id)
        txt += '\tHEALTH: {}\n'.format(self.health)
        txt += '\tX: {}\n'.format(self.x)
        txt += '\tY: {}\n'.format(self.y)
        txt += '\tFACING: {}\n'.format(self.facing)
        txt += '\tMISSION: {}\n'.format(self.mission)
        txt += '\tTAG ID: {}\n'.format(self.tag_id)
        txt += '\tVETERANCY: {}\n'.format(self.veterancy)
        txt += '\tGROUP: {}\n'.format(self.group)
        txt += '\tHIGH: {}\n'.format(self.high)
        txt += '\tFOLLOWS INDEX: {}\n'.format(self.follows_index)
        txt += '\tAUTOCREATE NO RECRUITABLE: {}\n'.format(self.autocreate_no_recruitable)
        txt += '\tAUTOCREATE YES RECRUITABLE: {}\n'.format(self.autocreate_yes_recruitable)
        return txt


class UnitList():
    def __init__(self, section):
        self.units = []
        for key in section:
            unit = Unit()
            unit.from_string(key, section[key])
            self.units.append(unit)

    def write_to_ini(self, ini):
        ini.remove_section('Units')
        ini.add_section('Units')
        for unit in self.units:
            ini.set('Units', str(unit.id), unit.serialize())
    