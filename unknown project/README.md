# 🌐 Task 2 Network Automation Generator

**Automatically creates complete Cisco Packet Tracer network configurations for Task 2!**

## 🚀 Quick Start

### Option 1: Windows (Easiest)
1. **Double-click** `Generate_Task2_Network.bat`
2. **Wait** for files to generate
3. **Open** the `Task2_Network_Configs` folder
4. **Follow** the Packet Tracer instructions

### Option 2: Python (Any OS)
1. **Run:** `python run_task2_generator.py`
2. **Check** the `Task2_Network_Configs` folder
3. **Follow** the setup instructions

### Option 3: Direct Python
```bash
python task2_network_generator.py
```

## 📋 What You Get

After running the generator, you'll have:

```
Task2_Network_Configs/
├── R1_config.txt                    # Router 1 configuration
├── R2_config.txt                    # Router 2 configuration  
├── R3_config.txt                    # Router 3 configuration
├── R4_config.txt                    # Router 4 configuration
├── SW1_config.txt                   # Switch 1 configuration
├── SW2_config.txt                   # Switch 2 configuration
├── SW3_config.txt                   # Switch 3 configuration
├── SW4_config.txt                   # Switch 4 configuration
├── PC_configs.txt                   # All PC IP configurations
├── Packet_Tracer_Instructions.md   # Step-by-step setup guide
├── Network_Documentation.md         # Complete network documentation
└── network_topology.json           # Network topology reference
```

## 🔧 Network Specifications

### 🌐 Topology
- **4 Routers** in full mesh topology (R1, R2, R3, R4)
- **4 Switches** (SW1, SW2, SW3, SW4) 
- **8 PCs** (2 per switch)
- **OSPF routing** for dynamic routing
- **VLANs** for network segmentation

### 📡 IP Addressing
- **Router Links:** 10.x.x.x/30 networks
- **LAN Networks:** 192.168.x.0/24 networks
- **VLANs:** 10, 20, 30, 40 (Sales, Marketing, IT, Finance)

### 🔒 Security Features
- Port security on switches
- Password protection
- Management VLANs
- Access control

## 📖 How to Use in Packet Tracer

### Step 1: Create Physical Topology
1. **Add devices:** 4 routers, 4 switches, 8 PCs
2. **Connect cables** as shown in instructions
3. **Power on** all devices

### Step 2: Apply Configurations
1. **Copy** router configs from `.txt` files
2. **Paste** into router CLI (Global Config mode)
3. **Repeat** for all switches
4. **Configure** PC IP addresses

### Step 3: Verify Network
1. **Check OSPF:** `show ip ospf neighbor`
2. **Test connectivity:** `ping` between devices
3. **Verify VLANs:** `show vlan brief`

## 🎯 Expected Results

✅ **All OSPF neighbors in FULL state**  
✅ **Inter-VLAN routing working**  
✅ **End-to-end connectivity**  
✅ **Redundant paths available**  
✅ **Security features active**  

## 🛠️ Requirements

- **Python 3.6+** (for running the generator)
- **Cisco Packet Tracer** (for building the network)
- **Windows/Mac/Linux** (any OS works)

## 🆘 Troubleshooting

### "Python not found"
- Install Python from python.org
- Make sure Python is in your PATH

### "Files not generating"
- Check you have write permissions
- Run as administrator if needed

### "Network not working in Packet Tracer"
- Verify all cables are connected
- Check device power status
- Ensure configs were pasted correctly

## 📚 Learning Outcomes

After completing this network, you'll understand:
- **OSPF routing protocol**
- **VLAN configuration**
- **Inter-VLAN routing**
- **Network redundancy**
- **Switch port security**
- **Network documentation**

## 🎉 Success!

Your Task 2 network is now ready! This automated approach saves hours of manual configuration and ensures consistency across all devices.

**Happy networking!** 🌐✨
