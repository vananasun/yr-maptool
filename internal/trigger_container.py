from internal.sections.section_tags import Tag, TagList
from internal.sections.section_triggers import Trigger, TriggerList
from internal.sections.section_events import Event, EventList
from internal.sections.section_actions import Action, ActionList
from internal.id_factory import IDFactory
from copy import deepcopy as deepcopy

class TriggerContainer:

    def __init__(self, id_factory: IDFactory):
        self.id_factory = id_factory
        self.trigger = Trigger()
        self.trigger.id = id_factory.next()
        self.tag = Tag()
        self.tag.id = id_factory.next()
        self.tag.trigger_id = self.trigger.id
        self.setFlags(False, 0)
        self.event = Event()
        self.event.id = self.trigger.id
        self.action = Action()
        self.action.id = self.trigger.id


    def setName(self, name: str):
        self.trigger.name = name
        self.tag.name = name

    
    def setFlags(self, disabled: bool, repeats: int):
        if disabled:
            self.trigger.disabled = '1'
        else:
            self.trigger.disabled = '0'
        self.tag.persistence = str(repeats)


    def addCondition(self, event_id: int, p1, p2, p3 = None):
        self.event.num += 1
        cond = [ str(event_id), str(p1), str(p2) ]
        if (p3 != None):
            cond.append(str(p3))
        self.event.conditions.append(cond)
    

    def addAction(self, action_id: int, p1=0, p2=0, p3=0, p4=0, p5=0, p6=0, p7=0):
        self.action.num +=1
        self.action.actions.append([
            action_id,
            str(p1), str(p2), str(p3), str(p4), str(p5), str(p6), str(p7)
        ])


    def splitTriggerActions(self) -> list['TriggerContainer']:
        """
        Splits a trigger with more actions than given number of actions into
        a chain of triggers as a workaround for the bug where more than 10
        actions will bug the trigger.
        """
        max_actions = 8 # 10 minus 2 because we also need space for an enable
                        # and disable action
        split_actions = [
            self.action.actions[i:i+max_actions] for i in range(0, len(self.action.actions), max_actions)
        ]
        num_chunks = len(split_actions)
        new_triggers = []

        for n in range(num_chunks):
            chunk = split_actions[n]

            # Create new TriggerContainer object unless this is the first
            # trigger in the chain, then we just use that object
            if n == 0:
                t = deepcopy(self)
                t.action.actions.clear()
                t.action.num = 0
            else:
                t = TriggerContainer(self.id_factory)
                t.setFlags(True, 2)
                t.addCondition(Event.EVENT_ANY, 0, 0)
            
            t.setName('{} ({})'.format(self.trigger.name, n + 1))

            # Add action to disable the current trigger after it fires
            t.addAction(Action.ACTION_DISABLE_TRIGGER, 2, t.trigger.id, 0, 0, 0, 0, 'A')

            # Insert the chunk of actions into the trigger
            for action_from_chunk in chunk:
                t.action.actions.append(action_from_chunk)
                t.action.num += 1

            new_triggers.append(t)

        # Add action to enable next trigger in the chain,
        # unless this is the last trigger in the entire chain.
        for i in range(len(new_triggers)):
            if i != len(new_triggers) - 1:
                new_triggers[i].addAction(
                    Action.ACTION_ENABLE_TRIGGER,
                    2, new_triggers[i+1].trigger.id, 0, 0, 0, 0, 'A'
                )

        # # Fix the first trigger's ID to be the original trigger's ID,
        # # this avoids weird bugs when calling this function later on
        # # in your program. Also fixes very first action to use this ID.
        # new_triggers[0].trigger.id = self.trigger.id
        # new_triggers[0].tag.id = self.tag.id
        # new_triggers[0].tag.trigger_id = self.trigger.id
        # new_triggers[0].event.id = self.trigger.id
        # new_triggers[0].action.id = self.trigger.id
        # new_triggers[0].action.actions[0] = [
        #     Action.ACTION_DISABLE_TRIGGER, 2, self.trigger.id, 0, 0, 0, 0, 'A'
        # ]

        return new_triggers