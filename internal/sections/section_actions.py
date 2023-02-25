

class Action:

    ACTION_ENABLE_TRIGGER = 53
    ACTION_DISABLE_TRIGGER = 54
    ACTION_SET_LOCAL = 56
    ACTION_CLEAR_LOCAL = 57
    ACTION_REINFORCEMENT_BY_CHRONO = 107
    

    def __init__(self):
        self.num = 0
        self.actions = []

    def from_string(self, key, val):
        """
        ID=NUM,A1,A1P1,A1P2,A1P3,A1P4,A1P5,A1P6,A1P7
        ID=NUM,A1,A1P1,A1P2,A1P3,A1P4,A1P5,A1P6,A1P7,A2,A2P1,A2P2,A2P3,A2P4,A2P5,A2P6,A2P7

        String 	Meaning
        ID 	    The Action's ID. Has to be the same as the Trigger's ID.
        NUM 	Amount of actual actions in this Action.
        A1 	    The first action (its index in the Available Actions list)
        A1P1 	The first parameter for A1, defaults to 0
        A1P2 	The second parameter for A1, defaults to 0
        A1P3 	The third parameter for A1, defaults to 0
        A1P4 	The fourth parameter for A1, defaults to 0
        A1P5 	The fifth parameter for A1, defaults to 0
        A1P6 	The sixth parameter for A1, defaults to 0
        A1P7 	The seventh parameter for A1, defaults to 0
        """
        txt = val.split(',')
        self.id = str(key)
        self.num = int(txt[0])
        c = 1
        for i in range(self.num):
            action = [
                txt[c + 0], # action index
                txt[c + 1], # param 1
                txt[c + 2], # param 2
                txt[c + 3], # param 3
                txt[c + 4], # param 4
                txt[c + 5], # param 5
                txt[c + 6], # param 6
                txt[c + 7], # param 7
            ]
            self.actions.append(action)
            c += 8
    
    def serialize(self):
        txt = '{}'.format(self.num)
        for action in self.actions:
            txt += ',{},{},{},{},{},{},{},{}'.format(
                action[0],
                action[1],
                action[2],
                action[3],
                action[4],
                action[5],
                action[6],
                action[7],
            )
        return txt
        
    def __str__(self):
        txt = '{}\n\tNUM: {}'.format(self.id, self.num)
        for i in range(self.num):
            txt += '\n\tACTION {}: {} {} {} {} {} {} {} '.format(
                self.actions[i][0],
                self.actions[i][1],
                self.actions[i][2],
                self.actions[i][3],
                self.actions[i][4],
                self.actions[i][5],
                self.actions[i][6],
                self.actions[i][7],
            )
        return txt


class ActionList():
    def __init__(self, section):
        self.actions = []
        for key in section:
            action = Action()
            action.from_string(key, section[key])
            self.actions.append(action)
    
    def write_to_ini(self, ini):
        ini.remove_section('Actions')
        ini.add_section('Actions')
        for action in self.actions:
            ini.set('Actions', str(action.id), action.serialize())
        
    def get_by_id(self, id):
        for action in self.actions:
            if id == action.id:
                return action
        return None
