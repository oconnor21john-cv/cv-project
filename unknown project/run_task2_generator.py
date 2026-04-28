#!/usr/bin/env python3
"""
Simple runner script for Task 2 Network Generator
Just run this file to create all your Packet Tracer configurations!
"""

import sys
import os

# Add current directory to path so we can import our generator
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from task2_network_generator import Task2NetworkGenerator
    
    print("🚀 Starting Task 2 Network Generation...")
    print("⏳ This will take a few seconds...")
    
    # Create the generator and run it
    generator = Task2NetworkGenerator()
    output_dir = generator.generate_all_configs()
    
    print(f"\n✨ SUCCESS! Your network files are ready!")
    print(f"📂 Check the '{output_dir}' folder for all your files.")
    
    # Show what was created
    print(f"\n📋 What you got:")
    print(f"   🔧 Router configs: R1_config.txt, R2_config.txt, R3_config.txt, R4_config.txt")
    print(f"   🔧 Switch configs: SW1_config.txt, SW2_config.txt, SW3_config.txt, SW4_config.txt")
    print(f"   💻 PC configs: PC_configs.txt")
    print(f"   📚 Documentation: Network_Documentation.md")
    print(f"   📖 Instructions: Packet_Tracer_Instructions.md")
    
    print(f"\n🎯 Ready to build your network in Packet Tracer!")
    
except ImportError as e:
    print(f"❌ Error: Could not import the network generator.")
    print(f"   Make sure 'task2_network_generator.py' is in the same folder.")
    print(f"   Error details: {e}")
except Exception as e:
    print(f"❌ Error generating network: {e}")
    print(f"   Please check the error and try again.")

input("\n🎉 Press Enter to close...")
