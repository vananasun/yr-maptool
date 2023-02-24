from tkinter import *
from tkinter import ttk, filedialog
from tkinter.messagebox import askyesno, showerror
from internal.map_file import MapFile
from internal.gui.techtype_editor import TechtypeEditor
from internal.sort_triggers import TriggerSorter
from internal.zombies.gen_zombie_spawns import GenZombieSpawns
import json
from copy import deepcopy as deepcopy

MSG_ASK_NEWFILE = "Ahoy, matey! Ye be looking to chart a new course, eh? Are ye certain ye want to start fresh with a new file, leaving behind all yer previous work? Take heed, for this be a fateful decision that could lead ye to new treasures, or send ye down to Davy Jones' locker. If ye be feeling adventurous, then raise the sails and set a course for the horizon. But if ye be hesitant, then batten down the hatches and stick with yer current course. What say ye, me hearty?"
MSG_ASK_OPEN = "Arr, ye be treading treacherous waters, matey! Ye sure ye want to open a new file and lose all yer hard-earned progress? Think on it well, for once ye proceed, there be no turning back. If ye be ready to take the plunge, then heave ho and open that new file. But if ye be havin' second thoughts, then weigh the risks, and decide wisely. What say ye, me hearty?"
MSG_ASK_EXIT = 'Arr, me hearty! Ye be sure ye want to walk the plank and quit this fine vessel? Yer departure be a heavy blow to our crew, and we\'d be sad to see ye go. Think on it a moment, and weigh the consequences. If ye be certain, then hoist the Jolly Roger and be on yer way. But if ye have any doubts, then stay with us, and we\'ll sail the high seas together. What say ye, matey?'
MSG_ASK_DELETE_AREA = "Avast, matey! Ye sure ye wanna delete that area? Be like tearin' off a piece of yer treasure map. If it be useless, hoist the anchor and delete it. But if ye have doubts, weigh the risks. What say ye?"
MSG_ASK_EXPORT = "Arrr ye sure ye wanna overwrite the map file on export? If ye be certain, weigh anchor and proceed. If not, batten down the hatches and weigh the options."
MSG_ERR_WAYPOINTS = "Avast, ye scallywag! Ye've entered the waypoint list wrongly! Beware, sailing without proper waypoints be as dangerous as a kraken in a storm. Take care to plot yer course rightly or ye'll be heading straight into Davey Jones' locker. Ye best check yer list before ye set sail again, lest ye suffer a watery grave. Arrr!"


# def item_to_index(id):
#     return int(id[1:6])-1

def sanitize_entry_get(entry):
    try:
        value = int(entry.get())
        return value
    except TclError:
        return 0


class AreaList:
    def __init__(self, root: Tk, area_editor):
        self.area_editor = area_editor
        self.root = root
        
        # create frame
        frame = LabelFrame(self.root, text='Areas', width=80, height=435)
        frame.grid(row=0, column=0, sticky=N)
        
        # create table
        self.tree = ttk.Treeview(frame, height=19, columns=('#0',), selectmode='browse', show='tree')
        self.tree.grid(row=1, column=0, columnspan=2)
        self.tree.heading('0', text='Name', anchor='w')
        self.tree.column('0', width=60, minwidth=60, stretch=False, anchor=W)
        self.tree.bind("<ButtonRelease-1>", self.on_select)

        # buttons
        ttk.Button(frame, text='Insert', command=self.insert_area).grid(
            row=2, column=0, sticky=W+E)
        ttk.Button(frame, text='Delete', command=self.delete_area).grid(
            row=2, column=1, sticky=W+E)

        self.last_selection = None
        self.json = { 'areas': [] }


    def insert_area(self):
        self.save_selected_area()

        # copy or insert completely new
        if len(self.tree.selection()):
            copied_area = deepcopy(
                self.json['areas'][self.tree.index(self.tree.selection()[0])]
            )
            copied_area['name'] = "New Area"
            self.json['areas'].append(copied_area)
        else:
            self.json['areas'].append({
                "name": "New Area",
                "respawn_delay": 80,
                "celltag_disable_time": 30,
                "celltag_radius": 2,
                "techtypes": [
                    { "techtype": "ZOMA", "minimum": 10, "taskforce_size": 6 },
                ],
                "spawnpoints": [
                    { "waypoint_id": 150 }
                ]
            })

        # do the rest with the GUI
        id = self.tree.insert('', 'end', text='New Area')
        self.tree.selection_set(id)
        idx = self.tree.index(id)
        area_editor.load_area_json(
            self.json['areas'][idx]#, id
        )
        self.last_selection = id



    def delete_area(self):
        if len(self.tree.selection()):
            answer = askyesno('', MSG_ASK_DELETE_AREA)
            if not answer:
                return

            for selected_item in self.tree.selection():
                del self.json['areas'][self.tree.index(selected_item)]
                self.tree.delete(selected_item)
            area_editor.clear_fields()

            self.last_selection = None


    def load_json(self, json):
        self.last_selection = None
        self.json = json

        # clear area editor fields just in case
        area_editor.clear_fields()

        # remove all first and then fill with data
        for item in self.tree.get_children():
            self.tree.delete(item)
        for area in self.json['areas']:
            self.tree.insert('', 'end', text=area['name'])

        # select first area
        if len(self.tree.get_children()):
            first_id = self.tree.get_children()[0]
            area_editor.load_area_json(self.json['areas'][0])#, first_id)
            self.tree.selection_set(first_id)
            self.last_selection = first_id
        

    

    def on_select(self, event):
        self.save_selected_area()
        if len(self.tree.selection()):
            item_id = self.tree.selection()[0]
            idx = self.tree.index(item_id)
            area_editor.load_area_json(self.json['areas'][idx])
            self.last_selection = item_id


    def save_selected_area(self):
        if not self.last_selection or not len(self.tree.selection()):
            self.last_selection = None
            return
        index = self.tree.index(self.last_selection)
        self.json['areas'][index] = area_editor.serialize()
        area_editor.tree_techtypes.cancel_edit_techtype()

        # update name shown in list
        self.tree.item(self.last_selection, text=self.json['areas'][index]['name'])



    def serialize(self):
        self.save_selected_area()
        return self.json



class AreaEditor:
    def __init__(self, root: Tk):
        self.root = root
        
        self.frame_basic = LabelFrame(self.root, text='Area Editor', width=385, height=426)
        self.frame_basic.grid(row=0, column=1, columnspan=2, sticky=N+E)

        self.name = StringVar()
        self.label_name = Label(self.frame_basic)
        self.label_name.place(x=5, y=30, height=20, width=120, bordermode='ignore')
        self.label_name.configure(anchor='e')
        self.label_name.configure(justify='right')
        self.label_name.configure(text='Name')
        self.entry_name = Entry(self.frame_basic, textvariable=self.name)
        self.entry_name.place(x=125, y=30, height=20, width=250, bordermode='ignore')

        self.respawn_delay = IntVar()
        self.label_respawn = Label(self.frame_basic)
        self.label_respawn.place(x=5, y=55, height=20, width=120, bordermode='ignore')
        self.label_respawn.configure(anchor='e')
        self.label_respawn.configure(justify='right')
        self.label_respawn.configure(text='Respawn Delay')
        self.entry_respawn = Entry(self.frame_basic, textvariable=self.respawn_delay)
        self.entry_respawn.place(x=125, y=55, height=20, width=250, bordermode='ignore')
        
        self.celltag_disable_time = IntVar()
        self.label_disable_time = Label(self.frame_basic)
        self.label_disable_time.place(x=5, y=80, height=20, width=120, bordermode='ignore')
        self.label_disable_time.configure(anchor='e')
        self.label_disable_time.configure(justify='right')
        self.label_disable_time.configure(text='Celltag Disable Time')
        self.entry_disable_time = Entry(self.frame_basic, textvariable=self.celltag_disable_time)
        self.entry_disable_time.place(x=125, y=80, height=20, width=250, bordermode='ignore')
        
        self.celltag_radius = IntVar()
        self.label_radius = Label(self.frame_basic)
        self.label_radius.place(x=5, y=105, height=20, width=120, bordermode='ignore')
        self.label_radius.configure(anchor='e')
        self.label_radius.configure(justify='right')
        self.label_radius.configure(text='Celltag Radius')
        self.entry_radius = Entry(self.frame_basic, textvariable=self.celltag_radius)
        self.entry_radius.place(x=125, y=105, height=20, width=250, bordermode='ignore')
        
        self.tree_techtypes = TechtypeEditor(self.frame_basic, height=10, columns=("#0","#1","#2"), selectmode='browse')

        self.label_waypoints = Label(self.frame_basic)
        self.label_waypoints.configure(text='Waypoint list, comma separated: 151,152,156,...')
        self.label_waypoints.configure(anchor=W)
        self.label_waypoints.place(x=5, y=381, height=20, width=300, bordermode='ignore')
        self.entry_waypoints_var = StringVar()
        self.entry_waypoints = Entry(self.frame_basic, textvariable=self.entry_waypoints_var)
        self.entry_waypoints.place(x=5, y=381, width=300, height=25)
        self.btn_waypoints = ttk.Button(self.frame_basic, text='Update', command=self.update_waypoint_list)
        self.btn_waypoints.place(x=305, y=381, width=70, height=25)

        

    def update_waypoint_list(self):
        try:
            waypoints_txt = self.entry_waypoints_var.get().strip().split(',')
            waypoints = []
            for wp_txt in waypoints_txt:
                waypoints.append(int(wp_txt))
            sanitized_str = ','.join([str(wp) for wp in waypoints])
            self.entry_waypoints_var.set(sanitized_str)
        except ValueError:
            showerror('', MSG_ERR_WAYPOINTS)
            # self.entry_waypoints_var.set(sanitized_str)
            pass # @TODO: show fuckup msg box
        
        self.root.focus() # unfocus as a visual effect to indicate we did something



    def clear_fields(self):
        self.name.set('')
        self.respawn_delay.set('0')
        self.celltag_disable_time.set('0')
        self.celltag_radius.set('0')
        self.tree_techtypes.clear_fields()
        self.entry_waypoints_var.set('')


    def load_area_json(self, area_json):
        self.name.set(area_json['name'])
        self.respawn_delay.set(area_json['respawn_delay'])
        self.celltag_disable_time.set(area_json['celltag_disable_time'])
        self.celltag_radius.set(area_json['celltag_radius'])
        self.tree_techtypes.load_techtype_json(area_json['techtypes'])

        wp_str = ''
        for wp in area_json['spawnpoints']:
            wp_str += str(wp['waypoint_id']) + ','
        wp_str = wp_str[:-1]
        self.entry_waypoints_var.set(wp_str)

    def serialize(self):
        json_obj = {}
        json_obj['name'] = self.name.get()
        json_obj['respawn_delay'] = sanitize_entry_get(self.respawn_delay)
        json_obj['celltag_disable_time'] = sanitize_entry_get(self.celltag_disable_time)
        json_obj['celltag_radius'] = sanitize_entry_get(self.celltag_radius)
        json_obj['techtypes'] = self.tree_techtypes.serialize()

        waypoints_txt = self.entry_waypoints_var.get().strip().split(',')
        spawnpoints = []
        try:
            for wp_txt in waypoints_txt:
                spawnpoints.append({
                    'waypoint_id': int(wp_txt)
                })
        except ValueError:
            print('wp serialization err beware')
            pass
        json_obj['spawnpoints'] = spawnpoints
    
        return json_obj




###
### Actions
###


def action_new():
    answer = askyesno('', MSG_ASK_NEWFILE)
    if answer:
        area_list.load_json({'areas':[]}) # practically empty json


def action_open():
    answer = askyesno('', MSG_ASK_OPEN)
    if not answer:
        return
    filename = filedialog.askopenfilename()
    if ''==filename:
        return
    with open(filename) as f:
        spawn_json = json.load(f)
        area_list.load_json(spawn_json)
        root.title = filename


def action_save():
    filename = filedialog.asksaveasfilename(defaultextension='json')
    if ''==filename:
        return
    with open(filename, 'w') as f:
        json.dump(area_list.serialize(), f, indent=4)
        root.title = filename


def action_export_to_map():
    answer = askyesno('', MSG_ASK_EXPORT)
    if not answer:
        return
    filename = filedialog.asksaveasfilename(defaultextension=['map','yrm'])
    map = MapFile()
    map.from_file(filename)
    gen_zombie_spawns = GenZombieSpawns(map, area_list.serialize())
    gen_zombie_spawns.generate()
    map.save(filename)
    # map.from_file(filename)
    # trigger_sorter = TriggerSorter(map)
    # trigger_sorter.sort_triggers()
    # map.save(filename)




root = Tk()
root.geometry("645x435")
root.resizable(False, False)


menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=action_new)
filemenu.add_command(label="Open", command=action_open)
filemenu.add_command(label="Save", command=action_save)
filemenu.add_command(label="Export to map", command=action_export_to_map)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)


area_editor = AreaEditor(root)
area_list = AreaList(root, area_editor)





root.config(menu=menubar)
root.mainloop()



