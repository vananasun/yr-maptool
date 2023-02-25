from internal.map_file import MapFile
from internal.sections.section_tags import Tag, TagList
from internal.sections.section_triggers import Trigger, TriggerList
from internal.sections.section_events import Event, EventList
from internal.sections.section_actions import Action, ActionList
from internal.sections.section_structures import Structure, StructureList
from internal.sections.section_units import Unit, UnitList
from internal.sections.section_infantry import Infantry, InfantryList
from internal.sections.section_teamtypes import Team, TeamList 
from internal.sections.section_scripttypes import Script, ScriptList
from internal.sections.section_taskforces import Taskforce, TaskforceList
from internal.sections.section_celltags import Celltag, CelltagList
from copy import deepcopy



class IDFactory:
    def __init__(self):
        self.current_index = 0
    
    def next(self):
        id = '01' + str(self.current_index).rjust(6, '0')
        self.current_index += 1
        return id
    
    def current_as_int(self):
        return self.current_index




class TriggerSorter():

    def __init__(self, map: MapFile):
        self.map = map
        self.ini = map.ini

        self.tags = TagList(self.ini['Tags'])
        self.triggers = TriggerList(self.ini['Triggers'])
        self.events = EventList(self.ini['Events'])
        self.actions = ActionList(self.ini['Actions'])
        self.structures = StructureList(self.ini['Structures'])
        self.units = UnitList(self.ini['Units'])
        self.infantry = InfantryList(self.ini['Infantry'])
        self.teams = TeamList(self.ini)
        self.scripts = ScriptList(self.ini)
        self.taskforces = TaskforceList(self.ini)
        self.celltags = CelltagList(self.ini)

        self.id_factory = IDFactory()



    def sort_triggers(self):

        # Remove all old IDs from ini
        # 01000168 is an example of a leftover section, has 3 refs, but 7 refs is the correct one
        # should be fixed now with these lines
        for team in self.teams.teams:
            self.ini.remove_section(team.id)
        for taskforce in self.taskforces.taskforces:
            self.ini.remove_section(taskforce.id)
        for script in self.scripts.scripts:
            self.ini.remove_section(script.id)


        # Sort triggers
        old_triggers = deepcopy(self.triggers.sort())
        old_tags = deepcopy(self.tags.tags)
        old_events = deepcopy(self.events.events)
        old_actions = deepcopy(self.actions.actions)
        sorted_triggers = deepcopy(old_triggers)

        for trig_index, trig in enumerate(old_triggers):
            new_id = self.id_factory.next()
            #sorted_triggers[trig_index] = trig

            for i, ref in enumerate(old_triggers): # correct linked triggers
                if ref.linked_trigger == trig.id:
                    sorted_triggers[i].linked_trigger = new_id
            
            for i, ref in enumerate(old_tags): # correct tags
                if ref.trigger_id == trig.id:
                    self.tags.tags[i].trigger_id = new_id
            
            for i, ref in enumerate(old_events): # correct events
                if ref.id == trig.id:
                    self.events.events[i].id = new_id
            
            for i, ref in enumerate(old_actions): # correct actions
                if ref.id == trig.id:
                    self.actions.actions[i].id = new_id
                for j, ref_line in enumerate(ref.actions):
                    TRIGGERS = [ 12, 22, 53, 54 ] # these reference a trigger in P2
                    if int(ref_line[0]) in TRIGGERS and ref_line[2] == trig.id:
                        self.actions.actions[i].actions[j][2] = new_id
                        
            sorted_triggers[trig_index].id = new_id

        self.triggers.triggers = sorted_triggers



        # Sort tags
        old_tags = deepcopy(self.tags.tags.sort())
        old_infantry = deepcopy(self.infantry.infantry)
        old_structures = deepcopy(self.structures.structures)
        old_units = deepcopy(self.units.units)
        old_teams = deepcopy(self.teams.teams)
        old_actions = deepcopy(self.actions.actions)
        old_celltags = deepcopy(self.celltags.celltags)
        sorted_tags = []

        for tag in self.tags.sort():
            new_id = self.id_factory.next()
            
            for i, ref in enumerate(old_infantry): # correct infantry
                if ref.tag_id == tag.id:
                    self.infantry.infantry[i].tag_id = new_id

            for i, ref in enumerate(old_structures): # correct structures
                if ref.tag_id == tag.id:
                    self.structures.structures[i].tag_id = new_id
            
            for i, ref in enumerate(old_units): # correct units
                if ref.tag_id == tag.id:
                    self.units.units[i].tag_id = new_id
            
            for i, ref in enumerate(old_teams): # correct teams
                if ref.tag_id == tag.id:
                    self.teams.teams[i].tag_id = new_id

            for i, ref in enumerate(old_actions): # correct actions
                for j, ref_line in enumerate(ref.actions):
                    TAGS = [ 70 ] # these reference a tag in P2
                    if int(ref_line[0]) in TAGS and ref_line[2] == tag.id:
                        self.actions.actions[i].actions[j][2] = new_id
            
            for i, ref in enumerate(old_celltags): # correct celltags
                if ref.tag_id == tag.id:
                    self.celltags.celltags[i].tag_id = new_id
        
            tag.id = new_id
            sorted_tags.append(tag)

        self.tags.tags = sorted_tags



        # Sort scripts
        old_scripts = deepcopy(self.scripts.sort())
        sorted_scripts = deepcopy(old_scripts) #{}

        for script_index, script in enumerate(old_scripts):
            new_id = self.id_factory.next()
            # sorted_scripts[script_index] = script

            # Update mission lines referencing scripts
            for i, ref in enumerate(old_scripts):
                for j, ref_line in enumerate(ref.lines):
                    # "Change Script" mission
                    if int(ref_line['mission']) == 17 and ref_line['argument'] == script.id:
                        sorted_scripts[i].lines[j]['argument'] = new_id

            for i, ref in enumerate(old_teams): # correct teams
                if ref.script_id == script.id:
                    self.teams.teams[i].script_id = new_id

            sorted_scripts[script_index].id = new_id

        # print('scripts {} -> {}'.format(len(old_scripts), len(sorted_scripts)))
        self.scripts.scripts = sorted_scripts
        
        
        # Sort teams
        old_actions = deepcopy(self.actions.actions)
        old_events = deepcopy(self.events.events)
        old_scripts = deepcopy(self.scripts.scripts)
        sorted_teams = []

        for team in self.teams.sort():
            new_id = self.id_factory.next()

            TEAM_ACTIONS = [ 4, 5, 7, 80, 104, 105, 107 ] # actions with team id as P2
            for i, ref in enumerate(old_actions):
                for j, action in enumerate(ref.actions):
                    if int(action[0]) in TEAM_ACTIONS and action[2] == team.id:
                        self.actions.actions[i].actions[j][2] = new_id

            TEAM_EVENTS = [ 23 ]
            for i, ref in enumerate(old_events):
                for j, condition in enumerate(ref.conditions):
                    if int(condition[0]) in TEAM_EVENTS and condition[2] == team.id:
                        self.events.events[i].conditions[j][2] = new_id
            
            for i, ref in enumerate(old_scripts):
                for j, ref_line in enumerate(ref.lines):
                    if int(ref_line['mission']) == 18:
                        self.scripts.scripts[i].lines[j]['argument'] = new_id

            team.id = new_id
            sorted_teams.append(team)
            
        # print('teams {} -> {}'.format(len(self.teams.teams), len(sorted_teams)))
        self.teams.teams = sorted_teams
        

        # Sort taskforces
        old_teams = deepcopy(self.teams.teams)
        sorted_taskforces = []

        for taskforce in self.taskforces.taskforces:
            new_id = self.id_factory.next()

            for i, ref in enumerate(old_teams):
                if ref.taskforce_id == taskforce.id:
                    self.teams.teams[i].taskforce_id = new_id

            taskforce.id = new_id
            sorted_taskforces.append(taskforce)

        # print('taskforces {} -> {}'.format(len(self.taskforces.taskforces), len(sorted_taskforces)))
        self.taskforces.taskforces = sorted_taskforces


        # Write everything out
        self.actions.write_to_ini(self.map.ini)
        self.events.write_to_ini(self.map.ini)
        self.infantry.write_to_ini(self.map.ini)
        self.scripts.write_to_ini(self.map.ini)
        self.structures.write_to_ini(self.map.ini)
        self.units.write_to_ini(self.map.ini)
        self.tags.write_to_ini(self.map.ini)
        self.taskforces.write_to_ini(self.map.ini)
        self.teams.write_to_ini(self.map.ini)
        self.triggers.write_to_ini(self.map.ini)
        self.celltags.write_to_ini(self.map.ini)


        print('Got {} IDs'.format(self.id_factory.current_as_int()))

        #for e in self.triggers.triggers: print(e)

        