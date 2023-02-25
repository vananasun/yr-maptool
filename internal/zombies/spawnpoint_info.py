from internal.id_factory import IDFactory
from internal.sections.section_actions import Action, ActionList
from internal.sections.section_events import Event, EventList
from internal.sections.section_scripttypes import Script
from internal.sections.section_tags import Tag, TagList
from internal.sections.section_taskforces import Taskforce, TaskforceList
from internal.sections.section_teamtypes import Team, TeamList
from internal.sections.section_triggers import Trigger, TriggerList
from internal.sections.section_variablenames import LocalVariable, LocalVariableList
from internal.sections.section_waypoints import Waypoint, WaypointList
from internal.trigger_container import TriggerContainer

try:
    from internal.zombies.spawn_area import SpawnArea
except ImportError:
    import sys
    SpawnArea = sys.modules[__package__ + '.spawn_area']


class SpawnpointInfo:
    def __init__(self, area: SpawnArea, waypoint: Waypoint, id_factory: IDFactory):
        self.id_factory = id_factory
        self.area = area
        self.team = None
        self.waypoint = waypoint
        # self.wp_index = waypoint_index
        # self.wp_letter = Waypoint.num_to_letter(waypoint_index)




    def gen_team(self, script: Script, taskforce: Taskforce):
        team = Team()
        team.id = self.id_factory.next()
        team.max = '5'
        team.name = 'SPAWN - {} - w{} ({})'.format(
            self.area.name, self.waypoint.index, self.area.techtype
        )
        team.full = 'yes'
        team.group = '-1'
        team.house = 'Russians'
        team.script_id = script.id
        team.whiner = 'no'
        team.droppod = 'no'
        team.suicide = 'no'
        team.loadable = 'no'
        team.prebuild = 'no'
        team.priority = '5'
        team.waypoint = 'A'
        team.annoyance = 'no'
        team.ion_immune = 'no'
        team.recruiter = 'no'
        team.reinforce = 'no'
        team.taskforce_id = taskforce.id
        team.tech_level = '0'
        team.aggressive = 'yes'
        team.autocreate = 'no'
        team.guard_slower = 'no'
        team.on_trans_only = 'no'
        team.avoid_threats = 'no'
        team.loose_recruit = 'no'
        team.veteran_level = '1'
        team.is_base_defense = 'no'
        team.use_transport_origin = 'no'
        team.mind_control_decision = '0'
        team.only_target_house_enemy = 'no'
        team.transports_return_on_unload = 'no'
        team.are_team_members_recruitable = 'no'
        self.team = team


    def gen_trigger_spawn(self, activation_var: LocalVariable):

        self.trigger_spawn = TriggerContainer(self.id_factory)
        self.trigger_spawn.setFlags(True, 2)
        self.trigger_spawn.setName('SPAWN - {} - w{} spawn ({})'.format(
            self.area.name, self.waypoint.index, self.area.techtype)
        )

        random_delay = self.area.calc_distributed_spawn_delay(self.waypoint)

        self.trigger_spawn.addCondition(Event.EVENT_RANDOM_DELAY, 0, random_delay)
        self.trigger_spawn.addCondition(Event.EVENT_LOCAL_IS_SET, 0, activation_var.id)
        self.trigger_spawn.addAction(
            Action.ACTION_REINFORCEMENT_BY_CHRONO,
            1, self.team.id, 0, 0, 0, 0, self.waypoint.to_letter()
        )
        self.trigger_spawn.addAction(
            Action.ACTION_ENABLE_TRIGGER,
            2, self.area.trigs_disable[0].trigger.id, 0, 0, 0, 0, 'A'
        )

        self.area.add_spawnpoint_trigger_to_group(self.trigger_spawn)
    

