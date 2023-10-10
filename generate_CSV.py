import xml.etree.ElementTree as ET
import csv

#Class for taking a tree and exporting to CSV
class CSVexporter:
    
    def print_next_elem(self, parent_node, prev):
        if len(parent_node.child_nodes) > 0:
            self.array.append({"tag": prev + "." + parent_node.name, "text": ""})
            for i in parent_node.child_nodes:
                CSVexporter.print_next_elem(self, i, prev + "." + parent_node.name)
        else:
            self.array.append({"tag": prev + "." + parent_node.name, "text": parent_node.value})
            
    
    def log_in_csv(self, array_in, savepath):
        with open(savepath, 'a', newline='') as f:
            fieldnames = ['tag', 'text-r']
            writer = csv.DictWriter(f, delimiter=',', fieldnames=fieldnames)
            writer.writeheader()
            for x in array_in:
                if(x != ""):
                    try:
                        writer.writerow({'tag': x['tag'], 'text-r': x['text']})
                    except Exception as e:
                        print("Was unable to add the following entry: " + str(e)) 
    
    
    
    def __init__(self, root_node, savepath):
    
        self.array = []
        #Start to gather node names
        self.array.append({"tag": root_node.name, "text":""})
        if len(root_node.child_nodes) > 0:
            for i in root_node.child_nodes:
                CSVexporter.print_next_elem(self, i, root_node.name)

        #Add to CSV
        CSVexporter.log_in_csv(self, self.array, savepath)
        
    
       

               

