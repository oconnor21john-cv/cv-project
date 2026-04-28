#!/usr/bin/env python3
"""
Advanced Configuration Generator
Uses Jinja2 templates to generate device configurations from inventory
"""

import os
import json
import yaml
from datetime import datetime
from typing import Dict, List, Any, Optional
from jinja2 import Environment, FileSystemLoader, Template
from pathlib import Path

from inventory.network_inventory import NetworkInventory, NetworkDevice

class ConfigurationGenerator:
    """Advanced configuration generator using Jinja2 templates"""
    
    def __init__(self, template_dir: str = "templates", output_dir: str = "configs"):
        self.template_dir = Path(template_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize Jinja2 environment
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Add custom filters
        self.jinja_env.filters['subnet_to_wildcard'] = self._subnet_to_wildcard
        self.jinja_env.filters['ip_to_network'] = self._ip_to_network
        
    def _subnet_to_wildcard(self, subnet_mask: str) -> str:
        """Convert subnet mask to wildcard mask"""
        octets = subnet_mask.split('.')
        wildcard_octets = [str(255 - int(octet)) for octet in octets]
        return '.'.join(wildcard_octets)
        
    def _ip_to_network(self, ip_address: str, subnet_mask: str) -> str:
        """Get network address from IP and subnet mask"""
        from ipaddress import IPv4Network
        network = IPv4Network(f"{ip_address}/{subnet_mask}", strict=False)
        return str(network.network_address)
        
    def generate_router_config(self, device: NetworkDevice, 
                             ospf_config: Optional[Dict] = None,
                             static_routes: Optional[List[Dict]] = None,
                             **kwargs) -> str:
        """Generate router configuration"""
        template = self.jinja_env.get_template('router_template.j2')
        
        # Prepare OSPF configuration
        if not ospf_config and device.device_type == "router":
            ospf_config = self._generate_ospf_config(device)
            
        context = {
            'device': device,
            'generation_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ospf_config': ospf_config,
            'static_routes': static_routes,
            **kwargs
        }
        
        return template.render(**context)
        
    def generate_switch_config(self, device: NetworkDevice,
                             vlans: Optional[Dict] = None,
                             port_security: Optional[Dict] = None,
                             **kwargs) -> str:
        """Generate switch configuration"""
        template = self.jinja_env.get_template('switch_template.j2')
        
        # Default VLAN configuration for Task 2
        if not vlans:
            vlans = {
                10: {"name": "SALES", "description": "Sales Department"},
                20: {"name": "MARKETING", "description": "Marketing Department"},
                30: {"name": "IT", "description": "IT Department"},
                40: {"name": "FINANCE", "description": "Finance Department"},
                99: {"name": "MANAGEMENT", "description": "Management VLAN"}
            }
            
        # Default port security
        if not port_security:
            port_security = {
                "max_addresses": 2,
                "violation_action": "shutdown"
            }
            
        # Default management configuration
        management_config = {
            "default_gateway": self._get_default_gateway(device)
        }
        
        # Unused port ranges (for 2960 switch)
        unused_port_ranges = ["FastEthernet0/5-24"] if device.model == "Cisco 2960" else []
        
        context = {
            'device': device,
            'generation_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'vlans': vlans,
            'port_security': port_security,
            'management_config': management_config,
            'trunk_native_vlan': 99,
            'trunk_allowed_vlans': "all",
            'shutdown_unused_ports': True,
            'unused_port_ranges': unused_port_ranges,
            **kwargs
        }
        
        return template.render(**context)
        
    def _generate_ospf_config(self, device: NetworkDevice) -> Dict:
        """Generate OSPF configuration for a router"""
        networks = []
        
        for interface in device.interfaces:
            if interface.ip_address and interface.ip_address != "":
                network_addr = self._ip_to_network(interface.ip_address, interface.subnet_mask)
                wildcard = self._subnet_to_wildcard(interface.subnet_mask)
                
                networks.append({
                    "network": network_addr,
                    "wildcard": wildcard,
                    "area": 0
                })
                
        return {
            "process_id": 1,
            "networks": networks
        }
        
    def _get_default_gateway(self, device: NetworkDevice) -> str:
        """Get default gateway for switch management"""
        # Extract network from management IP and assume .1 is the gateway
        mgmt_ip = device.mgmt_ip
        if mgmt_ip:
            octets = mgmt_ip.split('.')
            octets[-1] = '1'
            return '.'.join(octets)
        return ""
        
    def generate_device_config(self, device: NetworkDevice, **kwargs) -> str:
        """Generate configuration for any device type"""
        if device.device_type == "router":
            return self.generate_router_config(device, **kwargs)
        elif device.device_type == "switch":
            return self.generate_switch_config(device, **kwargs)
        else:
            raise ValueError(f"Unsupported device type: {device.device_type}")
            
    def generate_all_configs(self, inventory: NetworkInventory, 
                           save_to_files: bool = True) -> Dict[str, str]:
        """Generate configurations for all devices in inventory"""
        configs = {}
        
        print("🔧 Generating device configurations...")
        
        # Generate router configs
        routers = inventory.get_routers()
        for router in routers:
            print(f"   📡 Generating {router.hostname} configuration...")
            config = self.generate_device_config(router)
            configs[router.hostname] = config
            
            if save_to_files:
                filename = self.output_dir / f"{router.hostname}_config.txt"
                with open(filename, 'w') as f:
                    f.write(config)
                    
        # Generate switch configs
        switches = inventory.get_switches()
        for switch in switches:
            print(f"   🔀 Generating {switch.hostname} configuration...")
            config = self.generate_device_config(switch)
            configs[switch.hostname] = config
            
            if save_to_files:
                filename = self.output_dir / f"{switch.hostname}_config.txt"
                with open(filename, 'w') as f:
                    f.write(config)
                    
        print(f"✅ Generated {len(configs)} device configurations")
        return configs
        
    def generate_pc_configs(self, inventory: NetworkInventory, 
                          save_to_file: bool = True) -> str:
        """Generate PC configuration guide"""
        pcs = inventory.get_pcs()
        
        config_text = f"""# PC Configuration Guide - Task 2 Network
# Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
        
        for pc in pcs:
            interface = pc.interfaces[0]  # PCs have one interface
            vlan_info = self._get_vlan_info(interface.vlan)
            
            config_text += f"""{'='*50}
{pc.hostname} Configuration
{'='*50}
IP Address: {interface.ip_address}
Subnet Mask: {interface.subnet_mask}
Default Gateway: {self._get_pc_gateway(interface.ip_address)}
DNS Server: 8.8.8.8

VLAN Assignment: {interface.vlan} ({vlan_info})
Network: {self._ip_to_network(interface.ip_address, interface.subnet_mask)}/24

Test Commands:
- ping {self._get_pc_gateway(interface.ip_address)}  (Test gateway connectivity)
- ipconfig                                          (View IP configuration)

"""
        
        if save_to_file:
            filename = self.output_dir / "PC_configs.txt"
            with open(filename, 'w') as f:
                f.write(config_text)
                
        return config_text
        
    def _get_vlan_info(self, vlan_id: int) -> str:
        """Get VLAN name from VLAN ID"""
        vlan_names = {10: "Sales", 20: "Marketing", 30: "IT", 40: "Finance", 99: "Management"}
        return vlan_names.get(vlan_id, f"VLAN{vlan_id}")
        
    def _get_pc_gateway(self, ip_address: str) -> str:
        """Get gateway IP for PC"""
        octets = ip_address.split('.')
        octets[-1] = '1'
        return '.'.join(octets)
        
    def create_deployment_summary(self, inventory: NetworkInventory, 
                                configs: Dict[str, str]) -> str:
        """Create deployment summary document"""
        summary = f"""# Task 2 Network Deployment Summary
Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Network Overview
- **Total Devices:** {len(inventory.devices)}
- **Routers:** {len(inventory.get_routers())}
- **Switches:** {len(inventory.get_switches())}
- **PCs:** {len(inventory.get_pcs())}
- **VLANs:** {len(inventory.vlans)}
- **Physical Connections:** {len(inventory.connections)}

## Generated Configurations
"""
        
        for device_name in sorted(configs.keys()):
            device = inventory.get_device(device_name)
            config_size = len(configs[device_name])
            summary += f"- **{device_name}** ({device.device_type}): {config_size:,} characters\n"
            
        summary += f"""
## Network Addressing
"""
        
        for name, network in inventory.networks.items():
            summary += f"- **{name}:** {network}\n"
            
        summary += f"""
## VLAN Configuration
"""
        
        for vlan_id, vlan_info in inventory.vlans.items():
            summary += f"- **VLAN {vlan_id}:** {vlan_info['name']}\n"
            
        summary += f"""
## Deployment Instructions
1. Load configurations into respective devices
2. Verify physical connections match topology
3. Test OSPF neighbor relationships
4. Validate inter-VLAN routing
5. Confirm end-to-end connectivity

## Validation Commands
### Routers:
- `show ip route`
- `show ip ospf neighbor`
- `show ip interface brief`

### Switches:
- `show vlan brief`
- `show interface trunk`
- `show mac address-table`

### PCs:
- `ipconfig`
- `ping [gateway]`
- `ping [remote_host]`
"""
        
        filename = self.output_dir / "deployment_summary.md"
        with open(filename, 'w') as f:
            f.write(summary)
            
        return summary

def main():
    """Main function for testing configuration generation"""
    from inventory.network_inventory import create_task2_inventory
    
    print("🚀 Advanced Configuration Generator")
    print("=" * 50)
    
    # Create inventory
    print("📋 Loading network inventory...")
    inventory = create_task2_inventory()
    
    # Initialize generator
    generator = ConfigurationGenerator()
    
    # Generate all configurations
    configs = generator.generate_all_configs(inventory)
    
    # Generate PC configurations
    print("💻 Generating PC configurations...")
    generator.generate_pc_configs(inventory)
    
    # Create deployment summary
    print("📊 Creating deployment summary...")
    generator.create_deployment_summary(inventory, configs)
    
    print(f"\n🎉 Configuration generation complete!")
    print(f"📁 Output directory: {generator.output_dir}")
    print(f"📄 Files generated: {len(configs) + 2}")  # +2 for PC configs and summary
    
if __name__ == "__main__":
    main()

