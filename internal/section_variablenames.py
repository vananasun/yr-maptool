
class LocalVariable:

    def from_string(self, key, val):
        self.id = str(key)
        txt = val.split(';')[0].split(',')
        self.name = txt[0]
        self.default_state = txt[1]

    def serialize(self):
        return '{},{}'.format(self.name, self.default_state)

    def __str__(self):
        return '{}\tNAME: {}\n\tDEFAULT STATE: {}\n'.format(self.id, self.name, self.default_state)





class LocalVariableList():
    def __init__(self, ini):
        self.variables = []
        if 'VariableNames' in ini:
            for key in ini['VariableNames']:
                var = LocalVariable()
                var.from_string(key, ini['VariableNames'][key])
                self.variables.append(var)


    def get_by_id(self, id):
        for k, v in enumerate(self.variables):
            if id == v.id:
                return { k: v }
        return None

    def write_to_ini(self, ini):
        ini.remove_section('VariableNames')
        ini.add_section('VariableNames')
        for var in self.variables:
            ini.set('VariableNames', str(var.id), var.serialize())
    