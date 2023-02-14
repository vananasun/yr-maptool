
class IDFactory:
    def __init__(self):
        self.current_index = 0
        self.var_index = 50
    
    def next(self):
        id = '01' + str(self.current_index).rjust(6, '0')
        self.current_index += 1
        return id
    
    def next_var(self):
        ret = self.var_index
        self.var_index += 1
        return ret
    
    def current_as_int(self):
        return self.current_index
    
    def rebase_index(self, new_index = 500000):
        self.current_index = new_index
    