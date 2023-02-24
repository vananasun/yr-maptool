from tkinter import *
from tkinter import ttk



class TechtypeEditor(ttk.Treeview):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        self.place(x=5, y=125, width=370, height=200)
        self.heading('#0', text='Techtype', anchor=W)
        self.heading('#1', text='Total units', anchor=W)
        self.heading('#2', text='Taskforce size', anchor=W)
        self.column('#0', width=140, minwidth=140, stretch=False, anchor=W)
        self.column('#1', width=114, minwidth=114, stretch=False)
        self.column('#2', width=114, minwidth=114, stretch=False)
        self.bind("<Button-1>", self.save_techtype_changes)
        self.bind('<Double-1>', self.edit_cell)

        ttk.Button(master, text='New Techtype', command=self.new_techtype).place(
            x=5, y=325, width=120, height=25)
            
        ttk.Button(master, text='Remove Techtype', command=self.remove_techtype).place(
            x=125, y=325, width=120, height=25)
        
        self.entry = Text(self, width=15, height=1)
        self.entry.bind("<Return>", self.save_techtype_changes)
        self.entry.bind("<Escape>", self.cancel_edit_techtype)

        self.edit_mode = False
        self.edit_row = None
        self.edit_column = None
        self.edit_item = None
        


    def serialize(self):
        json_obj = []
        for row in self.get_children():
            item = self.item(row)
            json_obj.append({
                'techtype': item['text'],
                'minimum': item['values'][0],
                'taskforce_size': item['values'][1]
            })
        return json_obj
    

    def load_techtype_json(self, techtype_json):
        self.clear_fields()
        for obj in techtype_json:
            self.insert(
                '', 'end',
                text=obj['techtype'],
                values=(obj['minimum'], obj['taskforce_size'])
            )
        # # select first area
        # if len(self.tree.get_children()):
        #     first_id = self.tree.get_children()[0]
        #     area_editor.load_area_json(self.json['areas'][0])#, first_id)
        #     self.tree.selection_set(first_id)


    def clear_fields(self):
        for row in self.get_children():
            self.delete(row)


    def cancel_edit_techtype(self, event=None):
        if not self.edit_mode:
            return
        self.edit_mode = False
        self.entry.delete('1.0', END)
        self.entry.insert(END, '')
        self.entry.place_forget()
    
    def save_techtype_changes(self, event=None):
        if not self.edit_mode:
            return
        self.edit_mode = False

        new_text = self.entry.get(0.0, "end").strip()
        if len(new_text): # must have some text otherwise ignore it
            if self.edit_column == '#0':
                self.item(self.edit_item, text=new_text)
            else:
                self.set(self.edit_row, column=self.edit_column, value=new_text)
            
        # get rid of textbox
        self.entry.delete('1.0', END)
        self.entry.insert(END, '')
        self.entry.place_forget()

        # self.save_to_json()

    def new_techtype(self):
        techtype_json = {
            "techtype": "ZOMA", "minimum": 20, "taskforce_size": 6
        }
        item = self.insert(
            '', 'end',
            text=techtype_json['techtype'],
            values=(techtype_json['minimum'],techtype_json['taskforce_size'],)   
        )
        self.update()
        self.selection_set([item])


    def remove_techtype(self):
        for item in self.selection():
            self.delete(item)
        if len(self.get_children()):
            self.selection_set([self.get_children()[-1]])


    def edit_cell(self, event):
        self.save_techtype_changes()

        if not len(self.selection()):
            return
        for item in self.selection():
            column = self.identify_column(event.x)
            row = self.identify_row(event.y)
            self.edit_item = self.focus()
        if not len(column) or not len(row):
            return
        cn = int(str(column).replace('#', ''))
        rn = self.index(self.edit_item)#int(str(row).replace('I', ''))
        
        x_offsets = [0, 140, 140+114] # by column number
        widths = [140, 114, 114]
        self.entry.focus()
        self.entry.place(x=x_offsets[cn], y=25+rn*20, width=widths[cn])

        self.edit_mode = True
        self.edit_row = row
        self.edit_column = column


