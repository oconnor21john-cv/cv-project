#!/usr/bin/env python3
"""
Packet Tracer Configuration Helper
Helps organize and display configurations for easy copy-paste into Packet Tracer
"""

import os
import sys
from pathlib import Path

class PacketTracerConfigHelper:
    def __init__(self, config_dir):
        self.config_dir = Path(config_dir)
        if not self.config_dir.exists():
            raise FileNotFoundError(f"Configuration directory not found: {config_dir}")
    
    def list_devices(self):
        """List all available device configurations"""
        configs = sorted(self.config_dir.glob("*_config.txt"))
        
        print("\n" + "="*70)
        print("AVAILABLE DEVICE CONFIGURATIONS")
        print("="*70)
        
        routers = [c for c in configs if c.stem.startswith('R')]
        switches = [c for c in configs if c.stem.startswith('SW')]
        
        print(f"\n📡 ROUTERS ({len(routers)}):")
        for i, config in enumerate(routers, 1):
            device_name = config.stem.replace('_config', '')
            print(f"   {i:2d}. {device_name}")
        
        print(f"\n🔌 SWITCHES ({len(switches)}):")
        for i, config in enumerate(switches, 1):
            device_name = config.stem.replace('_config', '')
            print(f"   {i:2d}. {device_name}")
        
        print("\n" + "="*70)
    
    def display_config(self, device_name):
        """Display configuration for a specific device"""
        config_file = self.config_dir / f"{device_name}_config.txt"
        
        if not config_file.exists():
            print(f"❌ Configuration not found for device: {device_name}")
            return False
        
        with open(config_file, 'r') as f:
            config = f.read()
        
        print("\n" + "="*70)
        print(f"CONFIGURATION FOR: {device_name}")
        print("="*70)
        print("\n📋 INSTRUCTIONS:")
        print("   1. In Packet Tracer, click on the device")
        print("   2. Go to the CLI tab")
        print("   3. Press Enter to get to the prompt")
        print("   4. Copy the configuration below")
        print("   5. Paste it into the CLI")
        print("   6. Wait for the configuration to apply")
        print("\n" + "-"*70)
        print("CONFIGURATION START")
        print("-"*70 + "\n")
        
        print(config)
        
        print("\n" + "-"*70)
        print("CONFIGURATION END")
        print("-"*70)
        print(f"\n✅ Configuration for {device_name} displayed successfully!")
        print("   Copy the text between 'CONFIGURATION START' and 'CONFIGURATION END'\n")
        
        return True
    
    def create_batch_file(self):
        """Create a checklist file for tracking configuration progress"""
        configs = sorted(self.config_dir.glob("*_config.txt"))
        checklist_file = self.config_dir / "CONFIGURATION_CHECKLIST.txt"
        
        with open(checklist_file, 'w') as f:
            f.write("="*70 + "\n")
            f.write("PACKET TRACER CONFIGURATION CHECKLIST\n")
            f.write("="*70 + "\n\n")
            f.write("Mark each device as you configure it:\n")
            f.write("[ ] = Not configured\n")
            f.write("[X] = Configured\n\n")
            
            f.write("-"*70 + "\n")
            f.write("ROUTERS:\n")
            f.write("-"*70 + "\n")
            for config in configs:
                if config.stem.startswith('R'):
                    device_name = config.stem.replace('_config', '')
                    f.write(f"[ ] {device_name}\n")
            
            f.write("\n" + "-"*70 + "\n")
            f.write("SWITCHES:\n")
            f.write("-"*70 + "\n")
            for config in configs:
                if config.stem.startswith('SW'):
                    device_name = config.stem.replace('_config', '')
                    f.write(f"[ ] {device_name}\n")
            
            f.write("\n" + "="*70 + "\n")
            f.write("VERIFICATION STEPS:\n")
            f.write("="*70 + "\n")
            f.write("[ ] All devices configured\n")
            f.write("[ ] All physical connections made\n")
            f.write("[ ] OSPF neighbors established (show ip ospf neighbor)\n")
            f.write("[ ] All routes learned (show ip route ospf)\n")
            f.write("[ ] DHCP working (test with PCs)\n")
            f.write("[ ] Inter-VLAN routing working\n")
            f.write("[ ] WAN link R2-R5 operational\n")
            f.write("[ ] All interfaces up (show ip interface brief)\n")
        
        print(f"\n✅ Checklist created: {checklist_file}")
        return checklist_file
    
    def interactive_mode(self):
        """Interactive mode for easy configuration"""
        while True:
            print("\n" + "="*70)
            print("PACKET TRACER CONFIGURATION HELPER - INTERACTIVE MODE")
            print("="*70)
            print("\nOptions:")
            print("  1. List all devices")
            print("  2. Display configuration for a device")
            print("  3. Create configuration checklist")
            print("  4. Show setup instructions")
            print("  5. Exit")
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                self.list_devices()
            
            elif choice == '2':
                device_name = input("\nEnter device name (e.g., R1, SW2): ").strip().upper()
                self.display_config(device_name)
                input("\nPress Enter to continue...")
            
            elif choice == '3':
                self.create_batch_file()
                input("\nPress Enter to continue...")
            
            elif choice == '4':
                instructions_file = self.config_dir / "Enhanced_Packet_Tracer_Instructions_v2.md"
                if instructions_file.exists():
                    print(f"\n📖 Setup instructions available at:")
                    print(f"   {instructions_file}")
                    print("\nOpen this file in a text editor for detailed setup steps.")
                else:
                    print("\n❌ Instructions file not found")
                input("\nPress Enter to continue...")
            
            elif choice == '5':
                print("\n👋 Goodbye!")
                break
            
            else:
                print("\n❌ Invalid choice. Please try again.")

def main():
    """Main function"""
    print("\n" + "="*70)
    print("PACKET TRACER CONFIGURATION HELPER")
    print("="*70)
    
    # Check for available configuration directories
    possible_dirs = [
        "Enhanced_Task2_Network_Configs_v2",
        "Enhanced_Task2_Network_Configs",
        "Task2_Network_Configs"
    ]
    
    config_dir = None
    for dir_name in possible_dirs:
        if os.path.exists(dir_name):
            config_dir = dir_name
            break
    
    if not config_dir:
        print("\n❌ No configuration directory found!")
        print("\nPlease run the network generator first:")
        print("   python enhanced_task2_network_generator_v2.py")
        sys.exit(1)
    
    print(f"\n✅ Using configuration directory: {config_dir}")
    
    helper = PacketTracerConfigHelper(config_dir)
    
    # Check if device name was provided as argument
    if len(sys.argv) > 1:
        device_name = sys.argv[1].upper()
        helper.display_config(device_name)
    else:
        # Interactive mode
        helper.interactive_mode()

if __name__ == "__main__":
    main()

