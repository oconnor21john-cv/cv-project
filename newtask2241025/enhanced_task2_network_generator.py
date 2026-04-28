#!/usr/bin/env python3
"""
Enhanced Task 2 Network Automation Generator
Creates complete Cisco Packet Tracer network configurations
Based on the complete Task 2 network topology diagram
Excludes ISP devices as specified
"""

import os
import json
from datetime import datetime

class EnhancedTask2NetworkGenerator:
    def __init__(self):
        # Excluded devices: Local ISP R1-R4, ISP S1-S4, ISP Remote devices, 4331 ISP Remote
        self.network_topology = {
            "routers": {
                # Main routers from diagram (excluding ISP routers)
                "R1": {
                    "model": "2901",
                    "interfaces": {
                        "g0/0": {"ip": "10.1.12.1", "mask": "255.255.255.252", "connected_to": "R2"},
                        "g0/1": {"ip": "192.168.1.1", "mask": "255.255.255.0", "connected_to": "SW1", "vlan_gateway": True}
                    },
                    "ospf_networks": [
                        {"network": "10.1.12.0", "wildcard": "0.0.0.3", "area": "0"},
                        {"network": "192.168.1.0", "wildcard": "0.0.0.255", "area": "0"}
                    ],
                    "dhcp_pools": [
                        {"name": "VLAN1_POOL", "network": "192.168.1.0", "mask": "255.255.255.0", 
                         "default_router": "192.168.1.1", "dns": "8.8.8.8"}
                    ]
                },
                "R2": {
                    "model": "4331",
                    "interfaces": {
                        "g0/0/0": {"ip": "10.1.12.2", "mask": "255.255.255.252", "connected_to": "R1"},
                        "g0/0/1": {"ip": "10.2.23.1", "mask": "255.255.255.252", "connected_to": "R3"},
                        "g0/1/0": {"ip": "10.2.24.1", "mask": "255.255.255.252", "connected_to": "R4"},
                        "g0/1/1": {"ip": "10.2.25.1", "mask": "255.255.255.252", "connected_to": "R5"},
                        "g0/1/2": {"ip": "192.168.2.1", "mask": "255.255.255.0", "connected_to": "SW2", "vlan_gateway": True}
                    },
                    "ospf_networks": [
                        {"network": "10.1.12.0", "wildcard": "0.0.0.3", "area": "0"},
                        {"network": "10.2.23.0", "wildcard": "0.0.0.3", "area": "0"},
                        {"network": "10.2.24.0", "wildcard": "0.0.0.3", "area": "0"},
                        {"network": "10.2.25.0", "wildcard": "0.0.0.3", "area": "0"},
                        {"network": "192.168.2.0", "wildcard": "0.0.0.255", "area": "0"}
                    ],
                    "dhcp_pools": [
                        {"name": "VLAN2_POOL", "network": "192.168.2.0", "mask": "255.255.255.0", 
                         "default_router": "192.168.2.1", "dns": "8.8.8.8"}
                    ]
                },
                "R3": {
                    "model": "2901",
                    "interfaces": {
                        "g0/0": {"ip": "10.2.23.2", "mask": "255.255.255.252", "connected_to": "R2"},
                        "g0/1": {"ip": "10.3.36.1", "mask": "255.255.255.252", "connected_to": "R6"},
                        "g0/2": {"ip": "192.168.3.1", "mask": "255.255.255.0", "connected_to": "SW3", "vlan_gateway": True}
                    },
                    "ospf_networks": [
                        {"network": "10.2.23.0", "wildcard": "0.0.0.3", "area": "0"},
                        {"network": "10.3.36.0", "wildcard": "0.0.0.3", "area": "0"},
                        {"network": "192.168.3.0", "wildcard": "0.0.0.255", "area": "0"}
                    ],
                    "dhcp_pools": [
                        {"name": "VLAN3_POOL", "network": "192.168.3.0", "mask": "255.255.255.0", 
                         "default_router": "192.168.3.1", "dns": "8.8.8.8"}
                    ]
                },
                "R4": {
                    "model": "2901",
                    "interfaces": {
                        "g0/0": {"ip": "10.2.24.2", "mask": "255.255.255.252", "connected_to": "R2"},
                        "g0/1": {"ip": "192.168.4.1", "mask": "255.255.255.0", "connected_to": "SW4", "vlan_gateway": True}
                    },
                    "ospf_networks": [
                        {"network": "10.2.24.0", "wildcard": "0.0.0.3", "area": "0"},
                        {"network": "192.168.4.0", "wildcard": "0.0.0.255", "area": "0"}
                    ],
                    "dhcp_pools": [
                        {"name": "VLAN4_POOL", "network": "192.168.4.0", "mask": "255.255.255.0", 
                         "default_router": "192.168.4.1", "dns": "8.8.8.8"}
                    ]
                },
                "R5": {
                    "model": "2901",
                    "interfaces": {
                        "g0/0": {"ip": "10.2.25.2", "mask": "255.255.255.252", "connected_to": "R2"},
                        "g0/1": {"ip": "192.168.5.1", "mask": "255.255.255.0", "connected_to": "SW5", "vlan_gateway": True}
                    },
                    "ospf_networks": [
                        {"network": "10.2.25.0", "wildcard": "0.0.0.3", "area": "0"},
                        {"network": "192.168.5.0", "wildcard": "0.0.0.255", "area": "0"}
                    ],
                    "dhcp_pools": [
                        {"name": "VLAN5_POOL", "network": "192.168.5.0", "mask": "255.255.255.0", 
                         "default_router": "192.168.5.1", "dns": "8.8.8.8"}
                    ]
                },
                "R6": {
                    "model": "2901",
                    "interfaces": {
                        "g0/0": {"ip": "10.3.36.2", "mask": "255.255.255.252", "connected_to": "R3"},
                        "g0/1": {"ip": "10.6.67.1", "mask": "255.255.255.252", "connected_to": "R7"},
                        "g0/2": {"ip": "192.168.6.1", "mask": "255.255.255.0", "connected_to": "SW6", "vlan_gateway": True}
                    },
                    "ospf_networks": [
                        {"network": "10.3.36.0", "wildcard": "0.0.0.3", "area": "0"},
                        {"network": "10.6.67.0", "wildcard": "0.0.0.3", "area": "0"},
                        {"network": "192.168.6.0", "wildcard": "0.0.0.255", "area": "0"}
                    ],
                    "dhcp_pools": [
                        {"name": "VLAN6_POOL", "network": "192.168.6.0", "mask": "255.255.255.0", 
                         "default_router": "192.168.6.1", "dns": "8.8.8.8"}
                    ]
                },
                "R7": {
                    "model": "2901",
                    "interfaces": {
                        "g0/0": {"ip": "10.6.67.2", "mask": "255.255.255.252", "connected_to": "R6"},
                        "g0/1": {"ip": "10.7.78.1", "mask": "255.255.255.252", "connected_to": "R8"},
                        "g0/2": {"ip": "192.168.7.1", "mask": "255.255.255.0", "connected_to": "SW7", "vlan_gateway": True}
                    },
                    "ospf_networks": [
                        {"network": "10.6.67.0", "wildcard": "0.0.0.3", "area": "0"},
                        {"network": "10.7.78.0", "wildcard": "0.0.0.3", "area": "0"},
                        {"network": "192.168.7.0", "wildcard": "0.0.0.255", "area": "0"}
                    ],
                    "dhcp_pools": [
                        {"name": "VLAN7_POOL", "network": "192.168.7.0", "mask": "255.255.255.0", 
                         "default_router": "192.168.7.1", "dns": "8.8.8.8"}
                    ]
                },
                "R8": {
                    "model": "2901",
                    "interfaces": {
                        "g0/0": {"ip": "10.7.78.2", "mask": "255.255.255.252", "connected_to": "R7"},
                        "g0/1": {"ip": "192.168.8.1", "mask": "255.255.255.0", "connected_to": "SW8", "vlan_gateway": True}
                    },
                    "ospf_networks": [
                        {"network": "10.7.78.0", "wildcard": "0.0.0.3", "area": "0"},
                        {"network": "192.168.8.0", "wildcard": "0.0.0.255", "area": "0"}
                    ],
                    "dhcp_pools": [
                        {"name": "VLAN8_POOL", "network": "192.168.8.0", "mask": "255.255.255.0", 
                         "default_router": "192.168.8.1", "dns": "8.8.8.8"}
                    ]
                },
                # Lower section routers (R11-R16)
                "R11": {
                    "model": "2901",
                    "interfaces": {
                        "g0/0": {"ip": "10.11.12.1", "mask": "255.255.255.252", "connected_to": "R12"},
                        "g0/1": {"ip": "192.168.11.1", "mask": "255.255.255.0", "connected_to": "SW11", "vlan_gateway": True}
                    },
                    "ospf_networks": [
                        {"network": "10.11.12.0", "wildcard": "0.0.0.3", "area": "1"},
                        {"network": "192.168.11.0", "wildcard": "0.0.0.255", "area": "1"}
                    ],
                    "dhcp_pools": [
                        {"name": "VLAN11_POOL", "network": "192.168.11.0", "mask": "255.255.255.0", 
                         "default_router": "192.168.11.1", "dns": "8.8.8.8"}
                    ]
                },
                "R12": {
                    "model": "2901",
                    "interfaces": {
                        "g0/0": {"ip": "10.11.12.2", "mask": "255.255.255.252", "connected_to": "R11"},
                        "g0/1": {"ip": "10.12.13.1", "mask": "255.255.255.252", "connected_to": "R13"},
                        "g0/2": {"ip": "192.168.12.1", "mask": "255.255.255.0", "connected_to": "SW12", "vlan_gateway": True}
                    },
                    "ospf_networks": [
                        {"network": "10.11.12.0", "wildcard": "0.0.0.3", "area": "1"},
                        {"network": "10.12.13.0", "wildcard": "0.0.0.3", "area": "1"},
                        {"network": "192.168.12.0", "wildcard": "0.0.0.255", "area": "1"}
                    ],
                    "dhcp_pools": [
                        {"name": "VLAN12_POOL", "network": "192.168.12.0", "mask": "255.255.255.0", 
                         "default_router": "192.168.12.1", "dns": "8.8.8.8"}
                    ]
                },
                "R13": {
                    "model": "2901",
                    "interfaces": {
                        "g0/0": {"ip": "10.12.13.2", "mask": "255.255.255.252", "connected_to": "R12"},
                        "g0/1": {"ip": "10.13.14.1", "mask": "255.255.255.252", "connected_to": "R14"},
                        "g0/2": {"ip": "192.168.13.1", "mask": "255.255.255.0", "connected_to": "SW13", "vlan_gateway": True}
                    },
                    "ospf_networks": [
                        {"network": "10.12.13.0", "wildcard": "0.0.0.3", "area": "1"},
                        {"network": "10.13.14.0", "wildcard": "0.0.0.3", "area": "1"},
                        {"network": "192.168.13.0", "wildcard": "0.0.0.255", "area": "1"}
                    ],
                    "dhcp_pools": [
                        {"name": "VLAN13_POOL", "network": "192.168.13.0", "mask": "255.255.255.0", 
                         "default_router": "192.168.13.1", "dns": "8.8.8.8"}
                    ]
                },
                "R14": {
                    "model": "2901",
                    "interfaces": {
                        "g0/0": {"ip": "10.13.14.2", "mask": "255.255.255.252", "connected_to": "R13"},
                        "g0/1": {"ip": "10.14.15.1", "mask": "255.255.255.252", "connected_to": "R15"},
                        "g0/2": {"ip": "192.168.14.1", "mask": "255.255.255.0", "connected_to": "SW14", "vlan_gateway": True}
                    },
                    "ospf_networks": [
                        {"network": "10.13.14.0", "wildcard": "0.0.0.3", "area": "1"},
                        {"network": "10.14.15.0", "wildcard": "0.0.0.3", "area": "1"},
                        {"network": "192.168.14.0", "wildcard": "0.0.0.255", "area": "1"}
                    ],
                    "dhcp_pools": [
                        {"name": "VLAN14_POOL", "network": "192.168.14.0", "mask": "255.255.255.0", 
                         "default_router": "192.168.14.1", "dns": "8.8.8.8"}
                    ]
                },
                "R15": {
                    "model": "2901",
                    "interfaces": {
                        "g0/0": {"ip": "10.14.15.2", "mask": "255.255.255.252", "connected_to": "R14"},
                        "g0/1": {"ip": "10.15.16.1", "mask": "255.255.255.252", "connected_to": "R16"},
                        "g0/2": {"ip": "192.168.15.1", "mask": "255.255.255.0", "connected_to": "SW15", "vlan_gateway": True}
                    },
                    "ospf_networks": [
                        {"network": "10.14.15.0", "wildcard": "0.0.0.3", "area": "1"},
                        {"network": "10.15.16.0", "wildcard": "0.0.0.3", "area": "1"},
                        {"network": "192.168.15.0", "wildcard": "0.0.0.255", "area": "1"}
                    ],
                    "dhcp_pools": [
                        {"name": "VLAN15_POOL", "network": "192.168.15.0", "mask": "255.255.255.0", 
                         "default_router": "192.168.15.1", "dns": "8.8.8.8"}
                    ]
                },
                "R16": {
                    "model": "2901",
                    "interfaces": {
                        "g0/0": {"ip": "10.15.16.2", "mask": "255.255.255.252", "connected_to": "R15"},
                        "g0/1": {"ip": "192.168.16.1", "mask": "255.255.255.0", "connected_to": "SW16", "vlan_gateway": True}
                    },
                    "ospf_networks": [
                        {"network": "10.15.16.0", "wildcard": "0.0.0.3", "area": "1"},
                        {"network": "192.168.16.0", "wildcard": "0.0.0.255", "area": "1"}
                    ],
                    "dhcp_pools": [
                        {"name": "VLAN16_POOL", "network": "192.168.16.0", "mask": "255.255.255.0", 
                         "default_router": "192.168.16.1", "dns": "8.8.8.8"}
                    ]
                }
            },
            "switches": {
                # Upper section switches
                "SW1": {
                    "vlans": {"1": "VLAN1_DHCP", "99": "MANAGEMENT"},
                    "trunk_ports": ["g0/1"],
                    "access_ports": {"f0/1": "1", "f0/2": "1", "f0/3": "1", "f0/4": "1"},
                    "management_ip": "192.168.1.10",
                    "default_gateway": "192.168.1.1"
                },
                "SW2": {
                    "vlans": {"2": "VLAN2_DHCP", "99": "MANAGEMENT"},
                    "trunk_ports": ["g0/1"],
                    "access_ports": {"f0/1": "2", "f0/2": "2", "f0/3": "2", "f0/4": "2"},
                    "management_ip": "192.168.2.10",
                    "default_gateway": "192.168.2.1"
                },
                "SW3": {
                    "vlans": {"3": "VLAN3_DHCP", "99": "MANAGEMENT"},
                    "trunk_ports": ["g0/1"],
                    "access_ports": {"f0/1": "3", "f0/2": "3", "f0/3": "3", "f0/4": "3"},
                    "management_ip": "192.168.3.10",
                    "default_gateway": "192.168.3.1"
                },
                "SW4": {
                    "vlans": {"4": "VLAN4_DHCP", "99": "MANAGEMENT"},
                    "trunk_ports": ["g0/1"],
                    "access_ports": {"f0/1": "4", "f0/2": "4", "f0/3": "4", "f0/4": "4"},
                    "management_ip": "192.168.4.10",
                    "default_gateway": "192.168.4.1"
                },
                "SW5": {
                    "vlans": {"5": "VLAN5_DHCP", "99": "MANAGEMENT"},
                    "trunk_ports": ["g0/1"],
                    "access_ports": {"f0/1": "5", "f0/2": "5", "f0/3": "5", "f0/4": "5"},
                    "management_ip": "192.168.5.10",
                    "default_gateway": "192.168.5.1"
                },
                "SW6": {
                    "vlans": {"6": "VLAN6_DHCP", "99": "MANAGEMENT"},
                    "trunk_ports": ["g0/1"],
                    "access_ports": {"f0/1": "6", "f0/2": "6", "f0/3": "6", "f0/4": "6"},
                    "management_ip": "192.168.6.10",
                    "default_gateway": "192.168.6.1"
                },
                "SW7": {
                    "vlans": {"7": "VLAN7_DHCP", "99": "MANAGEMENT"},
                    "trunk_ports": ["g0/1"],
                    "access_ports": {"f0/1": "7", "f0/2": "7", "f0/3": "7", "f0/4": "7"},
                    "management_ip": "192.168.7.10",
                    "default_gateway": "192.168.7.1"
                },
                "SW8": {
                    "vlans": {"8": "VLAN8_DHCP", "99": "MANAGEMENT"},
                    "trunk_ports": ["g0/1"],
                    "access_ports": {"f0/1": "8", "f0/2": "8", "f0/3": "8", "f0/4": "8"},
                    "management_ip": "192.168.8.10",
                    "default_gateway": "192.168.8.1"
                },
                # Lower section switches
                "SW11": {
                    "vlans": {"11": "VLAN11_DHCP", "99": "MANAGEMENT"},
                    "trunk_ports": ["g0/1"],
                    "access_ports": {"f0/1": "11", "f0/2": "11", "f0/3": "11", "f0/4": "11"},
                    "management_ip": "192.168.11.10",
                    "default_gateway": "192.168.11.1"
                },
                "SW12": {
                    "vlans": {"12": "VLAN12_DHCP", "99": "MANAGEMENT"},
                    "trunk_ports": ["g0/1"],
                    "access_ports": {"f0/1": "12", "f0/2": "12", "f0/3": "12", "f0/4": "12"},
                    "management_ip": "192.168.12.10",
                    "default_gateway": "192.168.12.1"
                },
                "SW13": {
                    "vlans": {"13": "VLAN13_DHCP", "99": "MANAGEMENT"},
                    "trunk_ports": ["g0/1"],
                    "access_ports": {"f0/1": "13", "f0/2": "13", "f0/3": "13", "f0/4": "13"},
                    "management_ip": "192.168.13.10",
                    "default_gateway": "192.168.13.1"
                },
                "SW14": {
                    "vlans": {"14": "VLAN14_DHCP", "99": "MANAGEMENT"},
                    "trunk_ports": ["g0/1"],
                    "access_ports": {"f0/1": "14", "f0/2": "14", "f0/3": "14", "f0/4": "14"},
                    "management_ip": "192.168.14.10",
                    "default_gateway": "192.168.14.1"
                },
                "SW15": {
                    "vlans": {"15": "VLAN15_DHCP", "99": "MANAGEMENT"},
                    "trunk_ports": ["g0/1"],
                    "access_ports": {"f0/1": "15", "f0/2": "15", "f0/3": "15", "f0/4": "15"},
                    "management_ip": "192.168.15.10",
                    "default_gateway": "192.168.15.1"
                },
                "SW16": {
                    "vlans": {"16": "VLAN16_DHCP", "99": "MANAGEMENT"},
                    "trunk_ports": ["g0/1"],
                    "access_ports": {"f0/1": "16", "f0/2": "16", "f0/3": "16", "f0/4": "16"},
                    "management_ip": "192.168.16.10",
                    "default_gateway": "192.168.16.1"
                }
            },
            "servers": {
                # Upper section servers (excluding ISP servers)
                "S1": {"ip": "192.168.1.100", "mask": "255.255.255.0", "gateway": "192.168.1.1", "vlan": "1"},
                "S2": {"ip": "192.168.2.100", "mask": "255.255.255.0", "gateway": "192.168.2.1", "vlan": "2"},
                "S3": {"ip": "192.168.3.100", "mask": "255.255.255.0", "gateway": "192.168.3.1", "vlan": "3"},
                "S4": {"ip": "192.168.4.100", "mask": "255.255.255.0", "gateway": "192.168.4.1", "vlan": "4"},
                "S5": {"ip": "192.168.5.100", "mask": "255.255.255.0", "gateway": "192.168.5.1", "vlan": "5"},
                "S6": {"ip": "192.168.6.100", "mask": "255.255.255.0", "gateway": "192.168.6.1", "vlan": "6"},
                "S8": {"ip": "192.168.8.100", "mask": "255.255.255.0", "gateway": "192.168.8.1", "vlan": "8"},
                # Lower section servers
                "S11": {"ip": "192.168.11.100", "mask": "255.255.255.0", "gateway": "192.168.11.1", "vlan": "11"},
                "S12": {"ip": "192.168.12.100", "mask": "255.255.255.0", "gateway": "192.168.12.1", "vlan": "12"},
                "S13": {"ip": "192.168.13.100", "mask": "255.255.255.0", "gateway": "192.168.13.1", "vlan": "13"},
                "S14": {"ip": "192.168.14.100", "mask": "255.255.255.0", "gateway": "192.168.14.1", "vlan": "14"},
                "S15": {"ip": "192.168.15.100", "mask": "255.255.255.0", "gateway": "192.168.15.1", "vlan": "15"},
                "S16": {"ip": "192.168.16.100", "mask": "255.255.255.0", "gateway": "192.168.16.1", "vlan": "16"}
            }
        }
    
    def generate_router_config(self, router_name):
        """Generate complete router configuration with DHCP and OSPF"""
        router_data = self.network_topology["routers"][router_name]
        model = router_data.get("model", "2901")
        
        config = f"""!
! {router_name} Configuration - Enhanced Task 2 Network ({model})
! Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
! Excludes ISP devices as specified
!
version 15.1
no service timestamps log datetime msec
no service timestamps debug datetime msec
no service password-encryption
!
hostname {router_name}
!
enable secret 5 $1$mERr$9cTjUIEqNGurQiFU.ZeCi1
!
ip cef
no ipv6 cef
!
username admin privilege 15 secret 5 $1$mERr$9cTjUIEqNGurQiFU.ZeCi1
!
spanning-tree mode pvst
!
"""
        
        # Add DHCP pools if they exist
        if "dhcp_pools" in router_data:
            for pool in router_data["dhcp_pools"]:
                config += f"""!
ip dhcp pool {pool['name']}
 network {pool['network']} {pool['mask']}
 default-router {pool['default_router']}
 dns-server {pool['dns']}
!
"""
        
        # Add interface configurations
        for interface, config_data in router_data["interfaces"].items():
            # Handle different interface naming for 4331 vs 2901
            if model == "4331":
                interface_name = f"GigabitEthernet{interface}"
            else:
                interface_name = f"GigabitEthernet{interface}"
                
            config += f"""!
interface {interface_name}
 description Connected to {config_data['connected_to']}
 ip address {config_data['ip']} {config_data['mask']}
"""
            # Add DHCP helper if this is a VLAN gateway
            if config_data.get("vlan_gateway"):
                config += f" ip helper-address {config_data['ip']}\n"
            
            config += """ duplex auto
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
banner motd ^C
******************************************
*        AUTHORIZED ACCESS ONLY         *
*   Enhanced Task 2 Network - """ + router_name + f""" ({model})   *
*     ISP devices excluded as requested *
******************************************
^C
!
line con 0
 password cisco
 login
!
line vty 0 4
 password cisco
 login local
 transport input ssh
!
end
"""
        return config
    
    def generate_switch_config(self, switch_name):
        """Generate complete switch configuration"""
        switch_data = self.network_topology["switches"][switch_name]
        
        config = f"""!
! {switch_name} Configuration - Enhanced Task 2 Network
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
banner motd ^C
******************************************
*        AUTHORIZED ACCESS ONLY         *
*   Enhanced Task 2 Network - {switch_name}     *
******************************************
^C
!
line con 0
 password cisco
 login
!
line vty 0 15
 password cisco
 login
!
end
"""
        return config
    
    def generate_server_config(self, server_name):
        """Generate server configuration for Packet Tracer"""
        server_data = self.network_topology["servers"][server_name]
        
        config = f"""# {server_name} Configuration - Enhanced Task 2 Network
# Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# ISP servers excluded as requested

# Static IP Configuration
IP Address: {server_data['ip']}
Subnet Mask: {server_data['mask']}
Default Gateway: {server_data['gateway']}
DNS Server: 8.8.8.8

# VLAN Assignment: {server_data['vlan']}
# Network: {server_data['gateway'].rsplit('.', 1)[0]}.0/24

# Services Configuration:
# - Web Server (HTTP/HTTPS)
# - FTP Server
# - DNS Server (optional)
# - DHCP Relay (configured on router)

# Test Commands:
# ping {server_data['gateway']}  (Test gateway connectivity)
# ping 8.8.8.8             (Test internet connectivity - will fail without ISP)
# ipconfig                 (View IP configuration)
"""
        return config
    
    def create_packet_tracer_instructions(self):
        """Create comprehensive Packet Tracer setup instructions"""
        instructions = f"""
# Enhanced Task 2 Network - Packet Tracer Setup Instructions
Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## IMPORTANT: ISP Devices Excluded
This configuration excludes the following devices as requested:
- Local ISP R1, R2, R3, R4
- ISP S1, S2, S3, S4 (3650 models in middle)
- ISP Remote devices
- 4331 ISP Remote (ping 9.9.9.9)

## Step 1: Add Devices to Workspace

### Routers (13 total):
- 1 x Cisco 4331 Router (R2) - **Requires interface modules**
- 12 x Cisco 2901 Routers (R1, R3-R8, R11-R16)

### Switches (16 total):
- 16 x Cisco 2960 Switches (SW1-SW8, SW11-SW16)

### Servers (13 total):
- 13 x Generic Servers (S1-S8, S11-S16, excluding ISP servers)

## Step 2: R2 (4331) Interface Module Setup
**CRITICAL**: R2 needs additional interfaces to connect to 4 routers

1. Power off R2
2. Add interface module: **EHWIC-4ESG** (4-port Gigabit Ethernet)
3. Power on R2
4. Verify interfaces: G0/0/0, G0/0/1, G0/1/0, G0/1/1, G0/1/2, G0/1/3

## Step 3: Physical Connections

### Upper Section Router-to-Router Links:
- R1 G0/0 <-> R2 G0/0/0
- R2 G0/0/1 <-> R3 G0/0  
- R2 G0/1/0 <-> R4 G0/0
- R2 G0/1/1 <-> R5 G0/0
- R3 G0/1 <-> R6 G0/0
- R6 G0/1 <-> R7 G0/0
- R7 G0/1 <-> R8 G0/0

### Lower Section Router-to-Router Links:
- R11 G0/0 <-> R12 G0/0
- R12 G0/1 <-> R13 G0/0
- R13 G0/1 <-> R14 G0/0
- R14 G0/1 <-> R15 G0/0
- R15 G0/1 <-> R16 G0/0

### Router-to-Switch Links:
- R1 G0/1 <-> SW1 G0/1
- R2 G0/1/2 <-> SW2 G0/1
- R3 G0/2 <-> SW3 G0/1
- R4 G0/1 <-> SW4 G0/1
- R5 G0/1 <-> SW5 G0/1
- R6 G0/2 <-> SW6 G0/1
- R7 G0/2 <-> SW7 G0/1
- R8 G0/1 <-> SW8 G0/1
- R11 G0/1 <-> SW11 G0/1
- R12 G0/2 <-> SW12 G0/1
- R13 G0/2 <-> SW13 G0/1
- R14 G0/2 <-> SW14 G0/1
- R15 G0/2 <-> SW15 G0/1
- R16 G0/1 <-> SW16 G0/1

### Switch-to-Server Links:
- Each switch F0/1 <-> Corresponding server (S1-S8, S11-S16)

## Step 4: Configure Devices
Copy configurations from generated files to device CLI:

### Routers:
- R1_config.txt -> R1 CLI
- R2_config.txt -> R2 CLI (4331 with modules)
- R3_config.txt -> R3 CLI
- ... (continue for all routers)

### Switches:
- SW1_config.txt -> SW1 CLI
- SW2_config.txt -> SW2 CLI
- ... (continue for all switches)

### Servers:
Configure IP addresses from Server_configs.txt

## Step 5: Network Areas
- **Area 0**: Upper section (R1-R8) - Main backbone
- **Area 1**: Lower section (R11-R16) - Branch networks

## Step 6: DHCP Configuration
Each router provides DHCP for its local VLAN:
- R1: 192.168.1.0/24 (VLAN 1)
- R2: 192.168.2.0/24 (VLAN 2)
- ... (continue for all VLANs)

## Step 7: Verification Commands

### On Routers:
- show ip route ospf
- show ip ospf neighbor
- show ip dhcp binding
- show ip interface brief

### On Switches:
- show vlan brief
- show interface trunk
- show spanning-tree

### On Servers:
- ipconfig
- ping [gateway]
- ping [remote_server]

## Step 8: Testing Scenarios
1. **DHCP Testing**: Connect PCs to access ports, verify DHCP assignment
2. **Inter-VLAN Routing**: Test communication between different VLANs
3. **OSPF Convergence**: Shut down links, verify route recalculation
4. **Area Communication**: Test Area 0 <-> Area 1 communication

## Expected Results
- All OSPF neighbors in FULL state
- DHCP clients receive IP addresses automatically
- Inter-VLAN communication works
- Network has redundant paths
- **Note**: No internet connectivity (ISP devices excluded)

## Troubleshooting Tips
1. **R2 Interface Issues**: Ensure EHWIC-4ESG module is properly installed
2. **OSPF Problems**: Check area assignments and network statements
3. **DHCP Issues**: Verify ip helper-address on VLAN interfaces
4. **VLAN Problems**: Check trunk configurations and VLAN assignments

## Network Topology Summary
- **13 Routers**: 1x 4331, 12x 2901
- **16 Switches**: All 2960 models
- **13 Servers**: Excluding ISP servers as requested
- **2 OSPF Areas**: Area 0 (upper), Area 1 (lower)
- **16 VLANs**: Each with DHCP service
"""
        return instructions
    
    def generate_all_configs(self):
        """Generate all configuration files for the enhanced network"""
        # Create output directory
        output_dir = "Enhanced_Task2_Network_Configs"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        print(f"Generating Enhanced Task 2 Network Configurations...")
        print(f"Output directory: {output_dir}")
        print(f"Excluding ISP devices as requested")
        
        # Generate router configs
        print(f"\nGenerating Router Configurations ({len(self.network_topology['routers'])} routers)...")
        for router_name in self.network_topology["routers"]:
            config = self.generate_router_config(router_name)
            filename = f"{output_dir}/{router_name}_config.txt"
            with open(filename, 'w') as f:
                f.write(config)
            model = self.network_topology["routers"][router_name].get("model", "2901")
            print(f"   [OK] {router_name}_config.txt ({model})")
        
        # Generate switch configs
        print(f"\nGenerating Switch Configurations ({len(self.network_topology['switches'])} switches)...")
        for switch_name in self.network_topology["switches"]:
            config = self.generate_switch_config(switch_name)
            filename = f"{output_dir}/{switch_name}_config.txt"
            with open(filename, 'w') as f:
                f.write(config)
            print(f"   [OK] {switch_name}_config.txt")
        
        # Generate server configs
        print(f"\nGenerating Server Configurations ({len(self.network_topology['servers'])} servers)...")
        server_configs = ""
        for server_name in self.network_topology["servers"]:
            server_configs += self.generate_server_config(server_name) + "\n" + "="*60 + "\n"
        
        with open(f"{output_dir}/Server_configs.txt", 'w') as f:
            f.write(server_configs)
        print(f"   [OK] Server_configs.txt")
        
        # Generate documentation
        print(f"\nGenerating Documentation...")
        instructions = self.create_packet_tracer_instructions()
        with open(f"{output_dir}/Enhanced_Packet_Tracer_Instructions.md", 'w') as f:
            f.write(instructions)
        print(f"   [OK] Enhanced_Packet_Tracer_Instructions.md")
        
        # Generate topology JSON for reference
        with open(f"{output_dir}/enhanced_network_topology.json", 'w') as f:
            json.dump(self.network_topology, f, indent=2)
        print(f"   [OK] enhanced_network_topology.json")
        
        # Generate device summary
        summary = f"""
# Enhanced Task 2 Network - Device Summary
Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Devices Included:
- **Routers**: {len(self.network_topology['routers'])} (1x 4331, 12x 2901)
- **Switches**: {len(self.network_topology['switches'])} (All 2960)
- **Servers**: {len(self.network_topology['servers'])} (Excluding ISP servers)

## Devices Excluded (as requested):
- Local ISP R1, R2, R3, R4
- ISP S1, S2, S3, S4 (3650 models)
- ISP Remote devices
- 4331 ISP Remote (ping 9.9.9.9)

## Key Features:
- OSPF routing with 2 areas
- DHCP services on all routers
- VLAN segmentation
- Port security on switches
- Management VLANs
- Redundant paths (where applicable)

## Special Requirements:
- R2 (4331) requires EHWIC-4ESG module for 4 connections
- No internet connectivity (ISP excluded)
- Area 0: Upper section, Area 1: Lower section
"""
        
        with open(f"{output_dir}/Device_Summary.md", 'w') as f:
            f.write(summary)
        print(f"   [OK] Device_Summary.md")
        
        print(f"\nEnhanced Task 2 Network Generation Complete!")
        print(f"Files created in '{output_dir}' directory:")
        print(f"   - {len(self.network_topology['routers'])} Router configuration files")
        print(f"   - {len(self.network_topology['switches'])} Switch configuration files") 
        print(f"   - Server configuration file")
        print(f"   - Enhanced setup instructions")
        print(f"   - Device summary and topology reference")
        print(f"\nIMPORTANT: R2 (4331) needs EHWIC-4ESG module!")
        
        return output_dir

def main():
    """Main function to generate the enhanced network"""
    print("=" * 70)
    print("ENHANCED TASK 2 NETWORK AUTOMATION GENERATOR")
    print("ISP DEVICES EXCLUDED AS REQUESTED")
    print("=" * 70)
    
    generator = EnhancedTask2NetworkGenerator()
    output_dir = generator.generate_all_configs()
    
    print(f"\nNext Steps:")
    print(f"1. Open Packet Tracer")
    print(f"2. Add EHWIC-4ESG module to R2 (4331 router)")
    print(f"3. Follow instructions in '{output_dir}/Enhanced_Packet_Tracer_Instructions.md'")
    print(f"4. Copy configurations from the generated .txt files")
    print(f"5. Test network connectivity using verification commands")
    
    print(f"\nYour enhanced Task 2 network is ready to deploy!")
    print(f"Remember: R2 needs interface module for 4 connections!")

if __name__ == "__main__":
    main()
