
class Team:
    
    def __init__(self):
        self.tag_id = ''

    def from_section(self, id, section):
        self.id = id
        self.name = section['Name']
        self.group = section['Group']
        self.house = section['House']
        self.script_id = section['Script']
        self.whiner = section['Whiner']
        self.droppod = section['Droppod']
        self.suicide = section['Suicide']
        self.loadable = section['Loadable']
        self.prebuild = section['Prebuild']
        self.priority = section['Priority']
        self.waypoint = section['Waypoint']
        self.annoyance = section['Annoyance']
        self.ion_immune = section['IonImmune']
        self.recruiter = section['Recruiter']
        self.reinforce = section['Reinforce']
        self.taskforce_id = section['TaskForce']
        self.tech_level = section['TechLevel']
        self.aggressive = section['Aggressive']
        self.autocreate = section['Autocreate']
        self.guard_slower = section['GuardSlower']
        self.on_trans_only = section['OnTransOnly']
        self.avoid_threats = section['AvoidThreats']
        self.loose_recruit = section['LooseRecruit']
        self.veteran_level = section['VeteranLevel']
        self.is_base_defense = section['IsBaseDefense']
        self.use_transport_origin = section['UseTransportOrigin']
        self.mind_control_decision = section['MindControlDecision']
        self.only_target_house_enemy = section['OnlyTargetHouseEnemy']
        self.transports_return_on_unload = section['TransportsReturnOnUnload']
        self.are_team_members_recruitable = section['AreTeamMembersRecruitable']
        if 'Max' in section:
            self.max = section['Max']
        else:
            self.max = ''
        if 'Full' in section:
            self.full = section['Full']
        else:
            self.full = ''
        if 'Tag' in section:
            self.tag_id = section['Tag']
        else:
            self.tag_id = ''

    def write_section(self, ini):
        ini.remove_section(self.id)
        ini.add_section(self.id)
        if self.max != '':
            ini[self.id]['Max'] = self.max
        if self.full != '':
            ini[self.id]['Full'] = self.full
        if self.tag_id != '':
            ini[self.id]['Tag'] = self.tag_id
        ini[self.id]['Name'] = self.name
        ini[self.id]['Group'] = self.group
        ini[self.id]['House'] = self.house
        ini[self.id]['Script'] = self.script_id
        ini[self.id]['Whiner'] = self.whiner
        ini[self.id]['Droppod'] = self.droppod
        ini[self.id]['Suicide'] = self.suicide
        ini[self.id]['Loadable'] = self.loadable
        ini[self.id]['Prebuild'] = self.prebuild
        ini[self.id]['Priority'] = self.priority
        ini[self.id]['Waypoint'] = self.waypoint
        ini[self.id]['Annoyance'] = self.annoyance
        ini[self.id]['IonImmune'] = self.ion_immune
        ini[self.id]['Recruiter'] = self.recruiter
        ini[self.id]['Reinforce'] = self.reinforce
        ini[self.id]['TaskForce'] = self.taskforce_id
        ini[self.id]['TechLevel'] = self.tech_level
        ini[self.id]['Aggressive'] = self.aggressive
        ini[self.id]['Autocreate'] = self.autocreate
        ini[self.id]['GuardSlower'] = self.guard_slower
        ini[self.id]['OnTransOnly'] = self.on_trans_only
        ini[self.id]['AvoidThreats'] = self.avoid_threats
        ini[self.id]['LooseRecruit'] = self.loose_recruit
        ini[self.id]['VeteranLevel'] = self.veteran_level
        ini[self.id]['IsBaseDefense'] = self.is_base_defense
        ini[self.id]['UseTransportOrigin'] = self.use_transport_origin
        ini[self.id]['MindControlDecision'] = self.mind_control_decision
        ini[self.id]['OnlyTargetHouseEnemy'] = self.only_target_house_enemy
        ini[self.id]['TransportsReturnOnUnload'] = self.transports_return_on_unload
        ini[self.id]['AreTeamMembersRecruitable'] = self.are_team_members_recruitable
    
    def __lt__(self, other):
        return (self.name < other.name)


class TeamList:
    def __init__(self, ini):
        self.teams = []
        if 'TeamTypes' in ini:
            for team_id in ini['TeamTypes'].values():
                team = Team()
                team.from_section(team_id, ini[team_id])
                self.teams.append(team)

    def write_to_ini(self, ini):
        ids = []
        for team in self.teams:
            team.write_section(ini)
            ids.append(team.id)
        
        ini.remove_section('TeamTypes')
        ini.add_section('TeamTypes')
        for idx, val in enumerate(ids):
            ini.set('TeamTypes', str(idx), val)
    
    def sort(self):
        return sorted(self.teams)