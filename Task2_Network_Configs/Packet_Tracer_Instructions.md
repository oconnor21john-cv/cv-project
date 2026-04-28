# 🌐 Packet Tracer Setup Instructions - Task 2 Network

**Complete step-by-step guide to build your Task 2 network in Cisco Packet Tracer**

---

## 📋 Overview

You'll be creating a network with:
- **4 Routers** (R1, R2, R3, R4) in full mesh topology
- **4 Switches** (SW1, SW2, SW3, SW4)
- **8 PCs** (2 per switch)
- **OSPF routing** for dynamic routing
- **VLANs** for network segmentation

---

## 🔧 Step 1: Add Devices to Workspace

### Routers
1. **Drag 4 x Cisco 2901 Routers** from Network Devices > Routers
2. **Label them:** R1, R2, R3, R4
3. **Arrange** in a square formation for easy cabling

### Switches  
1. **Drag 4 x Cisco 2960 Switches** from Network Devices > Switches
2. **Label them:** SW1, SW2, SW3, SW4
3. **Place** each switch below its corresponding router

### PCs
1. **Drag 8 x Generic PCs** from End Devices > End Devices
2. **Label them:** PC1, PC2, PC3, PC4, PC5, PC6, PC7, PC8
3. **Place** 2 PCs below each switch

---

## 🔌 Step 2: Physical Connections

**Use Copper Straight-Through cables for all connections**

### Router-to-Router Links (Full Mesh):
```
R1 G0/0 ↔ R2 G0/0  (10.1.12.0/30 network)
R1 G0/1 ↔ R3 G0/0  (10.1.13.0/30 network)
R2 G0/1 ↔ R4 G0/0  (10.2.24.0/30 network)
R3 G0/1 ↔ R4 G0/1  (10.3.34.0/30 network)
```

### Router-to-Switch Links:
```
R1 G0/2 ↔ SW1 G0/1
R2 G0/2 ↔ SW2 G0/1
R3 G0/2 ↔ SW3 G0/1
R4 G0/2 ↔ SW4 G0/1
```

### Switch-to-PC Links:
```
SW1: F0/1 ↔ PC1, F0/2 ↔ PC2
SW2: F0/1 ↔ PC3, F0/2 ↔ PC4
SW3: F0/1 ↔ PC5, F0/2 ↔ PC6
SW4: F0/1 ↔ PC7, F0/2 ↔ PC8
```

---

## ⚙️ Step 3: Configure Devices

### Router Configuration

**For each router (R1, R2, R3, R4):**

1. **Click on the router**
2. **Go to CLI tab**
3. **Press Enter** to get to the prompt
4. **Copy the entire configuration** from the corresponding config file:
   - `R1_config.txt` → R1
   - `R2_config.txt` → R2
   - `R3_config.txt` → R3
   - `R4_config.txt` → R4
5. **Paste into CLI** and press Enter
6. **Wait for configuration** to apply

### Switch Configuration

**For each switch (SW1, SW2, SW3, SW4):**

1. **Click on the switch**
2. **Go to CLI tab**
3. **Press Enter** to get to the prompt
4. **Copy the entire configuration** from the corresponding config file:
   - `SW1_config.txt` → SW1
   - `SW2_config.txt` → SW2
   - `SW3_config.txt` → SW3
   - `SW4_config.txt` → SW4
5. **Paste into CLI** and press Enter
6. **Wait for configuration** to apply

### PC Configuration

**For each PC:**

1. **Click on the PC**
2. **Go to Desktop tab**
3. **Click IP Configuration**
4. **Select Static**
5. **Enter the IP settings** from `PC_configs.txt`:

| PC | IP Address | Subnet Mask | Default Gateway |
|----|------------|-------------|-----------------|
| PC1 | 192.168.10.100 | 255.255.255.0 | 192.168.10.1 |
| PC2 | 192.168.10.101 | 255.255.255.0 | 192.168.10.1 |
| PC3 | 192.168.20.100 | 255.255.255.0 | 192.168.20.1 |
| PC4 | 192.168.20.101 | 255.255.255.0 | 192.168.20.1 |
| PC5 | 192.168.30.100 | 255.255.255.0 | 192.168.30.1 |
| PC6 | 192.168.30.101 | 255.255.255.0 | 192.168.30.1 |
| PC7 | 192.168.40.100 | 255.255.255.0 | 192.168.40.1 |
| PC8 | 192.168.40.101 | 255.255.255.0 | 192.168.40.1 |

---

## ✅ Step 4: Verification Commands

### On Routers - Check OSPF:
```cisco
show ip route
show ip ospf neighbor
show ip interface brief
```

**Expected Results:**
- All OSPF neighbors should show **FULL** state
- Routing table should show all networks
- All interfaces should be **up/up**

### On Switches - Check VLANs:
```cisco
show vlan brief
show interface trunk
show mac address-table
```

**Expected Results:**
- VLANs 10, 20, 30, 40, 99 should be active
- Trunk ports should show allowed VLANs
- MAC addresses should be learned

### On PCs - Test Connectivity:
```
ipconfig
ping [gateway_ip]
ping [remote_pc_ip]
```

---

## 🧪 Step 5: Testing Scenarios

### Test 1: Local Connectivity
```
PC1 → ping 192.168.10.1 (Gateway)
PC3 → ping 192.168.20.1 (Gateway)
```
**Should succeed** ✅

### Test 2: Inter-VLAN Routing
```
PC1 → ping 192.168.20.100 (PC3)
PC5 → ping 192.168.40.100 (PC7)
```
**Should succeed** ✅

### Test 3: OSPF Convergence
1. **Shutdown** R1-R2 link: `R1(config-if)# shutdown`
2. **Check routing table:** `show ip route`
3. **Test connectivity** - should still work via alternate paths
4. **Bring link back up:** `R1(config-if)# no shutdown`

### Test 4: End-to-End Connectivity
```
PC1 → ping 192.168.40.101 (PC8)
PC2 → ping 192.168.30.100 (PC5)
```
**Should succeed** ✅

---

## 🎯 Expected Network Behavior

### ✅ Success Indicators:
- **All router interfaces up/up**
- **OSPF neighbors in FULL state**
- **All PCs can ping their gateways**
- **Inter-VLAN communication works**
- **Network has redundant paths**
- **VLANs properly segmented**

### ❌ Troubleshooting Common Issues:

**OSPF neighbors not forming:**
- Check interface IP addresses
- Verify network statements in OSPF
- Ensure no shutdown on interfaces

**PCs can't reach gateway:**
- Verify PC IP configuration
- Check VLAN assignments on switch ports
- Verify trunk configuration

**Inter-VLAN routing not working:**
- Check router interface IPs
- Verify OSPF is advertising all networks
- Test with traceroute to see path

---

## 🏆 Completion Checklist

- [ ] All devices powered on and configured
- [ ] All cables connected properly
- [ ] OSPF neighbors established (show ip ospf neighbor)
- [ ] All networks in routing table (show ip route)
- [ ] VLANs created and assigned (show vlan brief)
- [ ] PCs configured with correct IPs
- [ ] Local connectivity working (ping gateways)
- [ ] Inter-VLAN routing working (ping remote PCs)
- [ ] Redundant paths available
- [ ] Network documentation complete

---

## 🎉 Congratulations!

You've successfully built a complete enterprise network with:
- **Full mesh router topology**
- **OSPF dynamic routing**
- **VLAN segmentation**
- **Inter-VLAN routing**
- **Redundant paths**
- **Security features**

**Your Task 2 network is now fully operational!** 🌐✨
