
class Infantry:
    def from_string(self, key, val):
        """
        OWNER,ID,HEALTH,X,Y,SUB_CELL,MISSION,FACING,TAG,VETERANCY,
        GROUP,HIGH,AUTOCREATE_NO_RECRUITABLE,AUTOCREATE_YES_RECRUITABLE
        """
        txt = val.split(',')
        self.id = str(key)
        self.owner = txt[0]
        self.infantry_id = txt[1]
        self.health = txt[2]
        self.x = txt[3]
        self.y = txt[4]
        self.sub_cell = txt[5]
        self.mission = txt[6]
        self.facing = txt[7]
        self.tag_id = txt[8]
        self.veterancy = txt[9]
        self.group = txt[10]
        self.high = txt[11]
        self.autocreate_no_recruitable = txt[12]
        self.autocreate_yes_recruitable = txt[13]
    
    def serialize(self):
        txt = '{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(
            self.owner,
            self.infantry_id,
            self.health,
            self.x,
            self.y,
            self.sub_cell,
            self.mission,
            self.facing,
            self.tag_id,
            self.veterancy,
            self.group,
            self.high,
            self.autocreate_no_recruitable,
            self.autocreate_yes_recruitable
        )
        return txt
    
    def __str__(self):
        txt = '{}\n'.format(self.id)
        txt += '\tOWNER: {}\n'.format(self.owner)
        txt += '\tINFANTRY ID: {}\n'.format(self.infantry_id)
        txt += '\tHEALTH: {}\n'.format(self.health)
        txt += '\tX: {}\n'.format(self.x)
        txt += '\tY: {}\n'.format(self.y)
        txt += '\tSUB CELL: {}\n'.format(self.sub_cell)
        txt += '\tMISSION: {}\n'.format(self.mission)
        txt += '\tFACING: {}\n'.format(self.facing)
        txt += '\tTAG ID: {}\n'.format(self.tag_id)
        txt += '\tVETERANCY: {}\n'.format(self.veterancy)
        txt += '\tGROUP: {}\n'.format(self.group)
        txt += '\tHIGH: {}\n'.format(self.high)
        txt += '\tAUTOCREATE NO RECRUITABLE: {}\n'.format(self.autocreate_no_recruitable)
        txt += '\tAUTOCREATE YES RECRUITABLE: {}\n'.format(self.autocreate_yes_recruitable)
        return txt


class InfantryList():
    def __init__(self, section):
        self.infantry = []
        for key in section:
            unit = Infantry()
            unit.from_string(key, section[key])
            self.infantry.append(unit)

    def write_to_ini(self, ini):
        ini.remove_section('Infantry')
        ini.add_section('Infantry')
        for infant in self.infantry:
            ini.set('Infantry', str(infant.id), infant.serialize())
        