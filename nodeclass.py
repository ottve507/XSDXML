from tkinter import *
from tkinter.ttk import Treeview


#This class is used to represent the XML nodes in a tree. Populated with info based on XML schema
class Node:
    def __init__(self):
        self.min_occurrence = 0
        self.max_occurrence = 0
        self.name = "no_name"
        self.value = "no value provided"
        self.child_nodes = []
        self.tree_node = None
    
    def set_min_occurrence(self, min_occurrence):
        self.min_occurrence = min_occurrence

    def set_max_occurrence(self, max_occurrence):
        self.max_occurrence = max_occurrence
    
    def set_name(self, name):
        self.name = name
        
    def get_name(self):
        return self.name
    
    def set_value(self, value):
        self.value = value
    
    def append_child(self, node):
        self.child_nodes.append(node)
    
    def list_children(self,space):
        if len(self.child_nodes) > 0:
            for x in self.child_nodes:
                if(x.value != "no value provided"):
                    print(space + x.name + " -> " + x.value)
                else:
                    print(space + x.name)
                x.list_children(space + " ")
                