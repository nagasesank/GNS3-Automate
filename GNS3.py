import os
import subprocess
import time
import requests

# GNS3 server information
GNS3_SERVER = 'localhost'
GNS3_PORT = '3080'

# Project information
PROJECT_ID = 'a3a8e806-3bb2-4730-a096-67481dac1753'
GNS3_BASE_URL = f'http://{GNS3_SERVER}:{GNS3_PORT}/v2/projects/{PROJECT_ID}'

# API endpoint URLs
NODES_URL = f"{GNS3_BASE_URL}/nodes"

class GNS3:
    def __init__(self):
        self.nodes = self.get_nodes()
    
    def get_nodes(self) -> list:
        """Get nodes in project"""
        try:
            response = requests.get(NODES_URL)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching nodes: {e}")
            exit()
    
    def get_node(self, img_name: str) -> str:
        """Get the node_id for a node by name"""
        node = next((node for node in self.nodes if node['name'] == img_name), None)
        if node:
            return node['node_id']
        print(f"Node with name {img_name} not found.")
        exit()

class Device():
    def __init__(self, img_name: str) -> None:
        """Initialize the device with its node_id from GNS3"""
        gns3 = GNS3()
        self.node_id = gns3.get_node(img_name)
        self.name = img_name
        print(f"Device {self.name} initialized with Node ID: {self.node_id}")

    def _send_request(self, action: str) -> None:
        url = f"{GNS3_BASE_URL}/nodes/{self.node_id}/{action}"
        try:
            response = requests.post(url)
            response.raise_for_status()
            print(f"Device {self.name} {action} successful.")
        except requests.exceptions.RequestException as e:
            print(f"Failed to {action} the device {self.name}: {e}")

    def start_router(self):
        """Start the router"""
        self._send_request('start')

    def stop_router(self):
        """Stop the router"""
        self._send_request('stop')

    def device_status(self) -> str:
        """Check and return the status of the device"""
        url = f"{GNS3_BASE_URL}/nodes/{self.node_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            status = response.json().get('status', 'unknown')
            print(f"Device {self.name} status: {status}")
            return status
        except requests.exceptions.RequestException as e:
            print(f"Failed to get the status of the device {self.name}: {e}")
            return 'unknown'

class AnsiblePlaybookRunner:
    """Class to execute Ansible playbooks for different device types and manage GNS3 device states."""
    
    def __init__(self, inventory_path, device_name):
        self.inventory_path = inventory_path
        self.device = Device(device_name)
    
    def run_playbook(self, playbook_path, extra_vars=None):
        """Run an Ansible playbook with optional extra variables."""
        command = ["ansible-playbook", playbook_path, "-i", self.inventory_path]
        
        if extra_vars:
            extra_vars_formatted = " ".join([f"{key}={value}" for key, value in extra_vars.items()])
            command.extend(["-e", extra_vars_formatted])
        
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            print("Playbook output:\n", result.stdout)
        except subprocess.CalledProcessError as e:
            print("Error running playbook:\n", e.stderr)
    
    def manage_device_state(self, action):
        """Manage the GNS3 device state (up or down)."""
        if action.lower() in ('up', 'down'):
            getattr(self.device, f"{action}_router")()
            time.sleep(5)  # Simulating device state change time
        else:
            print("Invalid action. Please specify 'up' or 'down'.")
    
    def run_ios_playbooks(self):
        """Run the playbooks for Cisco IOS devices."""
        self.manage_device_state('up')
        playbook_dir = "ansible_playbooks/ios/"
        playbooks = ["configure_hostname.yml", "configure_interface.yml", "backup_config.yml"]
        for playbook in playbooks:
            self.run_playbook(os.path.join(playbook_dir, playbook))
        self.manage_device_state('down')

if __name__ == "__main__":
    # Path to your inventory file
    inventory_path = "./inventory.yml"
    
    # Initialize the Ansible playbook runner for a specific device
    runner = AnsiblePlaybookRunner(inventory_path, "IOS_Device")
    
    # Execute the playbooks for all device types (can be customized)
    runner.run_ios_playbooks()
