from collections import OrderedDict
from configparser import RawConfigParser
from .preview_base import PreviewBase

MSG_BAD_PREVIEW_SECTIONS = "Missing or invalid [Preview] and [PreviewPack] sections"
MSG_INVALID_PREVIEW_SIZE = "Preview size is invalid"

class MapFile:

    def __init__(self):
        self.ini = RawConfigParser(dict_type=OrderedDict, strict=False)
        self.ini.optionxform = str

    
    def from_file(self, map_path: str):
        self.ini.read(map_path)


    def save(self, filename: str):
        # Remove trailing semicolon comments on values
        for sect in self.ini.sections():
            for k in self.ini[sect]:
                val = self.ini.get(sect, str(k)).split(';')[0]
                self.ini.set(sect, str(k), val)

        self.reorder_sections()
        f = open(filename, "w")
        self.ini.write(f, space_around_delimiters=False)
        f.close()

    
    def set_name(self, name: str):
        self.ini.set("Basic", "Name", name)

    
    def set_preview(self, preview: PreviewBase):
        # [Preview] section
        size_value = "0,0,{},{}".format(preview.width, preview.height)
        self.ini.remove_section("Preview")
        self.ini.add_section("Preview")
        self.ini.set("Preview", "Size", size_value)

        # [PreviewPack] section
        packstr = preview.to_previewpack()
        self.ini.remove_section("PreviewPack")
        self.ini.add_section("PreviewPack")
        chunks = [packstr[i:i+70] for i in range(0, len(packstr), 70)]
        i = 1
        for chunk in chunks:
            self.ini.set("PreviewPack", str(i), chunk)
            i += 1


    def read_preview(self) -> PreviewBase:
        # Detect if the sections exist at all
        if not ('Preview' in self.ini and 'PreviewPack' in self.ini):
            raise Exception(MSG_BAD_PREVIEW_SECTIONS)
        
        # Detect if their section data is empty
        preview_empty = not len(self.ini['Preview'].keys())
        pack_empty = not len(self.ini['PreviewPack'].keys())
        if preview_empty or pack_empty:
            raise Exception(MSG_BAD_PREVIEW_SECTIONS)

        # @TODO: hidden preview detection

        # Read size
        width = int(self.ini['Preview']['Size'].split(',')[2])
        height = int(self.ini['Preview']['Size'].split(',')[3])
        if (width <= 0 or height <= 0):
            raise Exception(MSG_INVALID_PREVIEW_SIZE)
        
        # Gather PreviewPack string by summing up all the line values in the
        # [PreviewPack] section
        packstr = ''
        for key in self.ini['PreviewPack']:
            packstr += self.ini['PreviewPack'][key]

        # Decode the preview
        preview = PreviewBase()
        preview.from_previewpack(width, height, packstr)
        return preview


    def merge(self, filename: str, patch_mode: str):
        merged_map = MapFile()
        merged_map.from_file(filename)

        for section in merged_map.ini.sections():

            if patch_mode == "replace":
                self.ini.remove_section(section)

            if not self.ini.has_section(section):
                self.ini.add_section(section)
            elif patch_mode == "add":
                continue # do not replace or overwrite if only adding sections
            
            for key in merged_map.ini[section]:
                self.ini[section][key] = merged_map.ini[section][key]



    def reorder_sections(self):
        first = [
            'Header',
            'MultiplayerDialogSettings',
            'Basic',
            'Preview',
            'PreviewPack',
            'Map',
            'Lighting',
            'Triggers',
            'Actions',
            'Events',
            'Tags'
        ]
        last = [
            'General',
            'AircraftTypes',
            'VehicleTypes',
            'CellTags',
            'AITriggerTypesEnable',
            'SpecialFlags',

            'IsoMapPack5',
            'OverlayDataPack',
            'OverlayPack',
            'Structures',
            'Terrain',
            'TaskForces',
            'Houses',

            'Africans',
            'Alliance',
            'Americans',
            'Arabs',
            'British',
            'Confederation',
            'French',
            'GDI',
            'Germans',
            'Neutral',
            'Nod',
            'Russians',
            'Special',
            'YuriCountry',

            'FA2spVersionControl',
            'Digest'
        ]

        first.reverse()
        for name in first:
            if name in self.ini._sections:
                self.ini._sections.move_to_end(name, False)
        for name in last:
            if name in self.ini._sections:
                self.ini._sections.move_to_end(name, True)