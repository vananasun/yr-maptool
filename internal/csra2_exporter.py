from configparser import RawConfigParser
from internal.map_file import MapFile


class CSRA2Exporter:

    def __init__(self, map: MapFile):
        self.map = map
        self.ini = map.ini
    

    def export(self):
        info = {}
        info['Name'] = self.ini.get('Basic', 'Name', fallback='')
        info['Author'] = self.ini.get('Basic', 'Author', fallback='')
        info['Briefing'] = self.ini.get('Basic', 'Briefing', fallback='')
        info['Theather'] = self.ini.get('Map', 'Theater', fallback='')

        # Cropped map dimensions
        sz = self.ini.get('Map', 'LocalSize', fallback='')
        if sz != '':
            sz = sz.split(',')
            width = int(sz[2]) - int(sz[0])
            height = int(sz[3]) - int(sz[1])
            sz = '{} by {}'.format(width, height)
        info['Size'] = sz

        # Count waypoints to get player count
        waypoints_present = 0
        for i in range(8):
            if self.ini.get('Waypoints', str(i), fallback='') != '':
                waypoints_present += 1
        info['Starts'] = str(waypoints_present)

        print(self.format_txt(info))



    def format_txt(self, info):
        txt = ''
        for key, val in info.items():
            txt += '{}\n{}\n\n'.format(key, val)
        return txt.rstrip() # removes trailing newlines



    ###
    #
    # Data collection
    #
    ###

    # def get_name(self):
        # return self.ini.get('Basic', 'Name', fallback='None')
