# GNS3 Automatio using Anible 
## **Overview**
This repository offers a set of Python scripts to automate various tasks within the GNS3 network simulator. By harnessing the power of Python in tandem with GNS3's API, users can swiftly set up, manage, and tear down GNS3 topologies and projects.

## **Prerequisites**

1.GNS3 Installation:

* Install GNS3 from GNS3 Official Website.
* Make sure GNS3 API is enabled and accessible (default port is 3080).

2.Ansible Installation:
```bash 
sudo apt update
sudo apt install ansible -y
```
3.Python Requirements:

* Python 3.x should be installed.
* Required Python libraries
```bash
pip install requests
```
4.GNS3 Project:

* Import your network topology in GNS3.
* Ensure the project ID is set correctly in the Python script.

5.Ansible Inventory:

* The inventory.yml file should contain information on target devices like
```yaml
ios_devices:
  hosts:
    ios_router1:
      ansible_host: 192.168.1.10
      ansible_user: admin
      ansible_password: admin
```

## Folder Structure
```css
├── ansible_playbooks/
│   ├── ios/
│   │    ├── configure_hostname.yml
│   │    ├── configure_interface.yml
│   │    └── backup_config.yml
│   ├── ios_xe/
│   │    ├── configure_hostname.yml
│   │    ├── configure_interface.yml
│   │    └── backup_config.yml
│   ├── asa/
│   │    ├── configure_hostname.yml
│   │    ├── configure_interface.yml
│   │    └── backup_config.yml
│   ├── nxos/
│   │    ├── configure_hostname.yml
│   │    ├── configure_interface.yml
│   │    └── backup_config.yml
│   ├── bigip/
│   │    ├── configure_hostname.yml
│   │    ├── create_virtual_server.yml
│   │    └── backup_config.yml
│   └── juniper/
│        ├── configure_hostname.yml
│        ├── configure_interface.yml
│        └── backup_config.yml
├── backups/
├── inventory.yml
├── main.py
└── README.md
```

## Usage

1.**Run the Python Script**

Run the ```main.py``` file to start managing devices in GNS3 and executing Ansible playbooks
```bash
python3 main.py
```

2.**Configure Your GNS3 Device**

* Make sure the device name in GNS3 matches the device name you provide in the Python script.
* The script brings the GNS3 devices up, runs Ansible playbooks, and then powers the devices down.

3.**Run Specific Ansible Playbooks**

If you'd like to run a specific playbook, use the following command:
```bash
ansible-playbook -i inventory.yml ansible_playbooks/ios/configure_hostname.yml
```
## Customization
### Change Device Name
To change the device to be managed, modify the device name in the main.py file:
```bash
runner = AnsiblePlaybookRunner(inventory_path, "IOS_Device")
```
Change ```"IOS_Device"``` to the name of your device in GNS3.

### Change Playbooks
To change or add new playbooks, place them inside the corresponding directory (e.g., ```ansible_playbooks/ios/``` for Cisco IOS devices). Ensure that the playbook follows the structure of existing playbooks.

### Inventory File
The ```inventory.yml``` file contains the devices to manage. Here is an example configuration:
```yaml
ios_devices:
  hosts:
    ios_router1:
      ansible_host: 192.168.1.10
      ansible_user: admin
      ansible_password: admin

asa_devices:
  hosts:
    asa_firewall1:
      ansible_host: 192.168.2.10
      ansible_user: admin
      ansible_password: admin

nxos_devices:
  hosts:
    nxos_switch1:
      ansible_host: 192.168.3.10
      ansible_user: admin
      ansible_password: admin
```

## Commands

| Command |Description 
|----------|-----------
|```python3 main.py```   | Runs the full script to configure devices. 
|```ansible-playbook -i inventory.yml playbook.yml```   | Run a specific Ansible playbook.  
|```python3 main.py```    | Manages GNS3 devices and runs all playbooks.   

## Environment Variables

| Command |Description 
|----------|-----------
|```GNS3_SERVER```   | IP address of GNS3 server. Default is ```localhost```. 
|```GNS3_PORT```   |GNS3 API port. Default is ```3080```.  
|```PROJECT_ID```    | The GNS3 project ID for the topology. 

## Screenshots

Example GNS3 Topology:

![gns3](https://github.com/user-attachments/assets/7d08e097-4ff5-4ada-82d6-9c8cbad526ed)


 Let me know if you'd like any changes or additions.
