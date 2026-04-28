#!/usr/bin/env python3
"""
Advanced Network Inventory System
Manages network devices, IP addressing, and topology for Task 2 network
"""

import json
import yaml
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from ipaddress import IPv4Network, IPv4Address

@dataclass
class NetworkInterface:
    """Represents a network interface"""
    name: str
    ip_address: str
    subnet_mask: str
    description: str = ""
    vlan: int = None
    trunk: bool = False
    connected_to: str = ""
    
    @property
    def network(self) -> IPv4Network:
        """Get the network this interface belongs to"""
        return IPv4Network(f"{self.ip_address}/{self.subnet_mask}", strict=False)

@dataclass
class NetworkDevice:
    """Represents a network device"""
    hostname: str
    device_type: str  # router, switch, pc
    model: str
    mgmt_ip: str
    interfaces: List[NetworkInterface]
    credentials: Dict[str, str]
    location: str = ""
    
    def get_interface(self, name: str) -> NetworkInterface:
        """Get interface by name"""
        for interface in self.interfaces:
            if interface.name == name:
                return interface
        raise ValueError(f"Interface {name} not found on {self.hostname}")

class NetworkInventory:
    """Advanced network inventory management"""
    
    def __init__(self):
        self.devices: Dict[str, NetworkDevice] = {}
        self.vlans: Dict[int, Dict[str, str]] = {}
        self.networks: Dict[str, IPv4Network] = {}
        self.connections: List[Dict[str, str]] = []
        
    def add_device(self, device: NetworkDevice):
        """Add a device to inventory"""
        self.devices[device.hostname] = device
        
    def add_vlan(self, vlan_id: int, name: str, description: str = ""):
        """Add VLAN definition"""
        self.vlans[vlan_id] = {
            "name": name,
            "description": description
        }
        
    def add_network(self, name: str, network: str):
        """Add network definition"""
        self.networks[name] = IPv4Network(network)
        
    def add_connection(self, device1: str, interface1: str, device2: str, interface2: str):
        """Add physical connection between devices"""
        self.connections.append({
            "device1": device1,
            "interface1": interface1,
            "device2": device2,
            "interface2": interface2
        })
        
    def get_device(self, hostname: str) -> NetworkDevice:
        """Get device by hostname"""
        if hostname not in self.devices:
            raise ValueError(f"Device {hostname} not found in inventory")
        return self.devices[hostname]
        
    def get_devices_by_type(self, device_type: str) -> List[NetworkDevice]:
        """Get all devices of a specific type"""
        return [device for device in self.devices.values() 
                if device.device_type == device_type]
        
    def get_routers(self) -> List[NetworkDevice]:
        """Get all routers"""
        return self.get_devices_by_type("router")
        
    def get_switches(self) -> List[NetworkDevice]:
        """Get all switches"""
        return self.get_devices_by_type("switch")
        
    def get_pcs(self) -> List[NetworkDevice]:
        """Get all PCs"""
        return self.get_devices_by_type("pc")
        
    def validate_inventory(self) -> List[str]:
        """Validate inventory for consistency"""
        errors = []
        
        # Check for duplicate IP addresses
        ip_addresses = {}
        for device in self.devices.values():
            for interface in device.interfaces:
                if interface.ip_address in ip_addresses:
                    errors.append(f"Duplicate IP {interface.ip_address} on {device.hostname}:{interface.name} and {ip_addresses[interface.ip_address]}")
                else:
                    ip_addresses[interface.ip_address] = f"{device.hostname}:{interface.name}"
        
        # Check connections
        for conn in self.connections:
            try:
                device1 = self.get_device(conn["device1"])
                device2 = self.get_device(conn["device2"])
                device1.get_interface(conn["interface1"])
                device2.get_interface(conn["interface2"])
            except ValueError as e:
                errors.append(f"Connection error: {e}")
                
        return errors
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert inventory to dictionary"""
        return {
            "devices": {hostname: asdict(device) for hostname, device in self.devices.items()},
            "vlans": self.vlans,
            "networks": {name: str(network) for name, network in self.networks.items()},
            "connections": self.connections
        }
        
    def to_json(self, filename: str = None) -> str:
        """Export inventory to JSON"""
        data = self.to_dict()
        json_str = json.dumps(data, indent=2)
        if filename:
            with open(filename, 'w') as f:
                f.write(json_str)
        return json_str
        
    def to_yaml(self, filename: str = None) -> str:
        """Export inventory to YAML"""
        data = self.to_dict()
        yaml_str = yaml.dump(data, default_flow_style=False, indent=2)
        if filename:
            with open(filename, 'w') as f:
                f.write(yaml_str)
        return yaml_str
        
    @classmethod
    def from_json(cls, filename: str) -> 'NetworkInventory':
        """Load inventory from JSON file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        return cls._from_dict(data)
        
    @classmethod
    def from_yaml(cls, filename: str) -> 'NetworkInventory':
        """Load inventory from YAML file"""
        with open(filename, 'r') as f:
            data = yaml.safe_load(f)
        return cls._from_dict(data)
        
    @classmethod
    def _from_dict(cls, data: Dict[str, Any]) -> 'NetworkInventory':
        """Create inventory from dictionary"""
        inventory = cls()
        
        # Load devices
        for hostname, device_data in data.get("devices", {}).items():
            interfaces = [NetworkInterface(**iface) for iface in device_data["interfaces"]]
            device = NetworkDevice(
                hostname=device_data["hostname"],
                device_type=device_data["device_type"],
                model=device_data["model"],
                mgmt_ip=device_data["mgmt_ip"],
                interfaces=interfaces,
                credentials=device_data["credentials"],
                location=device_data.get("location", "")
            )
            inventory.add_device(device)
            
        # Load VLANs
        inventory.vlans = data.get("vlans", {})
        
        # Load networks
        for name, network_str in data.get("networks", {}).items():
            inventory.add_network(name, network_str)
            
        # Load connections
        inventory.connections = data.get("connections", [])
        
        return inventory

def create_task2_inventory() -> NetworkInventory:
    """Create the complete Task 2 network inventory"""
    inventory = NetworkInventory()
    
    # Define VLANs
    inventory.add_vlan(10, "SALES", "Sales Department")
    inventory.add_vlan(20, "MARKETING", "Marketing Department")
    inventory.add_vlan(30, "IT", "IT Department")
    inventory.add_vlan(40, "FINANCE", "Finance Department")
    inventory.add_vlan(99, "MANAGEMENT", "Management VLAN")
    
    # Define networks
    inventory.add_network("R1-R2", "10.1.12.0/30")
    inventory.add_network("R1-R3", "10.1.13.0/30")
    inventory.add_network("R2-R4", "10.2.24.0/30")
    inventory.add_network("R3-R4", "10.3.34.0/30")
    inventory.add_network("SALES", "192.168.10.0/24")
    inventory.add_network("MARKETING", "192.168.20.0/24")
    inventory.add_network("IT", "192.168.30.0/24")
    inventory.add_network("FINANCE", "192.168.40.0/24")
    
    # Default credentials
    router_creds = {"username": "admin", "password": "cisco", "secret": "cisco"}
    switch_creds = {"username": "admin", "password": "cisco", "secret": "cisco"}
    
    # Create routers
    routers = [
        {
            "hostname": "R1",
            "mgmt_ip": "192.168.10.1",
            "interfaces": [
                NetworkInterface("GigabitEthernet0/0", "10.1.12.1", "255.255.255.252", "Connected to R2"),
                NetworkInterface("GigabitEthernet0/1", "10.1.13.1", "255.255.255.252", "Connected to R3"),
                NetworkInterface("GigabitEthernet0/2", "192.168.10.1", "255.255.255.0", "Connected to SW1")
            ]
        },
        {
            "hostname": "R2",
            "mgmt_ip": "192.168.20.1",
            "interfaces": [
                NetworkInterface("GigabitEthernet0/0", "10.1.12.2", "255.255.255.252", "Connected to R1"),
                NetworkInterface("GigabitEthernet0/1", "10.2.24.1", "255.255.255.252", "Connected to R4"),
                NetworkInterface("GigabitEthernet0/2", "192.168.20.1", "255.255.255.0", "Connected to SW2")
            ]
        },
        {
            "hostname": "R3",
            "mgmt_ip": "192.168.30.1",
            "interfaces": [
                NetworkInterface("GigabitEthernet0/0", "10.1.13.2", "255.255.255.252", "Connected to R1"),
                NetworkInterface("GigabitEthernet0/1", "10.3.34.1", "255.255.255.252", "Connected to R4"),
                NetworkInterface("GigabitEthernet0/2", "192.168.30.1", "255.255.255.0", "Connected to SW3")
            ]
        },
        {
            "hostname": "R4",
            "mgmt_ip": "192.168.40.1",
            "interfaces": [
                NetworkInterface("GigabitEthernet0/0", "10.2.24.2", "255.255.255.252", "Connected to R2"),
                NetworkInterface("GigabitEthernet0/1", "10.3.34.2", "255.255.255.252", "Connected to R3"),
                NetworkInterface("GigabitEthernet0/2", "192.168.40.1", "255.255.255.0", "Connected to SW4")
            ]
        }
    ]
    
    for router_data in routers:
        device = NetworkDevice(
            hostname=router_data["hostname"],
            device_type="router",
            model="Cisco 2901",
            mgmt_ip=router_data["mgmt_ip"],
            interfaces=router_data["interfaces"],
            credentials=router_creds,
            location="Data Center"
        )
        inventory.add_device(device)
    
    # Create switches
    switches = [
        {
            "hostname": "SW1",
            "mgmt_ip": "192.168.10.10",
            "vlan": 10,
            "interfaces": [
                NetworkInterface("GigabitEthernet0/1", "", "", "Trunk to R1", trunk=True),
                NetworkInterface("FastEthernet0/1", "", "", "Access port VLAN 10", vlan=10),
                NetworkInterface("FastEthernet0/2", "", "", "Access port VLAN 10", vlan=10),
                NetworkInterface("Vlan99", "192.168.10.10", "255.255.255.0", "Management interface", vlan=99)
            ]
        },
        {
            "hostname": "SW2",
            "mgmt_ip": "192.168.20.10",
            "vlan": 20,
            "interfaces": [
                NetworkInterface("GigabitEthernet0/1", "", "", "Trunk to R2", trunk=True),
                NetworkInterface("FastEthernet0/1", "", "", "Access port VLAN 20", vlan=20),
                NetworkInterface("FastEthernet0/2", "", "", "Access port VLAN 20", vlan=20),
                NetworkInterface("Vlan99", "192.168.20.10", "255.255.255.0", "Management interface", vlan=99)
            ]
        },
        {
            "hostname": "SW3",
            "mgmt_ip": "192.168.30.10",
            "vlan": 30,
            "interfaces": [
                NetworkInterface("GigabitEthernet0/1", "", "", "Trunk to R3", trunk=True),
                NetworkInterface("FastEthernet0/1", "", "", "Access port VLAN 30", vlan=30),
                NetworkInterface("FastEthernet0/2", "", "", "Access port VLAN 30", vlan=30),
                NetworkInterface("Vlan99", "192.168.30.10", "255.255.255.0", "Management interface", vlan=99)
            ]
        },
        {
            "hostname": "SW4",
            "mgmt_ip": "192.168.40.10",
            "vlan": 40,
            "interfaces": [
                NetworkInterface("GigabitEthernet0/1", "", "", "Trunk to R4", trunk=True),
                NetworkInterface("FastEthernet0/1", "", "", "Access port VLAN 40", vlan=40),
                NetworkInterface("FastEthernet0/2", "", "", "Access port VLAN 40", vlan=40),
                NetworkInterface("Vlan99", "192.168.40.10", "255.255.255.0", "Management interface", vlan=99)
            ]
        }
    ]
    
    for switch_data in switches:
        device = NetworkDevice(
            hostname=switch_data["hostname"],
            device_type="switch",
            model="Cisco 2960",
            mgmt_ip=switch_data["mgmt_ip"],
            interfaces=switch_data["interfaces"],
            credentials=switch_creds,
            location="Access Layer"
        )
        inventory.add_device(device)
    
    # Create PCs
    pcs = [
        {"hostname": "PC1", "ip": "192.168.10.100", "gateway": "192.168.10.1", "vlan": 10},
        {"hostname": "PC2", "ip": "192.168.10.101", "gateway": "192.168.10.1", "vlan": 10},
        {"hostname": "PC3", "ip": "192.168.20.100", "gateway": "192.168.20.1", "vlan": 20},
        {"hostname": "PC4", "ip": "192.168.20.101", "gateway": "192.168.20.1", "vlan": 20},
        {"hostname": "PC5", "ip": "192.168.30.100", "gateway": "192.168.30.1", "vlan": 30},
        {"hostname": "PC6", "ip": "192.168.30.101", "gateway": "192.168.30.1", "vlan": 30},
        {"hostname": "PC7", "ip": "192.168.40.100", "gateway": "192.168.40.1", "vlan": 40},
        {"hostname": "PC8", "ip": "192.168.40.101", "gateway": "192.168.40.1", "vlan": 40}
    ]
    
    for pc_data in pcs:
        device = NetworkDevice(
            hostname=pc_data["hostname"],
            device_type="pc",
            model="Generic PC",
            mgmt_ip=pc_data["ip"],
            interfaces=[
                NetworkInterface("Ethernet0", pc_data["ip"], "255.255.255.0", 
                               f"Connected to switch", vlan=pc_data["vlan"])
            ],
            credentials={"username": "user", "password": "user"},
            location="End User"
        )
        inventory.add_device(device)
    
    # Add physical connections
    connections = [
        ("R1", "GigabitEthernet0/0", "R2", "GigabitEthernet0/0"),
        ("R1", "GigabitEthernet0/1", "R3", "GigabitEthernet0/0"),
        ("R2", "GigabitEthernet0/1", "R4", "GigabitEthernet0/0"),
        ("R3", "GigabitEthernet0/1", "R4", "GigabitEthernet0/1"),
        ("R1", "GigabitEthernet0/2", "SW1", "GigabitEthernet0/1"),
        ("R2", "GigabitEthernet0/2", "SW2", "GigabitEthernet0/1"),
        ("R3", "GigabitEthernet0/2", "SW3", "GigabitEthernet0/1"),
        ("R4", "GigabitEthernet0/2", "SW4", "GigabitEthernet0/1"),
        ("SW1", "FastEthernet0/1", "PC1", "Ethernet0"),
        ("SW1", "FastEthernet0/2", "PC2", "Ethernet0"),
        ("SW2", "FastEthernet0/1", "PC3", "Ethernet0"),
        ("SW2", "FastEthernet0/2", "PC4", "Ethernet0"),
        ("SW3", "FastEthernet0/1", "PC5", "Ethernet0"),
        ("SW3", "FastEthernet0/2", "PC6", "Ethernet0"),
        ("SW4", "FastEthernet0/1", "PC7", "Ethernet0"),
        ("SW4", "FastEthernet0/2", "PC8", "Ethernet0")
    ]
    
    for device1, int1, device2, int2 in connections:
        inventory.add_connection(device1, int1, device2, int2)
    
    return inventory

if __name__ == "__main__":
    # Create and export Task 2 inventory
    print("🔧 Creating Task 2 Network Inventory...")
    inventory = create_task2_inventory()
    
    # Validate inventory
    errors = inventory.validate_inventory()
    if errors:
        print("❌ Inventory validation errors:")
        for error in errors:
            print(f"   - {error}")
    else:
        print("✅ Inventory validation passed!")
    
    # Export to files
    inventory.to_json("task2_inventory.json")
    inventory.to_yaml("task2_inventory.yaml")
    
    print(f"📊 Inventory Summary:")
    print(f"   - Routers: {len(inventory.get_routers())}")
    print(f"   - Switches: {len(inventory.get_switches())}")
    print(f"   - PCs: {len(inventory.get_pcs())}")
    print(f"   - VLANs: {len(inventory.vlans)}")
    print(f"   - Networks: {len(inventory.networks)}")
    print(f"   - Connections: {len(inventory.connections)}")
    
    print("🎉 Network inventory created successfully!")

