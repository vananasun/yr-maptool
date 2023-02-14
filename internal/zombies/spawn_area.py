from internal.id_factory import IDFactory
from internal.section_actions import Action, ActionList
from internal.section_events import Event, EventList
from internal.section_tags import Tag, TagList
from internal.section_taskforces import Taskforce, TaskforceList
from internal.section_triggers import Trigger, TriggerList
from internal.section_variablenames import LocalVariable, LocalVariableList
from internal.trigger_container import TriggerContainer
from internal.zombies.spawnpoint_info import SpawnpointInfo


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

