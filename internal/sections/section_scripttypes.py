
class Script:
    def from_section(self, id, section):
        """
        [01000013]
        0=0,1
        Name=Attack Nearest
        """
        self.id = str(id)
        self.name = section['Name']
        self.lines = []
        for i in range(len(section) - 1):
            txt = section[str(i)].split(',')
            line = {
                'mission': txt[0],
                'argument': txt[1]
            }
            self.lines.append(line)
        
    def write_section(self, ini):
        ini.remove_section(self.id)
        ini.add_section(self.id)
        ini[self.id]['Name'] = self.name
        for idx, line in enumerate(self.lines):
            # Write "<int mission>,<int argument>"
            val = '{},{}'.format(line['mission'],  line['argument'])
            ini.set(self.id, str(idx), val);

    def __str__(self):
        txt = '{}\n\tNAME: {}'.format(self.id, self.name)
        for i in range(len(self.lines)):
            line = self.lines[i]
            txt += '\n\tMISSION: {}, {}'.format(line['mission'], line['argument'])
        return txt
    
    def __lt__(self, other):
        return self.name < other.name


class ScriptList:
    def __init__(self, ini):
        self.scripts = []
        if 'ScriptTypes' in ini:
            for script_id in ini['ScriptTypes'].values():
                script = Script()
                script.from_section(script_id, ini[script_id])
                self.scripts.append(script)

    def write_to_ini(self, ini):
        ids = []
        for s in self.scripts:
            s.write_section(ini)
            ids.append(s.id)
        
        ini.remove_section('ScriptTypes')
        ini.add_section('ScriptTypes')
        for idx, val in enumerate(ids):
            ini.set('ScriptTypes', str(idx), val)

    def sort(self):
        return sorted(self.scripts)