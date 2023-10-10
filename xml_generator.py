from tkinter import *
from tkinter.ttk import Treeview
from tkinter import filedialog
from generateFromXSD import GenXML
import xml.etree.cElementTree as ET

import xml.etree.ElementTree as ET
import sys

#Creates an xml file

class XMLExporter:
    
    def provide_children_to_parent(self, ET_parent_node, parent_node):
        if len(parent_node.child_nodes) > 0:
            for x in parent_node.child_nodes:
                child = ET.Element(x.name)
                ET_parent_node.append(child)
                XMLExporter.provide_children_to_parent(self, child, x)
        else:
            ET_parent_node.text = parent_node.value 
    
    #Find right node
    def export(self, root_node, filename):
        
        ET_root_node = ET.Element(root_node.name)
        XMLExporter.provide_children_to_parent(self, ET_root_node, root_node)
        tree = ET.ElementTree(ET_root_node)
        tree.write(filename)

       
                    
    
      
        
