#-*- encoding: utf8 -*-
# Call with "python parseXML.py test.xml"
# Tested with Python 3.5

from tkinter import *
from tkinter.ttk import Treeview
from tkinter import filedialog
from generateFromXSD import GenXML
from xml_generator import XMLExporter
from generate_CSV import CSVexporter

import xml.etree.ElementTree as ET
import sys

#Class that holds all the functionality and most of the UI.
#Called from the main.py

class App:
    
    #Find right node
    def loopThroughNodeTree(self,node, comparisson_tree_node):
        ret = None
        
        if node.tree_node == comparisson_tree_node:
            return node
            
        if len(node.child_nodes) > 0:        
            for x in node.child_nodes:
                ret = self.loopThroughNodeTree(x, comparisson_tree_node)
                if ret != None:
                    break
                    
        return ret
          
                
    
    #Event handler on click
    def clicker(self, e):
        try:
            self.input_text.delete('1.0', END)
            selection = self.tree.focus()
            values = self.tree.item(selection, "values")
            self.input_text.insert('1.0', values[0])
        except:
            None
            
    
    #NEEDS TO CHANGE
    #Will update the value of a node in the tree.
    #Need to only update the function so only certain nodes can be changed.
    def updateNodeValue(self):
        try:
            selection = self.tree.focus()
            update_value = self.input_text.get('1.0', END)
            
            self.tree.item(selection, values=update_value)
            node_array = self.loopThroughNodeTree(self.root_node, selection)
            node_array.value = update_value
        except:
            None
    
    
    #NEEDS TO CHANGE
    #Will delete a node in the tree
    #Needs to change - only certain child nodes should be able to be deleted
    def deleteNodeValue(self):
        try:
            selection = self.tree.focus()
            node_array = self.loopThroughNodeTree(self.root_node, selection)
            del node_array
            self.tree.delete(selection)
            
            #Initiate printing based on XSD
            first_node = self.tree.insert("", 'end', None, text=self.root_node.name)
            self.root_node.tree_node = first_node
            self.print_nodes(first_node, self.root_node)
            
        except:
            None
    
    
    #Will loead a new XML tree based on XSD specifications    
    def loadXSD(self):
        filename = filedialog.askopenfilename(initialdir = "/", title = "Select XSD", filetypes = (("XSD schema", "*.xsd*"), ("all files", "*.*")))
        generator = GenXML(filename, "Document", True)
        
        #Cleanup of old tree
        self.root_node = None
        self.tree.delete(*self.tree.get_children())
        
        #Start running through the XSD
        self.root_node = generator.run()
       
        #Initiate printing based on XSD
        first_node = self.tree.insert("", 'end', None, text=self.root_node.name)
        self.root_node.tree_node = first_node
        self.print_nodes(first_node, self.root_node)
        
        
    #Save function for XML files
    def export_to_XML(self):
    # Opens the save dialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".xml",  # Default file extension
            filetypes=[("XML files", "*.xml"), ("All files", "*.*")])  # File type options in the dialog
        
        # If a file name is provided (i.e., the dialog is not canceled)
        if filename:
            exporter = XMLExporter
            exporter.export(self, self.root_node, filename)
        
    #Save function for CSV-files
    def export_to_CSV(self):
        f = filedialog.asksaveasfile(mode='w', defaultextension=".csv", filetypes = [("CSV", "*.csv*")])
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        savepath = str(f.name) # starts from `1.0`, not `0.0`
        CSVexporter(self.root_node, savepath)
    
    #def __init__(self, root, root_node):
    def __init__(self, root):
        self.tree = Treeview(root)
        
        #Setup buttons
        self.XSDloadbutton = Button(root, text="1. Load XSD-schema", command = self.loadXSD)
        #self.XMLloadbutton = Button(root, text="2. Load XML-schema") #To Be implemented
        self.ExportXMLbutton = Button(root, text="3. Export XML", command = self.export_to_XML)
        self.ExportCSVbutton = Button(root, text="3. Export CSV", command = self.export_to_CSV)
        self.update_value_button = Button(root, text="Update node value", command = self.updateNodeValue)
        self.duplicate_node_button = Button(root, text="Duplicate node")
        self.delete_node_button = Button(root, text="Delete node", command = self.deleteNodeValue)
        self.input_text = Text(root,height=2)
        
        #Configure row / columns to fill GUI
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(1, weight=1)
        
        #Place in GRID
        self.XSDloadbutton.grid(row = 0, column = 0, pady = 2, sticky=W)
        #self.XMLloadbutton.grid(row = 0, column = 1, pady = 2, sticky=W) #To Be implemented
        self.ExportXMLbutton.grid(row = 0, column = 2, pady = 2, sticky=E)
        self.ExportCSVbutton.grid(row = 0, column = 3, pady = 2, sticky=E)
        self.tree.grid(row = 1, column = 0, columnspan = 4, pady = 2, sticky="nsew")
        self.input_text.grid(row = 2, column = 0, pady = 2, sticky="nsew")
        self.update_value_button.grid(row = 2, column = 1, pady = 2, sticky="nsew")
        self.duplicate_node_button.grid(row = 2, column = 2, pady = 2, sticky="nsew")
        self.delete_node_button.grid(row = 2, column = 3, pady = 2, sticky="nsew")
        
        #Define and format columns
        self.tree['columns'] = ("Value")
        self.tree.column("#0", width=10, minwidth=10)
        self.tree.column("Value", anchor=CENTER, width=150, minwidth=50)
        
        #Define headings
        self.tree.heading("#0", text="Label", anchor=W)
        self.tree.heading("Value", text="Value", anchor=CENTER)
        
        #Define event binding
        self.tree.bind("<ButtonRelease-1>", self.clicker)
        
    #Function for putting out nodes in the UI
    def print_nodes(self, tree_parent_node, parent_node):
   
        if len(parent_node.child_nodes) > 0:
            for x in parent_node.child_nodes:
                new_tree_node = self.tree.insert(tree_parent_node, 'end', None, text=x.name)
                x.tree_node = new_tree_node
                self.print_nodes(new_tree_node, x)
        else:
            self.tree.item(tree_parent_node, values=(parent_node.value))
        

