

class Waypoint:
    def from_string(self, key, val):
        txt = val.split(';')[0].split(',')
        self.index = int(key)
        self.coords_txt = txt[0]
    
    def serialize(self):
        return '{}'.format(self.coords_txt)

    def __str__(self):
        return '{}\n\tCOORDS: {}\n'.format(self.index, self.coords_txt)
    
    def __lt__(self, other):
        return (self.index < other.index)
    
    @staticmethod
    def num_to_letter(n):
        if n < 26:
            return chr(65+n)
        else:
            return chr(64+int(n/26)) + chr(65+int(n%26))
        
    def to_letter(self):
        return Waypoint.num_to_letter(self.index)



class WaypointList():
    def __init__(self, section):
        self.waypoints = []
        for key in section:
            waypoint = Waypoint()
            waypoint.from_string(key, section[key])
            self.waypoints.append(waypoint)

    def sort(self):
        return sorted(self.waypoints)

    def write_to_ini(self, ini):
        ini.remove_section('Waypoints')
        ini.add_section('Waypoints')
        for wp in self.waypoints:
            ini.set('Waypoints', str(wp.index), wp.serialize())
    

    def find(self, wp_index: int):
        for wp in self.waypoints:
            if wp.index == wp_index:
                return wp
        return None