
class Taskforce:
    def from_section(self, id, section):
        """
        [01000016]
        0=1,ZOMA
        1=1,ZOMB
        2=1,ZOMC
        Name=Zombies 3
        Group=-1
        """
        self.id = id
        self.name = section['Name']
        self.group = section['Group']
        self.lines = []
        for i in range(len(section) - 2):
            self.lines.append(section[str(i)])
    
    def write_section(self, ini):
        ini.remove_section(self.id)
        ini.add_section(self.id)
        ini[self.id]['Name'] = self.name
        ini[self.id]['Group'] = self.group
        for i in range(len(self.lines)):
            ini.set(self.id, str(i), self.lines[i])
        
    def __lt__(self, other):
        return (self.name < other.name)


class TaskforceList:
    def __init__(self, ini):
        self.taskforces = []
        if 'Taskforces' in ini:
            for id in ini['TaskForces'].values():
                tf = Taskforce()
                tf.from_section(id, ini[id])
                self.taskforces.append(tf)

    def write_to_ini(self, ini):
        ids = []
        for tf in self.taskforces:
            tf.write_section(ini)
            ids.append(tf.id)
        
        ini.remove_section('TaskForces')
        ini.add_section('TaskForces')
        for idx, val in enumerate(ids):
            ini.set('TaskForces', str(idx), val)

    def sort(self):
        return sorted(self.taskforces)


