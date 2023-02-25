import json

from math import sqrt as sqrt
from internal.coords import Coords
from internal.id_factory import IDFactory
from internal.map_file import MapFile
from internal.sections.section_actions import Action, ActionList
from internal.sections.section_celltags import Celltag, CelltagList
from internal.sections.section_events import Event, EventList
from internal.sections.section_infantry import Infantry, InfantryList
from internal.sections.section_scripttypes import Script, ScriptList
from internal.sections.section_structures import Structure, StructureList
from internal.sections.section_tags import Tag, TagList
from internal.sections.section_taskforces import Taskforce, TaskforceList
from internal.sections.section_teamtypes import Team, TeamList
from internal.sections.section_triggers import Trigger, TriggerList
from internal.sections.section_units import Unit, UnitList
from internal.sections.section_variablenames import LocalVariable, LocalVariableList
from internal.sections.section_waypoints import Waypoint, WaypointList
from internal.trigger_container import TriggerContainer
from internal.zombies.spawn_area import SpawnArea
from internal.zombies.spawnpoint_info import SpawnpointInfo


class GenZombieSpawns:

    def __init__(self, map: MapFile, json: dict):
        self.map = map
        self.ini = map.ini

        self.teams = TeamList(self.ini)
        self.scripts = ScriptList(self.ini)
        self.taskforces = TaskforceList(self.ini)

        self.variables = LocalVariableList(self.ini)
        self.waypoints = WaypointList(self.ini['Waypoints'])
        self.celltags = CelltagList(self.ini)

        self.tags = TagList(self.ini['Tags'])
        self.triggers = TriggerList(self.ini['Triggers'])
        self.events = EventList(self.ini['Events'])
        self.actions = ActionList(self.ini['Actions'])

        self.id_factory = IDFactory()

        self.spawn_json = json
        # # Load spawnpoint data from a JSON file
        # with open(json_path) as f:
        #     self.spawn_json = json.load(f)
    

    def gen_script(self) -> Script():
        script = Script()
        script.id = self.id_factory.next()
        script.name = 'Guard by scattering (generated)'
        script.lines = [{
            'mission': '21',
            'argument': '0'
        }]
        self.scripts.scripts.append(script)
        return script


    def gen_spawn_celltag_logic(self, json: dict):
        local_vars = {}

        spawnpoint_list = []
        for area_json in json['areas']:
            for spawnpoint_json in area_json['spawnpoints']:
                spawnpoint_list.append(spawnpoint_json)
        
        for spawnpoint_json in spawnpoint_list:
            # Check whether the waypoint really exists and get it's position
            wp_id = spawnpoint_json['waypoint_id']
            wp_pos = None
            for waypoint in self.waypoints.waypoints:
                if waypoint.index == wp_id:
                    wp_pos = waypoint.coords_txt
            if wp_pos is None:
                # Just create it
                wp = Waypoint()
                wp.from_string(wp_id, '200001')
                self.waypoints.waypoints.append(wp)
                wp_pos = '200001'
                print('Warning: Specified waypoint {} does not exist, creating it...'.format(wp_id))

            # Generate activation variable which is used to determine whether
            # a spawnpoint was deactivated through it's celltags
            var = LocalVariable()
            var.id = self.id_factory.next_var()
            var.name = 'spawn_w{}_active'.format(wp_id)
            var.default_state = '1'
            local_vars[wp_id] = var
            self.variables.variables.append(var)

            # Generate enable trigger
            t = TriggerContainer(self.id_factory)
            t.setFlags(True, 2)
            t.setName('SPAWN - w{} re-enable timer'.format(wp_id))
            t.addCondition(Event.EVENT_ELAPSED_TIME, 0, area_json['celltag_disable_time'])
            t.addAction(Action.ACTION_SET_LOCAL, 0, var.id, 0, 0, 0, 0, 'A')
            t.addAction(Action.ACTION_DISABLE_TRIGGER, 2, t.trigger.id, 0, 0, 0, 0, 'A')
            enable_trigger = t # the disable trigger needs to refer to this one
            self.tags.tags.append(t.tag)
            self.triggers.triggers.append(t.trigger)
            self.events.events.append(t.event)
            self.actions.actions.append(t.action)

            # Generate disable trigger
            t = TriggerContainer(self.id_factory)
            t.setFlags(False, 2)
            t.setName('SPAWN - w{} disable by celltags'.format(wp_id))
            t.addCondition(Event.EVENT_ENTERED_BY, 0, -1)
            t.addAction(Action.ACTION_CLEAR_LOCAL, 0, var.id, 0, 0, 0, 0, 'A')
            t.addAction(Action.ACTION_DISABLE_TRIGGER, 2, enable_trigger.trigger.id, 0, 0, 0, 0, 'A')
            t.addAction(Action.ACTION_ENABLE_TRIGGER, 2, enable_trigger.trigger.id, 0, 0, 0, 0, 'A')
            disable_trigger = t
            self.tags.tags.append(t.tag)
            self.triggers.triggers.append(t.trigger)
            self.events.events.append(t.event)
            self.actions.actions.append(t.action)

            # Generate associated celltags
            radius = area_json['celltag_radius']
            center = Coords.from_txt(wp_pos)
            for y in range(center.y - radius, center.y + radius + 1):
                for x in range(center.x - radius, center.x + radius + 1):
                    
                    # # Calculate whether this point lies within the circumference
                    # # of a circle
                    # dx = x - center.x
                    # dy = y - center.y
                    # if sqrt((dx*dx)+(dy*dy)) > radius:
                    #     continue

                    # @TODO: Detect overwritten celltags
                    celltag = Celltag()
                    celltag.id = Coords.to_txt(Coords(x, y))
                    celltag.tag_id = disable_trigger.tag.id
                    self.celltags.celltags.append(celltag)

        return local_vars

            

    def remember_trigger(self, t: TriggerContainer):
        self.tags.tags.append(t.tag)
        self.triggers.triggers.append(t.trigger)
        self.events.events.append(t.event)
        self.actions.actions.append(t.action)        
    
    


    def generate(self):

        self.id_factory.rebase_index() # so we get some space for new stuff

        script = self.gen_script() # we only need one script for the entire system

        local_vars = self.gen_spawn_celltag_logic(self.spawn_json)

        for area_json in self.spawn_json['areas']:
        
            for techtype_json in area_json['techtypes']:

                area = SpawnArea(area_json, techtype_json, self.id_factory)
                area.gen_taskforce(techtype_json['taskforce_size'])
                area.gen_trigger_enable_spawnpoints()
                area.gen_trigger_disable_spawnpoints()
                area.gen_trigger_respawn_queue_loop()
                area.gen_trigger_min_techtype()
                area.calc_spawnpoint_weights(self.waypoints, area_json)

                self.remember_trigger(area.trigger_enable_respawn_queue)
                self.remember_trigger(area.trigger_min_techtype)
                self.taskforces.taskforces.append(area.taskforce)
                self.variables.variables.append(area.var_is_respawning)

            
                for spawnpoint_json in area_json['spawnpoints']:

                    print('Generating spawn at waypoint {} for area {} with techtype {}'.format(
                        spawnpoint_json['waypoint_id'], area_json['name'], techtype_json['techtype']
                    ))

                    spawn = SpawnpointInfo(
                        area,
                        self.waypoints.find(spawnpoint_json['waypoint_id']),
                        self.id_factory)
                    
                    spawn.gen_team(script, area.taskforce)
                    self.teams.teams.append(spawn.team)

                    spawn.gen_trigger_spawn(local_vars[spawnpoint_json['waypoint_id']])
                    self.remember_trigger(spawn.trigger_spawn)


                # Split group's spawnpoint enable & disable triggers as a workaround for
                # the stupid max trigger action bug.
                area.trigs_enable = area.trigs_enable[0].splitTriggerActions()
                area.trigs_disable = area.trigs_disable[0].splitTriggerActions()

                # ... And remember them in the ini
                for t in area.trigs_enable:
                    self.tags.tags.append(t.tag)
                    self.triggers.triggers.append(t.trigger)
                    self.events.events.append(t.event)
                    self.actions.actions.append(t.action)
                for t in area.trigs_disable:
                    self.tags.tags.append(t.tag)
                    self.triggers.triggers.append(t.trigger)
                    self.events.events.append(t.event)
                    self.actions.actions.append(t.action)



        # Write modified sections out to the map ini
        self.teams.write_to_ini(self.map.ini)
        self.scripts.write_to_ini(self.map.ini)
        self.taskforces.write_to_ini(self.map.ini)
        self.variables.write_to_ini(self.map.ini)
        self.waypoints.write_to_ini(self.map.ini)
        self.celltags.write_to_ini(self.map.ini)
        self.tags.write_to_ini(self.map.ini)
        self.triggers.write_to_ini(self.map.ini)
        self.events.write_to_ini(self.map.ini)
        self.actions.write_to_ini(self.map.ini)


