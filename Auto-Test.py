import os,sys, re, time
import xml.etree.ElementTree as etree
from GNS3 import *
import subprocess as sp

obj = GNS3()

user_input =sys.argv[1]
file = open(os.path.abspath(user_input),'r')
path=list(os.walk("/home/surya/Scans"))[0][2]
xml_tree = etree.parse(file)
_family = xml_tree.findall('.//{http://oval.mitre.org/XMLSchema/oval-definitions-5}affected')[0].get('family')
family = "LINUX" if _family == "unix" else _family

### This Will Check the Ovaltools Scanning 
def oscommands():
    cmd = "ovaltools " +user_input+f" checkoval {family.upper()}"
    
    out = os.system(cmd)
    if out !=0:
        print("Scanning is not completed")
        print("---"*10)
        sys.exit()
    else:
        print("Scanning is Completed")


### Here You will Integrate with the GNS3 
def testing():
    path=input("Choose The Config Files To Test: ")
    if "esxi" in path:
        cmd= f"ovaltools -t {path}"
        os.system(cmd)
    else:   
        _path = list(filter(lambda x: x if family in x else '', path))
        for name, num in zip(_path, range(0, len(_path))):
            print(f"{num+1}. {name}")
    ### Here You Will Select The Config Files to Test with GNS# device
        resp = input("Select The Device to Scan:")
        device_name = re.findall(r"config-(.*)\.ini", _path[int(resp)-1])[0]
        node_id = obj.get_node(device_name)
        obj1=Device(node_id)
    # Start the Router
        obj1.start_router(node_id)
        time.sleep(30)
        cmd= f"ovaltools -t /home/surya/Scans/{_path[int(resp)-1]} {user_input}"
        os.system(cmd)
    # Stop the Router
        obj1.stop_router(node_id)
def report():
    pass

oscommands()
testing()





