
class Structure:

    def from_string(self, key, val):
        """
        OWNER,ID,HEALTH,X,Y,FACING,TAG,AI_SELLABLE,AI_REBUILDABLE,
        POWERED_ON,UPGRADES,SPOTLIGHT,UPGRADE_1,UPGRADE_2,UPGRADE_3,
        AI_REPAIRABLE,NOMINAL
        https://modenc.renegadeprojects.com/Structures_(maps)
        """
        txt = val.split(',')
        self.id = key
        self.owner = txt[0]
        self.building_id = txt[1]
        self.health = txt[2]
        self.x = txt[3]
        self.y = txt[4]
        self.facing = txt[5]
        self.tag_id = txt[6] # @TODO relate to tag
        self.ai_sellable = txt[7]
        self.ai_rebuildable = txt[8]
        self.powered_on = txt[9]
        self.upgrades = txt[10]
        self.spotlight = txt[11]
        self.upgrade_1 = txt[12]
        self.upgrade_2 = txt[13]
        self.upgrade_3 = txt[14]
        self.ai_repairable = txt[15]
        self.nominal = txt[16]

    def serialize(self):
        txt = '{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(
            self.owner,
            self.building_id,
            self.health,
            self.x,
            self.y,
            self.facing,
            self.tag_id,
            self.ai_sellable,
            self.ai_rebuildable,
            self.powered_on,
            self.upgrades,
            self.spotlight,
            self.upgrade_1,
            self.upgrade_2,
            self.upgrade_3,
            self.ai_repairable,
            self.nominal
        )
        return txt
    
    def __str__(self):
        txt  = '{}\n'.format(self.id)
        txt += '\tOWNER: {}\n'.format(self.owner)
        txt += '\tBUILDING ID: {}\n'.format(self.building_id)
        txt += '\tHEALTH: {}\n'.format(self.health)
        txt += '\tX: {}\n'.format(self.x)
        txt += '\tY: {}\n'.format(self.y)
        txt += '\tFACING: {}\n'.format(self.facing)
        txt += '\tTAG ID: {}\n'.format(self.tag_id)
        txt += '\tAI SELLABLE: {}\n'.format(self.ai_sellable)
        txt += '\tAI REBUILDABLE: {}\n'.format(self.ai_rebuildable)
        txt += '\tPOWERED ON: {}\n'.format(self.powered_on)
        txt += '\tUPGRADES: {}\n'.format(self.upgrades)
        txt += '\tSPOTLIGHT: {}\n'.format(self.spotlight)
        txt += '\tUPGRADE 1: {}\n'.format(self.upgrade_1)
        txt += '\tUPGRADE 2: {}\n'.format(self.upgrade_2)
        txt += '\tUPGRADE 3: {}\n'.format(self.upgrade_3)
        txt += '\tAI REPAIRABLE: {}\n'.format(self.ai_repairable)
        txt += '\tNOMINAL: {}'.format(self.nominal)
        return txt


class StructureList():
    def __init__(self, section):
        self.structures = []
        for key in section:
            structure = Structure()
            structure.from_string(key, section[key])
            self.structures.append(structure)

    def write_to_ini(self, ini):
        ini.remove_section('Structures')
        ini.add_section('Structures')
        for s in self.structures:
            ini.set('Structures', str(s.id), s.serialize())
    