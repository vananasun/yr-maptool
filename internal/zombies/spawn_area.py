from internal.id_factory import IDFactory
from internal.coords import Coords
from internal.sections.section_actions import Action, ActionList
from internal.sections.section_events import Event, EventList
from internal.sections.section_tags import Tag, TagList
from internal.sections.section_taskforces import Taskforce, TaskforceList
from internal.sections.section_triggers import Trigger, TriggerList
from internal.sections.section_variablenames import LocalVariable, LocalVariableList
from internal.sections.section_waypoints import Waypoint, WaypointList
from internal.trigger_container import TriggerContainer
from internal.zombies.spawnpoint_info import SpawnpointInfo
import statistics
from math import sqrt


class SpawnArea:
    def __init__(self, area_json: dict, techtype_json: dict, id_factory: IDFactory()):
        
        self.name = area_json['name']
        self.techtype = techtype_json['techtype']
        self.num_units = techtype_json['taskforce_size']
        self.min_units = techtype_json['minimum']
        self.respawn_delay = area_json['respawn_delay']
        self.id_factory = id_factory
        self.taskforce = None

        self.trigs_enable = []
        self.trigs_disable = []
        self.trigger_enable_respawn_queue = None
        self.trigger_min_techtype = None

        self.var_is_respawning = LocalVariable()
        self.var_is_respawning.id = self.id_factory.next_var()
        self.var_is_respawning.name = 'spawn_{}_respawning'.format(self.name)
        self.var_is_respawning.default_state = '0'

        self.probabilities = {}


    def calc_spawnpoint_weights(self, waypoints: WaypointList, area_json: dict):
        
        # Gather all spawnpoint positions as integer coordinates,
        # also gather information about the width and height of the area
        positions_x = []
        positions_y = []
        min_x = 99999
        max_x = 0
        min_y = 99999
        max_y = 0
        median_pos = (0.0,0.0) # median position of all spawnpoints in this area
        furthest_dist = 9999999.0 # furthest euclidian distance of spawn to median
        num_waypoints = 0

        for spawnpoint_json in area_json['spawnpoints']:
            for waypoint in waypoints.waypoints:
                if waypoint.index == spawnpoint_json['waypoint_id']:
                    int_coords = Coords.from_txt(waypoint.coords_txt)
                    positions_x.append(int_coords.x)
                    positions_y.append(int_coords.y)
                    min_x = min(min_x, int_coords.x)
                    max_x = max(max_x, int_coords.x)
                    min_y = min(min_y, int_coords.y)
                    max_y = max(max_y, int_coords.y)
                    num_waypoints += 1


        # Calculate the mean
        median_pos = ((statistics.median(positions_x)), (statistics.median(positions_y)))

        # Calculate furthest dist
        ax = (max_x-median_pos[0])
        ay = (max_y-median_pos[1])
        bx = (median_pos[0]-min_x)
        by = (median_pos[1]-min_y)
        furthest_dist = max(sqrt((ax*ax)+(ay*ay)), sqrt((bx*bx)+(by*by)))

        # Calculate probability weights of spawnpoints
        for spawnpoint_json in area_json['spawnpoints']:
            for wp in waypoints.waypoints:
                if wp.index == spawnpoint_json['waypoint_id']:
                    wp_pos = Coords.from_txt(wp.coords_txt)
                    dx = abs(median_pos[0] - wp_pos.x)
                    dy = abs(median_pos[1] - wp_pos.y)
                    probability = sqrt((dx*dx)+(dy*dy)) / furthest_dist
                    # probability = min(max(0.0, probability), 1.0) # correct tiny errors by clamping
                    self.probabilities[wp.index] = probability

        # Divide probability weights by the list's sum
        weight_sum = sum(self.probabilities.values())
        for key, val in self.probabilities.items():
            self.probabilities[key] = val / weight_sum

        # Normalize values between 0 and 1
        min_prob = min(self.probabilities.values())
        max_prob = max(self.probabilities.values())
        if min_prob != max_prob:
            for key, val in self.probabilities.items():
                self.probabilities[key] = (val - min_prob) / (max_prob - min_prob)
            

    def calc_distributed_spawn_delay(self, waypoint: Waypoint):

        # Calculate random delay for the trigger
        actual_delay = (1.5 - self.probabilities[waypoint.index]) * (self.respawn_delay)

        # print('Waypoint {} - {}, delay: {}, base_delay: {}'.format(
        #     waypoint.index, round(self.probabilities[waypoint.index],2), round(actual_delay), self.respawn_delay
        # ))

        return round(actual_delay)



    def gen_taskforce(self, num_units):
        tf = Taskforce()
        tf.id = self.id_factory.next()
        tf.name = 'SPAWN - {} {} ({})'.format(self.name, num_units, self.techtype)
        tf.group = '-1'
        tf.lines = [ '{},{}'.format(num_units, self.techtype) ]
        self.taskforce = tf
        

    def gen_trigger_enable_spawnpoints(self):
        t = TriggerContainer(self.id_factory)
        t.setFlags(True, 2)
        t.setName('SPAWN - {} - enable spawnpoints ({})'.format(self.name, self.techtype))
        t.addCondition(Event.EVENT_LOCAL_IS_CLEAR, 0, self.var_is_respawning.id)
        t.addAction(Action.ACTION_SET_LOCAL, 0, self.var_is_respawning.id, 0, 0, 0, 0, 'A')
        self.trigs_enable.append(t)

    def gen_trigger_disable_spawnpoints(self):
        t = TriggerContainer(self.id_factory)
        t.setFlags(True, 2)
        t.setName('SPAWN - {} - disable spawnpoints ({})'.format(self.name, self.techtype))
        t.addCondition(Event.EVENT_ANY, 0, 0)
        t.addAction(Action.ACTION_CLEAR_LOCAL, 0, self.var_is_respawning.id, 0, 0, 0, 0, 'A')
        self.trigs_disable.append(t)


    def gen_trigger_min_techtype(self):
        """
        Generates a trigger that prevents the respawn queue trigger from firing
        when a certain number of units of the techtype are on the map.
        """
        trig_id = self.trigger_enable_respawn_queue.trigger.id
        t = TriggerContainer(self.id_factory)
        t.setFlags(False, 2)
        t.setName('SPAWN - {} - min techtype check ({})'.format(self.name, self.techtype))
        t.addCondition(Event.EVENT_TECHTYPE_EXISTS, 2, self.min_units, self.techtype)
        t.addAction(Action.ACTION_DISABLE_TRIGGER, 2, trig_id, 0, 0, 0, 0, 'A')
        t.addAction(Action.ACTION_ENABLE_TRIGGER, 2, trig_id, 0, 0, 0, 0, 'A')
        self.trigger_min_techtype = t


    def gen_trigger_respawn_queue_loop(self):
        t = TriggerContainer(self.id_factory)
        t.setFlags(False, 2)
        t.setName('SPAWN - {} - respawn queue loop ({})'.format(self.name, self.techtype))
        t.addCondition(Event.EVENT_ELAPSED_TIME, 0, 1) # 1 tick is probably the lowest
        t.addAction(Action.ACTION_ENABLE_TRIGGER, 2, self.trigs_enable[0].trigger.id, 0, 0, 0, 0, 'A')
        self.trigger_enable_respawn_queue = t



    def add_spawnpoint_trigger_to_group(self, t: TriggerContainer):
        
        self.trigs_enable[0].addAction(
            Action.ACTION_ENABLE_TRIGGER,
            2, t.trigger.id, 0, 0, 0, 0, 'A'
        )
        self.trigs_disable[0].addAction(
            Action.ACTION_DISABLE_TRIGGER,
            2, t.trigger.id, 0, 0, 0, 0, 'A'
        )

