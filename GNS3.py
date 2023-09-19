import requests

# GNS3 server information
GNS3_SERVER = 'localhost'
GNS3_PORT = '3080'

# Project information
PROJECT_ID = 'a3a8e806-3bb2-4730-a096-67481dac1753'
GNS3_BASE_URL = 'http://localhost:3080/v2/projects/a3a8e806-3bb2-4730-a096-67481dac1753'

# API endpoint URLs
NODES_URL = f"http://{GNS3_SERVER}:{GNS3_PORT}/v2/projects/{PROJECT_ID}/nodes"

class GNS3():
    def get_nodes(self) -> set:
        # Get nodes in project
        response = requests.get(NODES_URL)
        if response.status_code != 200:
            print("Failed to get nodes")
            exit()
        return response.json()
    
    def get_node(self, img_name: str):
        for i in self.get_nodes():
            if i['name'] == img_name:
                return f"{i['node_id']}"


class Device():
    def __init__(self, node_id) -> None:
        self.node_id = node_id
        print(self.node_id)

    # Start router function
    def start_router(self, node_id):
        url = f"{GNS3_BASE_URL}/nodes/{node_id}/start"
        response = requests.post(url)
        if response.ok:
            print(f"Device started.")
        else:
            print(f"Failed to start the Device.")

    # Stop router function
    def stop_router(self, node_id):
        url = f"{GNS3_BASE_URL}/nodes/{node_id}/stop"
        response = requests.post(url)
        if response.ok:
            print(f"Device Stoped.")
        else:
            print(f"Failed to stop the Device.")

    def device_status(self) -> str:
        pass