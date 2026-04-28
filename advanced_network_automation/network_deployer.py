#!/usr/bin/env python3
"""
Advanced Network Deployment Engine
Uses Netmiko to deploy configurations to network devices
"""

import os
import time
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

try:
    from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
    from netmiko.exceptions import NetmikoBaseException
    NETMIKO_AVAILABLE = True
except ImportError:
    NETMIKO_AVAILABLE = False
    print("⚠️  Netmiko not available. Install with: pip install netmiko")

from inventory.network_inventory import NetworkInventory, NetworkDevice
from config_generator import ConfigurationGenerator

class NetworkDeployer:
    """Advanced network deployment using Netmiko"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Setup logging
        self.setup_logging()
        
        # Deployment statistics
        self.stats = {
            "total_devices": 0,
            "successful_deployments": 0,
            "failed_deployments": 0,
            "start_time": None,
            "end_time": None
        }
        
    def setup_logging(self):
        """Setup logging configuration"""
        log_filename = self.log_dir / f"deployment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        
    def create_device_connection(self, device: NetworkDevice) -> Dict[str, Any]:
        """Create Netmiko connection parameters for device"""
        if not NETMIKO_AVAILABLE:
            raise ImportError("Netmiko is required for device connections")
            
        # Map device types to Netmiko device types
        device_type_map = {
            "router": "cisco_ios",
            "switch": "cisco_ios"
        }
        
        if device.device_type not in device_type_map:
            raise ValueError(f"Unsupported device type: {device.device_type}")
            
        connection_params = {
            "device_type": device_type_map[device.device_type],
            "host": device.mgmt_ip,
            "username": device.credentials.get("username", "admin"),
            "password": device.credentials.get("password", "cisco"),
            "secret": device.credentials.get("secret", "cisco"),
            "timeout": 30,
            "session_timeout": 60,
            "auth_timeout": 30,
            "banner_timeout": 15,
            "conn_timeout": 10
        }
        
        return connection_params
        
    def test_connectivity(self, device: NetworkDevice) -> Tuple[bool, str]:
        """Test connectivity to a device"""
        try:
            connection_params = self.create_device_connection(device)
            
            with ConnectHandler(**connection_params) as conn:
                # Send a simple command to test connectivity
                output = conn.send_command("show version", read_timeout=10)
                if "Cisco" in output:
                    return True, "Connection successful"
                else:
                    return False, "Unexpected response from device"
                    
        except NetmikoAuthenticationException:
            return False, "Authentication failed"
        except NetmikoTimeoutException:
            return False, "Connection timeout"
        except Exception as e:
            return False, f"Connection error: {str(e)}"
            
    def backup_device_config(self, device: NetworkDevice) -> Tuple[bool, str, str]:
        """Backup current device configuration"""
        try:
            connection_params = self.create_device_connection(device)
            
            with ConnectHandler(**connection_params) as conn:
                # Get running configuration
                running_config = conn.send_command("show running-config", read_timeout=30)
                
                # Save backup
                backup_filename = self.log_dir / f"{device.hostname}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(backup_filename, 'w') as f:
                    f.write(running_config)
                    
                return True, str(backup_filename), running_config
                
        except Exception as e:
            return False, f"Backup failed: {str(e)}", ""
            
    def deploy_configuration(self, device: NetworkDevice, config: str, 
                           backup_first: bool = True) -> Tuple[bool, str]:
        """Deploy configuration to a device"""
        self.logger.info(f"Starting deployment to {device.hostname}")
        
        try:
            # Test connectivity first
            connected, conn_msg = self.test_connectivity(device)
            if not connected:
                return False, f"Connectivity test failed: {conn_msg}"
                
            # Backup current configuration if requested
            if backup_first:
                backup_success, backup_msg, _ = self.backup_device_config(device)
                if backup_success:
                    self.logger.info(f"Backup created: {backup_msg}")
                else:
                    self.logger.warning(f"Backup failed: {backup_msg}")
                    
            # Deploy configuration
            connection_params = self.create_device_connection(device)
            
            with ConnectHandler(**connection_params) as conn:
                # Enter configuration mode
                conn.enable()
                
                # Send configuration commands
                config_lines = config.split('\n')
                config_commands = [line.strip() for line in config_lines 
                                 if line.strip() and not line.strip().startswith('!')]
                
                # Filter out problematic commands for automated deployment
                filtered_commands = []
                skip_commands = ['end', 'exit', 'write memory', 'copy running-config startup-config']
                
                for cmd in config_commands:
                    if not any(skip_cmd in cmd.lower() for skip_cmd in skip_commands):
                        filtered_commands.append(cmd)
                        
                # Send configuration in batches
                batch_size = 50
                for i in range(0, len(filtered_commands), batch_size):
                    batch = filtered_commands[i:i + batch_size]
                    try:
                        output = conn.send_config_set(batch, read_timeout=30)
                        self.logger.debug(f"Batch {i//batch_size + 1} deployed successfully")
                    except Exception as e:
                        self.logger.error(f"Error in batch {i//batch_size + 1}: {str(e)}")
                        return False, f"Configuration deployment failed at batch {i//batch_size + 1}: {str(e)}"
                        
                # Save configuration
                save_output = conn.send_command("write memory", read_timeout=30)
                
                self.logger.info(f"Configuration deployed successfully to {device.hostname}")
                return True, "Configuration deployed successfully"
                
        except Exception as e:
            error_msg = f"Deployment failed: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg
            
    def deploy_to_multiple_devices(self, devices_configs: Dict[NetworkDevice, str],
                                 max_workers: int = 5, backup_first: bool = True) -> Dict[str, Dict]:
        """Deploy configurations to multiple devices in parallel"""
        self.stats["total_devices"] = len(devices_configs)
        self.stats["start_time"] = datetime.now()
        
        results = {}
        
        def deploy_single_device(device_config_pair):
            device, config = device_config_pair
            success, message = self.deploy_configuration(device, config, backup_first)
            return device.hostname, {"success": success, "message": message, "device": device.hostname}
            
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all deployment tasks
            future_to_device = {
                executor.submit(deploy_single_device, (device, config)): device.hostname
                for device, config in devices_configs.items()
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_device):
                hostname = future_to_device[future]
                try:
                    device_hostname, result = future.result()
                    results[device_hostname] = result
                    
                    if result["success"]:
                        self.stats["successful_deployments"] += 1
                        print(f"✅ {device_hostname}: {result['message']}")
                    else:
                        self.stats["failed_deployments"] += 1
                        print(f"❌ {device_hostname}: {result['message']}")
                        
                except Exception as e:
                    self.stats["failed_deployments"] += 1
                    results[hostname] = {"success": False, "message": f"Deployment exception: {str(e)}", "device": hostname}
                    print(f"❌ {hostname}: Deployment exception: {str(e)}")
                    
        self.stats["end_time"] = datetime.now()
        return results
        
    def validate_deployment(self, device: NetworkDevice, 
                          expected_config_snippets: List[str]) -> Tuple[bool, List[str]]:
        """Validate that configuration was deployed correctly"""
        try:
            connection_params = self.create_device_connection(device)
            
            with ConnectHandler(**connection_params) as conn:
                running_config = conn.send_command("show running-config", read_timeout=30)
                
                missing_snippets = []
                for snippet in expected_config_snippets:
                    if snippet not in running_config:
                        missing_snippets.append(snippet)
                        
                return len(missing_snippets) == 0, missing_snippets
                
        except Exception as e:
            return False, [f"Validation error: {str(e)}"]
            
    def generate_deployment_report(self, results: Dict[str, Dict]) -> str:
        """Generate deployment report"""
        report = f"""# Network Deployment Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Deployment Summary
- **Total Devices:** {self.stats['total_devices']}
- **Successful Deployments:** {self.stats['successful_deployments']}
- **Failed Deployments:** {self.stats['failed_deployments']}
- **Success Rate:** {(self.stats['successful_deployments'] / self.stats['total_devices'] * 100):.1f}%
- **Start Time:** {self.stats['start_time'].strftime('%Y-%m-%d %H:%M:%S')}
- **End Time:** {self.stats['end_time'].strftime('%Y-%m-%d %H:%M:%S')}
- **Duration:** {str(self.stats['end_time'] - self.stats['start_time'])}

## Device Results
"""
        
        for hostname, result in sorted(results.items()):
            status = "✅ SUCCESS" if result["success"] else "❌ FAILED"
            report += f"- **{hostname}:** {status} - {result['message']}\n"
            
        if self.stats['failed_deployments'] > 0:
            report += f"""
## Failed Deployments
The following devices failed deployment and require manual attention:
"""
            for hostname, result in results.items():
                if not result["success"]:
                    report += f"- **{hostname}:** {result['message']}\n"
                    
        report += f"""
## Next Steps
1. Review failed deployments and resolve issues
2. Validate network connectivity and routing
3. Test inter-VLAN communication
4. Verify OSPF neighbor relationships
5. Perform end-to-end connectivity tests

## Log Files
- Deployment logs: {self.log_dir}
- Configuration backups: {self.log_dir}
"""
        
        # Save report
        report_filename = self.log_dir / f"deployment_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_filename, 'w') as f:
            f.write(report)
            
        return report

class SimulatedDeployer(NetworkDeployer):
    """Simulated deployer for testing without real devices"""
    
    def __init__(self, log_dir: str = "logs"):
        super().__init__(log_dir)
        self.logger.info("Using simulated deployment mode")
        
    def test_connectivity(self, device: NetworkDevice) -> Tuple[bool, str]:
        """Simulate connectivity test"""
        time.sleep(0.5)  # Simulate network delay
        return True, "Simulated connection successful"
        
    def backup_device_config(self, device: NetworkDevice) -> Tuple[bool, str, str]:
        """Simulate configuration backup"""
        time.sleep(1)  # Simulate backup time
        backup_filename = self.log_dir / f"{device.hostname}_backup_simulated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Create simulated backup
        simulated_config = f"! Simulated backup for {device.hostname}\n! Generated on {datetime.now()}\n"
        with open(backup_filename, 'w') as f:
            f.write(simulated_config)
            
        return True, str(backup_filename), simulated_config
        
    def deploy_configuration(self, device: NetworkDevice, config: str, 
                           backup_first: bool = True) -> Tuple[bool, str]:
        """Simulate configuration deployment"""
        self.logger.info(f"Simulating deployment to {device.hostname}")
        
        # Simulate deployment time
        time.sleep(2)
        
        # Simulate occasional failures for testing
        import random
        if random.random() < 0.1:  # 10% failure rate for testing
            return False, "Simulated deployment failure"
            
        # Save deployed configuration for reference
        deployed_config_file = self.log_dir / f"{device.hostname}_deployed_config.txt"
        with open(deployed_config_file, 'w') as f:
            f.write(config)
            
        return True, "Simulated deployment successful"

def main():
    """Main function for testing deployment"""
    from inventory.network_inventory import create_task2_inventory
    
    print("🚀 Advanced Network Deployment Engine")
    print("=" * 50)
    
    # Create inventory and generate configurations
    print("📋 Loading network inventory...")
    inventory = create_task2_inventory()
    
    print("🔧 Generating configurations...")
    generator = ConfigurationGenerator()
    configs = generator.generate_all_configs(inventory, save_to_files=False)
    
    # Create deployer (simulated for testing)
    print("🌐 Initializing deployment engine...")
    deployer = SimulatedDeployer()
    
    # Prepare device-config pairs for deployment
    devices_configs = {}
    for hostname, config in configs.items():
        device = inventory.get_device(hostname)
        devices_configs[device] = config
        
    # Deploy configurations
    print(f"🚀 Deploying to {len(devices_configs)} devices...")
    results = deployer.deploy_to_multiple_devices(devices_configs, max_workers=3)
    
    # Generate report
    print("📊 Generating deployment report...")
    report = deployer.generate_deployment_report(results)
    
    print(f"\n🎉 Deployment complete!")
    print(f"✅ Successful: {deployer.stats['successful_deployments']}")
    print(f"❌ Failed: {deployer.stats['failed_deployments']}")
    print(f"📁 Logs: {deployer.log_dir}")
    
if __name__ == "__main__":
    main()

