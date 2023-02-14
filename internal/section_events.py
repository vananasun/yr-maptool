
class Event:
    EVENTS_WITH_THIRD_PARAM = [ 60, 61 ]

    EVENT_NONE = 0
    EVENT_ENTERED_BY = 1
    EVENT_SPIED_BY = 2
    EVENT_THIEVED_BY = 3
    EVENT_DISCOVERED_BY_PLAYER = 4
    EVENT_HOUSE_DISCOVERED = 5
    EVENT_ATTACKED_BY_ANYBODY = 6
    EVENT_DESTROYED_BY_ANYBODY = 7
    EVENT_ANY = 8
    EVENT_DESTROYED_UNITS_ALL = 9
    EVENT_DESTROYED_BUILDINGS_ALL = 10
    EVENT_DESTROYED_ALL = 11
    EVENT_CREDITS_EXCEED = 12
    EVENT_ELAPSED_TIME = 13
    EVENT_MISSION_TIMER_EXPIRED = 14
    EVENT_DESTROYED_BUILDINGS = 15

    EVENT_LOCAL_IS_SET = 36
    EVENT_LOCAL_IS_CLEAR = 37
    EVENT_RANDOM_DELAY = 51
    EVENT_ENTERED_OR_OVERFLOWN_BY = 59
    EVENT_TECHTYPE_EXISTS = 60
    EVENT_TECHTYPE_DOES_NOT_EXIST = 61


    def __init__(self):
        self.num = 0
        self.conditions = []


    def from_string(self, key, val):
        """
        ID=NUM,E1,E1P1,E1P2
        ID1=NUM2,E1,E1P1,E1P2,E1P3,E2,E2P1,E2P2

        String 	Meaning
        ID 	    The Event's ID. Has to be the same as the Trigger's ID.
        NUM 	Amount of conditions in this Event.
        E1 	    The first condition (its index in the Available Events list)
        E1P1 	The first parameter for E1, defaults to 0
        E1P2 	The second parameter for E1, defaults to 0
        E1P3 	The third (optional) parameter for E1
        """
        txt = val.split(',')
        self.id = str(key)
        self.num = int(txt[0])
        
        c = 1
        for i in range(self.num):
            condition = [txt[c + 0], txt[c + 1], txt[c + 2]]
            if int(condition[0]) in self.EVENTS_WITH_THIRD_PARAM:
                condition.append(txt[c + 3])
                c += 1
            c += 3
            self.conditions.append(condition)
    
    def serialize(self):
        txt = '{}'.format(self.num)
        for cond in self.conditions:
            if int(cond[0]) in self.EVENTS_WITH_THIRD_PARAM:
                txt += ',{},{},{},{}'.format(cond[0], cond[1], cond[2], cond[3])
            else:
                txt += ',{},{},{}'.format(cond[0], cond[1], cond[2])
        return txt

    def __str__(self):
        txt = '{}\n\tNUM: {}'.format(self.id, self.num)
        for i in range(self.num):
            txt += '\n\tCONDITION {}, P1: {}, P2: {}'.format(
                self.conditions[i][0],
                self.conditions[i][1],
                self.conditions[i][2]
            )
            # 3rd param is optional
            if len(self.conditions[i]) == 4:
                txt += ', P3: {}'.format(self.conditions[i][3])
        return txt


class EventList():
    def __init__(self, section):
        self.events = []
        for key in section:
            event = Event()
            event.from_string(key, section[key])
            self.events.append(event)

    def write_to_ini(self, ini):
        ini.remove_section('Events')
        ini.add_section('Events')
        for event in self.events:
            ini.set('Events', str(event.id), event.serialize())

    def get_by_id(self, id):
        for event in self.events:
            if id == event.id:
                return event
        return None
