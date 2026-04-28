#!/usr/bin/env python3
"""
Task 2 Network Automation Generator
Creates complete Cisco Packet Tracer network configurations
Based on the Task 2 network topology diagram
"""

import os
import json
from datetime import datetime

class Task2NetworkGenerator:
    def __init__(self):
        self.network_topology = {
            "routers": {
                "R1": {
                    "interfaces": {
                        "g0/0": {"ip": "10.1.12.1", "mask": "255.255.255.252", "connected_to": "R2"},
                        "g0/1": {"ip": "10.1.13.1", "mask": "255.255.255.252", "connected_to": "R3"},
                        "g0/2": {"ip": "192.168.10.1", "mask": "255.255.255.0", "connected_to": "SW1"}
                    },
                    "ospf_networks": [
                        {"network": "10.1.12.0", "wildcard": "0.0.0.3", "area": "0"},
                        {"network": "10.1.13.0", "wildcard": "0.0.0.3", "area": "0"},
                        {"network": "192.168.10.0", "wildcard": "0.0.0.255", "area": "0"}
                    ]
                },
                "R2": {
                    "interfaces": {
                        "g0/0": {"ip": "10.1.12.2", "mask": "255.255.255.252", "connected_to": "R1"},
                        "g0/1": {"ip": "10.2.24.1", "mask": "255.255.255.252", "connected_to": "R4"},
                        "g0/2": {"ip": "192.168.20.1", "mask": "255.255.255.0", "connected_to": "SW2"}
                    },
                    "ospf_networks": [
                        {"network": "10.1.12.0", "wildcard": "0.0.0.3", "area": "0"},
                        {"network": "10.2.24.0", "wildcard": "0.0.0.3", "area": "0"},
                        {"network": "192.168.20.0", "wildcard": "0.0.0.255", "area": "0"}
                    ]
                },
                "R3": {
                    "interfaces": {
                        "g0/0": {"ip": "10.1.13.2", "mask": "255.255.255.252", "connected_to": "R1"},
                        "g0/1": {"ip": "10.3.34.1", "mask": "255.255.255.252", "connected_to": "R4"},
                        "g0/2": {"ip": "192.168.30.1", "mask": "255.255.255.0", "connected_to": "SW3"}
                    },
                    "ospf_networks": [
                        {"network": "10.1.13.0", "wildcard": "0.0.0.3", "area": "0"},
                        {"network": "10.3.34.0", "wildcard": "0.0.0.3", "area": "0"},
                        {"network": "192.168.30.0", "wildcard": "0.0.0.255", "area": "0"}
                    ]
                },
                "R4": {
                    "interfaces": {
                        "g0/0": {"ip": "10.2.24.2", "mask": "255.255.255.252", "connected_to": "R2"},
                        "g0/1": {"ip": "10.3.34.2", "mask": "255.255.255.252", "connected_to": "R3"},
                        "g0/2": {"ip": "192.168.40.1", "mask": "255.255.255.0", "connected_to": "SW4"}
                    },
                    "ospf_networks": [
                        {"network": "10.2.24.0", "wildcard": "0.0.0.3", "area": "0"},
                        {"network": "10.3.34.0", "wildcard": "0.0.0.3", "area": "0"},
                        {"network": "192.168.40.0", "wildcard": "0.0.0.255", "area": "0"}
                    ]
                }
            },
            "switches": {
                "SW1": {
                    "vlans": {"10": "SALES", "99": "MANAGEMENT"},
                    "trunk_ports": ["g0/1"],
                    "access_ports": {"f0/1": "10", "f0/2": "10", "f0/3": "10", "f0/4": "10"},
                    "management_ip": "192.168.10.10",
                    "default_gateway": "192.168.10.1"
                },
                "SW2": {
                    "vlans": {"20": "MARKETING", "99": "MANAGEMENT"},
                    "trunk_ports": ["g0/1"],
                    "access_ports": {"f0/1": "20", "f0/2": "20", "f0/3": "20", "f0/4": "20"},
                    "management_ip": "192.168.20.10",
                    "default_gateway": "192.168.20.1"
                },
                "SW3": {
                    "vlans": {"30": "IT", "99": "MANAGEMENT"},
                    "trunk_ports": ["g0/1"],
                    "access_ports": {"f0/1": "30", "f0/2": "30", "f0/3": "30", "f0/4": "30"},
                    "management_ip": "192.168.30.10",
                    "default_gateway": "192.168.30.1"
                },
                "SW4": {
                    "vlans": {"40": "FINANCE", "99": "MANAGEMENT"},
                    "trunk_ports": ["g0/1"],
                    "access_ports": {"f0/1": "40", "f0/2": "40", "f0/3": "40", "f0/4": "40"},
                    "management_ip": "192.168.40.10",
                    "default_gateway": "192.168.40.1"
                }
            },
            "pcs": {
                "PC1": {"ip": "192.168.10.100", "mask": "255.255.255.0", "gateway": "192.168.10.1", "vlan": "10"},
                "PC2": {"ip": "192.168.10.101", "mask": "255.255.255.0", "gateway": "192.168.10.1", "vlan": "10"},
                "PC3": {"ip": "192.168.20.100", "mask": "255.255.255.0", "gateway": "192.168.20.1", "vlan": "20"},
                "PC4": {"ip": "192.168.20.101", "mask": "255.255.255.0", "gateway": "192.168.20.1", "vlan": "20"},
                "PC5": {"ip": "192.168.30.100", "mask": "255.255.255.0", "gateway": "192.168.30.1", "vlan": "30"},
                "PC6": {"ip": "192.168.30.101", "mask": "255.255.255.0", "gateway": "192.168.30.1", "vlan": "30"},
                "PC7": {"ip": "192.168.40.100", "mask": "255.255.255.0", "gateway": "192.168.40.1", "vlan": "40"},
                "PC8": {"ip": "192.168.40.101", "mask": "255.255.255.0", "gateway": "192.168.40.1", "vlan": "40"}
            }
        }
    
    def generate_router_config(self, router_name):
        """Generate complete router configuration"""
        router_data = self.network_topology["routers"][router_name]
        
        config = f"""!
! {router_name} Configuration - Task 2 Network
! Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
!
version 15.1
no service timestamps log datetime msec
no service timestamps debug datetime msec
no service password-encryption
!
hostname {router_name}
!
!
!
enable secret 5 $1$mERr$9cTjUIEqNGurQiFU.ZeCi1
!
!
!
!
!
!
ip cef
no ipv6 cef
!
!
username admin privilege 15 secret 5 $1$mERr$9cTjUIEqNGurQiFU.ZeCi1
!
!
license udi pid CISCO2901/K9 sn FTX1524MW6A-
!
!
!
!
!
!
!
!
!
!
!
spanning-tree mode pvst
!
!
!
!
"""
        
        # Add interface configurations
        for interface, config_data in router_data["interfaces"].items():
            config += f"""!
interface GigabitEthernet{interface}
 description Connected to {config_data['connected_to']}
 ip address {config_data['ip']} {config_data['mask']}
 duplex auto
 speed auto
 no shutdown
!
"""
        
        # Add OSPF configuration
        config += f"""!
router ospf 1
 log-adjacency-changes
"""
        
        for network in router_data["ospf_networks"]:
            config += f" network {network['network']} {network['wildcard']} area {network['area']}\n"
        
        config += """!
ip classless
!
ip flow-export version 9
!
!
!
banner motd ^C
******************************************
*        AUTHORIZED ACCESS ONLY         *
*     Task 2 Network - """ + router_name + """           *
******************************************
^C
!
!
!
line con 0
 password cisco
 login
!
line aux 0
!
line vty 0 4
 password cisco
 login local
 transport input ssh
!
!
!
end
"""
        return config
    
    def generate_switch_config(self, switch_name):
        """Generate complete switch configuration"""
        switch_data = self.network_topology["switches"][switch_name]
        
        config = f"""!
! {switch_name} Configuration - Task 2 Network
! Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
!
version 15.0
no service timestamps log datetime msec
no service timestamps debug datetime msec
no service password-encryption
!
hostname {switch_name}
!
enable secret 5 $1$mERr$9cTjUIEqNGurQiFU.ZeCi1
!
!
!
!
!
!
spanning-tree mode pvst
spanning-tree extend system-id
!
"""
        
        # Create VLANs
        for vlan_id, vlan_name in switch_data["vlans"].items():
            config += f"""vlan {vlan_id}
 name {vlan_name}
!
"""
        
        # Configure trunk ports
        for port in switch_data["trunk_ports"]:
            config += f"""!
interface GigabitEthernet{port}
 description Trunk to Router
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan all
 no shutdown
!
"""
        
        # Configure access ports
        for port, vlan in switch_data["access_ports"].items():
            config += f"""!
interface FastEthernet{port}
 description Access port VLAN {vlan}
 switchport mode access
 switchport access vlan {vlan}
 switchport port-security
 switchport port-security maximum 2
 switchport port-security mac-address sticky
 switchport port-security violation shutdown
 spanning-tree portfast
 no shutdown
!
"""
        
        # Management VLAN interface
        config += f"""!
interface Vlan99
 description Management Interface
 ip address {switch_data['management_ip']} 255.255.255.0
 no shutdown
!
ip default-gateway {switch_data['default_gateway']}
!
"""
        
        config += """!
banner motd ^C
******************************************
*        AUTHORIZED ACCESS ONLY         *
*     Task 2 Network - """ + switch_name + """          *
******************************************
^C
!
line con 0
 password cisco
 login
!
line vty 0 4
 password cisco
 login
!
line vty 5 15
 password cisco
 login
!
!
end
"""
        return config
    
    def generate_pc_config(self, pc_name):
        """Generate PC configuration for Packet Tracer"""
        pc_data = self.network_topology["pcs"][pc_name]
        
        config = f"""# {pc_name} Configuration - Task 2 Network
# Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# Static IP Configuration
IP Address: {pc_data['ip']}
Subnet Mask: {pc_data['mask']}
Default Gateway: {pc_data['gateway']}
DNS Server: 8.8.8.8

# VLAN Assignment: {pc_data['vlan']}
# Network: {pc_data['gateway'].rsplit('.', 1)[0]}.0/24

# Test Commands:
# ping {pc_data['gateway']}  (Test gateway connectivity)
# ping 8.8.8.8             (Test internet connectivity)
# ipconfig                 (View IP configuration)
"""
        return config
    
    def generate_network_documentation(self):
        """Generate network documentation"""
        doc = f"""
# Task 2 Network Documentation
Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Network Overview
This network consists of 4 routers in a full mesh topology with OSPF routing,
4 access switches, and 8 end devices across different VLANs.

## IP Addressing Scheme

### Router Interconnects (Point-to-Point /30 networks)
- R1-R2 Link: 10.1.12.0/30
  - R1 G0/0: 10.1.12.1/30
  - R2 G0/0: 10.1.12.2/30

- R1-R3 Link: 10.1.13.0/30
  - R1 G0/1: 10.1.13.1/30
  - R3 G0/0: 10.1.13.2/30

- R2-R4 Link: 10.2.24.0/30
  - R2 G0/1: 10.2.24.1/30
  - R4 G0/0: 10.2.24.2/30

- R3-R4 Link: 10.3.34.0/30
  - R3 G0/1: 10.3.34.1/30
  - R4 G0/1: 10.3.34.2/30

### LAN Networks (/24 networks)
- VLAN 10 (Sales): 192.168.10.0/24 - Connected to R1
- VLAN 20 (Marketing): 192.168.20.0/24 - Connected to R2
- VLAN 30 (IT): 192.168.30.0/24 - Connected to R3
- VLAN 40 (Finance): 192.168.40.0/24 - Connected to R4

### Device Assignments
"""
        
        # Add PC assignments
        for pc_name, pc_data in self.network_topology["pcs"].items():
            doc += f"- {pc_name}: {pc_data['ip']} (VLAN {pc_data['vlan']})\n"
        
        doc += """
## Routing Protocol
- OSPF Area 0 (Single Area)
- All networks advertised in OSPF
- Router ID: Highest IP address on device

## VLANs
- VLAN 10: Sales Department
- VLAN 20: Marketing Department  
- VLAN 30: IT Department
- VLAN 40: Finance Department
- VLAN 99: Management (Switch management)

## Security Features
- Port Security on access ports
- Enable secret passwords
- VTY line security
- Banner messages

## Testing Plan
1. Verify OSPF neighbor relationships
2. Test inter-VLAN routing
3. Verify end-to-end connectivity
4. Test redundant paths
"""
        return doc
    
    def create_packet_tracer_instructions(self):
        """Create step-by-step Packet Tracer setup instructions"""
        instructions = f"""
# Packet Tracer Setup Instructions - Task 2 Network
Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Step 1: Add Devices to Workspace
1. Add 4 x Cisco 2901 Routers (R1, R2, R3, R4)
2. Add 4 x Cisco 2960 Switches (SW1, SW2, SW3, SW4)  
3. Add 8 x Generic PCs (PC1-PC8)

## Step 2: Physical Connections
Make the following connections using Copper Straight-Through cables:

### Router-to-Router Links:
- R1 G0/0 ↔ R2 G0/0
- R1 G0/1 ↔ R3 G0/0  
- R2 G0/1 ↔ R4 G0/0
- R3 G0/1 ↔ R4 G0/1

### Router-to-Switch Links:
- R1 G0/2 ↔ SW1 G0/1
- R2 G0/2 ↔ SW2 G0/1
- R3 G0/2 ↔ SW3 G0/1
- R4 G0/2 ↔ SW4 G0/1

### Switch-to-PC Links:
- SW1 F0/1 ↔ PC1, SW1 F0/2 ↔ PC2
- SW2 F0/1 ↔ PC3, SW2 F0/2 ↔ PC4
- SW3 F0/1 ↔ PC5, SW3 F0/2 ↔ PC6
- SW4 F0/1 ↔ PC7, SW4 F0/2 ↔ PC8

## Step 3: Configure Devices
1. Copy configurations from generated files:
   - R1_config.txt → R1 CLI
   - R2_config.txt → R2 CLI
   - R3_config.txt → R3 CLI
   - R4_config.txt → R4 CLI
   - SW1_config.txt → SW1 CLI
   - SW2_config.txt → SW2 CLI
   - SW3_config.txt → SW3 CLI
   - SW4_config.txt → SW4 CLI

2. Configure PC IP addresses from PC_configs.txt

## Step 4: Verification Commands
Run these commands to verify the network:

### On Routers:
- show ip route
- show ip ospf neighbor
- show ip interface brief
- ping [destination_ip]

### On Switches:
- show vlan brief
- show interface trunk
- show mac address-table

### On PCs:
- ipconfig
- ping [gateway_ip]
- ping [remote_pc_ip]

## Step 5: Testing Scenarios
1. Ping from PC1 to PC3 (inter-VLAN routing)
2. Ping from PC5 to PC7 (different router paths)
3. Verify OSPF convergence by shutting down a link
4. Test redundant paths in the network

## Expected Results
- All OSPF neighbors should be in FULL state
- All PCs should be able to ping their gateways
- Inter-VLAN communication should work
- Network should have redundant paths for fault tolerance
"""
        return instructions
    
    def generate_all_configs(self):
        """Generate all configuration files"""
        # Create output directory
        output_dir = "Task2_Network_Configs"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        print(f"🚀 Generating Task 2 Network Configurations...")
        print(f"📁 Output directory: {output_dir}")
        
        # Generate router configs
        print("\n🔧 Generating Router Configurations...")
        for router_name in self.network_topology["routers"]:
            config = self.generate_router_config(router_name)
            filename = f"{output_dir}/{router_name}_config.txt"
            with open(filename, 'w') as f:
                f.write(config)
            print(f"   ✅ {router_name}_config.txt")
        
        # Generate switch configs
        print("\n🔧 Generating Switch Configurations...")
        for switch_name in self.network_topology["switches"]:
            config = self.generate_switch_config(switch_name)
            filename = f"{output_dir}/{switch_name}_config.txt"
            with open(filename, 'w') as f:
                f.write(config)
            print(f"   ✅ {switch_name}_config.txt")
        
        # Generate PC configs
        print("\n💻 Generating PC Configurations...")
        pc_configs = ""
        for pc_name in self.network_topology["pcs"]:
            pc_configs += self.generate_pc_config(pc_name) + "\n" + "="*50 + "\n"
        
        with open(f"{output_dir}/PC_configs.txt", 'w') as f:
            f.write(pc_configs)
        print(f"   ✅ PC_configs.txt")
        
        # Generate documentation
        print("\n📚 Generating Documentation...")
        doc = self.generate_network_documentation()
        with open(f"{output_dir}/Network_Documentation.md", 'w') as f:
            f.write(doc)
        print(f"   ✅ Network_Documentation.md")
        
        # Generate Packet Tracer instructions
        instructions = self.create_packet_tracer_instructions()
        with open(f"{output_dir}/Packet_Tracer_Instructions.md", 'w') as f:
            f.write(instructions)
        print(f"   ✅ Packet_Tracer_Instructions.md")
        
        # Generate topology JSON for reference
        with open(f"{output_dir}/network_topology.json", 'w') as f:
            json.dump(self.network_topology, f, indent=2)
        print(f"   ✅ network_topology.json")
        
        print(f"\n🎉 Task 2 Network Generation Complete!")
        print(f"📋 Files created in '{output_dir}' directory:")
        print(f"   • 4 Router configuration files")
        print(f"   • 4 Switch configuration files") 
        print(f"   • PC configuration file")
        print(f"   • Network documentation")
        print(f"   • Packet Tracer setup instructions")
        print(f"   • Network topology reference")
        
        return output_dir

def main():
    """Main function to generate the network"""
    print("=" * 60)
    print("🌐 TASK 2 NETWORK AUTOMATION GENERATOR")
    print("=" * 60)
    
    generator = Task2NetworkGenerator()
    output_dir = generator.generate_all_configs()
    
    print(f"\n📖 Next Steps:")
    print(f"1. Open Packet Tracer")
    print(f"2. Follow instructions in '{output_dir}/Packet_Tracer_Instructions.md'")
    print(f"3. Copy configurations from the generated .txt files")
    print(f"4. Test network connectivity using the verification commands")
    
    print(f"\n🎯 Your Task 2 network is ready to deploy!")

if __name__ == "__main__":
    main()

