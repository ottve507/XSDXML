from argparse import ArgumentParser
import xmlschema
from nodeclass import Node
from tkinter import *
from tkinter.ttk import Treeview

import xml.etree.ElementTree as ET
import sys
from xmlschema.validators import (
    XsdElement,
    XsdAnyElement,
    XsdComplexType,
    XsdAtomicBuiltin,
    XsdSimpleType,
    XsdList,
    XsdUnion)
    
    
#This file is used to understand the XSD-file and to support the generation of a UI tree.
#The functions are called from the file "generate_tree.py"

# sample data is hardcoded (XML example)
def valsmap(v):
    # numeric types
    v['decimal']    = '-3.72'
    v['float']      = '-42.217E11'
    v['double']     = '+24.3e-3'
    v['integer']    = '-176'
    v['positiveInteger'] = '+3'
    v['negativeInteger'] = '-7'
    v['nonPositiveInteger'] = '-34'
    v['nonNegativeInteger'] = '35'
    v['long'] = '567'
    v['int'] = '109'
    v['short'] = '4'
    v['byte'] = '2'
    v['unsignedLong'] = '94'
    v['unsignedInt'] = '96'
    v['unsignedShort'] = '24'
    v['unsignedByte'] = '17'
    # time/duration types
    v['dateTime'] = '2004-04-12T13:20:00-05:00'
    v['date'] = '2004-04-12'
    v['gYearMonth'] = '2004-04'
    v['gYear'] = '2004'
    v['duration'] = 'P2Y6M5DT12H35M30S'
    v['dayTimeDuration'] = 'P1DT2H'
    v['yearMonthDuration'] = 'P2Y6M'
    v['gMonthDay'] = '--04-12'
    v['gDay'] = '---02'
    v['gMonth'] = '--04'
    # string types
    v['string'] = 'lol'
    v['normalizedString'] = 'The cure for boredom is curiosity.'
    v['token'] = 'There is no cure for curiosity.'
    v['language'] = 'en-US'
    v['NMTOKEN'] = 'A_BCD'
    v['NMTOKENS'] = 'ABCD 123'
    v['Name'] = 'myElement'
    v['NCName'] = '_my.Element'
    v['Max35Text'] = "AbcdefghijklmnopqrstuvwxtzAbcdefghi"
    # magic types
    v['ID'] = 'IdID'
    v['IDREFS'] = 'IDrefs'
    v['ENTITY'] = 'prod557'
    v['ENTITIES'] = 'prod557 prod563'
    # oldball types
    v['QName'] = 'pre:myElement'
    v['boolean'] = 'true'
    v['hexBinary'] = '0FB8'
    v['base64Binary'] = '0fb8'
    v['anyURI'] = 'http://miaozn.github.io/misc'
    v['notation'] = 'asd'
    
    #ISO200022
    v['DocumentType3Code'] = "AB"
    v['ExternalPurpose1Code'] = "EP"
    v['CountryCode'] = "SE"
    v['ISODate'] = "1960-01-15"
    v['AnyBICIdentifier'] = "ESSESS"
    v['SettlementMethod1Code'] = "CLRG"
    v['ExternalServiceLevel1Code_EPC115-06_SCT_IB_2019_V1.0'] = "ABCD"
    v['ExternalAccountIdentification1Code'] ="HEJS"
    v['Max140Text'] = "140 character text here"
    v['IBAN2007Identifier'] = "SE12313139131"
    v['Max70Text'] = "Text with 70 characters"
    v['BICIdentifier'] = "ESSESESS"
    v['Max140Text_EPC115-06_SCT_IB_2019_V1.0'] = "140 charactes can be here"
    v['ISODateTime'] = "2013-11-07T11:41:10"
    v['Max15NumericText'] = "1"
    v['ExternalPersonIdentification1Code'] = "EPIC"
    



class GenXML:
    def __init__(self, xsd, elem, enable_choice):
        self.xsd = xmlschema.XMLSchema(xsd)
        self.elem = elem
        self.enable_choice = True
        self.root = True
        self.vals = {}
    
    # shorten the namespace
    def short_ns(self, ns):
        for k, v in self.xsd.namespaces.items():
            if k == '':
                continue
            if v == ns:
                return k
        return ''
    
    # if name is using long namespace,
    # lets replace it with the short one
    def use_short_ns(self, name):
        if name[0] == '{':
            x = name.find('}')
            ns = name[1:x]
            return self.short_ns(ns) + "" + name[x + 1:]
        return name
    
    
    # remove the namespace in name
    def remove_ns(self, name):
        if name[0] == '{':
            x = name.find('}')
            return name[x + 1:]
        return name

    # header of xml doc
    def print_header(self):
        print("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>")

    # put all defined namespaces as a string
    def ns_map_str(self):
        ns_all = ''
        for k, v in self.xsd.namespaces.items():
            if k == '':
                continue
            else:
                ns_all += 'xmlns:' + k + '=\"' + v + '\"' + ' '
        return ns_all
        

    # start a tag with name
    def start_tag(self, name):
        x = '<' + name
        if self.root:
            self.root = False
            x += ' ' + self.ns_map_str()
        x += '>'
        return x


    # end a tag with name
    def end_tag(self, name):
        return '</' + name + '>'
    
        
    # make a sample data for primitive types
    def genval(self, name, class_node):
        name = self.remove_ns(name)
        if name in self.vals:
            return self.vals[name]
        return 'ERROR ' + name
    
    
    # print a group
    def group2xml(self, g, class_node):
        if hasattr(g, 'model'):
            model = str(g.model)
            model = self.remove_ns(model)
        
            if hasattr(g, '_group'):
                nextg = g._group
                y = len(nextg)
                if y == 0:
                    #print ('<!--empty-->')
                    return
    
            #print ('<!--START:[' + model + ']-->')
            if self.enable_choice and model == 'choice':
                None
                #print ('<!--next item is from a [choice] group with size=' + str(y) + '-->')
            else:
                None
                #print ('<!--next ' + str(y) + ' items are in a [' + model + '] group-->')
                
            for ng in nextg:
                print(ng)
                if isinstance(ng, XsdElement):
                    self.node2xml(ng, class_node)
                elif isinstance(ng, XsdAnyElement):
                    self.node2xml(ng, class_node)
                else:
                    self.group2xml(ng, class_node)
            
                #if self.enable_choice and model == 'choice':
                #    break
            #print ('<!--END:[' + model + ']-->')
    
    
    # print a node
    def node2xml(self, node, parent_node):
        
        new_node = Node()
        new_node.set_name(self.use_short_ns(node.name))
        parent_node.append_child(new_node)
        
        
        #To be checked
        if not hasattr(node, 'min_occurs'):
            #print ('<!--next 1 item is mandatory (minOcuurs does not exist)-->')
            new_node.set_min_occurrence(1)

        elif node.min_occurs == 0:
            #print ('<!--next 1 item is optional (minOcuurs = 0)-->')
            new_node.set_min_occurrence(0)
            
        if isinstance(node.type, XsdComplexType):
            n = self.use_short_ns(node.name)
            print("----" + n)
            if node.type.is_simple():
                #print ('<!--simple content-->')
                tp = str(node.type.content_type)
                #print (self.start_tag(n) + self.genval(tp) + self.end_tag(n))
            else:
                self.group2xml(node.type.content_type, new_node)
        elif isinstance(node.type, XsdAtomicBuiltin):
            n = self.use_short_ns(node.name)
            
            tp = str(node.type)
        elif isinstance(node.type, XsdSimpleType):
            n = self.use_short_ns(node.name)
                   
            if isinstance(node.type, XsdList):
                #print ('<!--simpletype: list-->')
                tp = str(node.type.item_type)
                #print (self.start_tag(n) + self.genval(tp) + self.end_tag(n))
            elif isinstance(node.type, XsdUnion):
                #print ('<!--simpletype: union.-->')
                #print ('<!--default: using the 1st type-->')
                tp = str(node.type.member_types[0].base_type)
                #print (self.start_tag(n) + self.genval(tp) + self.end_tag(n))
            else:
                #tp = str(node.type.base_type)
                tp = str(node.type.name)
                #print (self.start_tag(n) + self.genval(tp, new_node) + self.end_tag(n))
                new_node.set_value(self.genval(tp, new_node))
        else:
            print("HM???????" + node)
            #print ('ERROR: unknown type: ' + node.type)
    
    
    # setup. Called from generator_tree.py when the function needs to be run.
    def run(self):
        valsmap(self.vals)
        root_node = Node() #a class defined in separate file to keep track
        root_node.set_name("My little document")
        self.print_header()
        self.node2xml(self.xsd.elements[self.elem],root_node)
        
        #Removing first dummy root
        root_node = root_node.child_nodes[0]
        return root_node
