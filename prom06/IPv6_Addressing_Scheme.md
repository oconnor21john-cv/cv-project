# IPv6 Addressing Scheme for Multi-Area Network

## Overview
This document provides a complete IPv6 addressing scheme for the three-area network topology using Global Unicast Addresses (GUA).

**Base Prefix**: `2001:db8::/32` (Documentation prefix, replace with actual allocation in production)

---

## **Area 1: Class B Network - 2001:db8:1000::/36**

### ISP Connection
- **ISP G1/1/1 ↔ R1 G0/0**: `2001:db8:1000::/127`
  - ISP Interface: `2001:db8:1000::1/127`
  - R1 G0/0: `2001:db8:1000::0/127`

### R1 to Switches
- **R1 G0/1 → S1**: `2001:db8:1000:1::/64`
  - R1 G0/1: `2001:db8:1000:1::1/64` (Gateway)
  
- **R1 G0/2 → S2**: `2001:db8:1000:2::/64`
  - R1 G0/2: `2001:db8:1000:2::1/64` (Gateway)

### S1 Branch

#### S1 to R2
- **S1 ↔ R2 G0/0**: Same VLAN as S1
  - R2 G0/0: `2001:db8:1000:1::2/64`
  
- **R2 G0/1 → Server**: `2001:db8:1000:10::/127`
  - R2 G0/1: `2001:db8:1000:10::0/127`
  - Server: `2001:db8:1000:10::1/127`

#### S1 to R3
- **S1 ↔ R3 G0/0**: Same VLAN as S1
  - R3 G0/0: `2001:db8:1000:1::3/64`
  
- **R3 G0/1 → S3a**: `2001:db8:1000:3::/64`
  - R3 G0/1: `2001:db8:1000:3::1/64` (Gateway)
  - S3a Management: `2001:db8:1000:3::2/64`

#### S3a VLANs (connected to R3)
- **VLAN 2 - 400 hosts**: `2001:db8:1000:20::/64`
  - Gateway (S3a): `2001:db8:1000:20::1/64`
  - Hosts: `2001:db8:1000:20::2` - `2001:db8:1000:20::191` (400 addresses)

- **VLAN 3 - 250 hosts**: `2001:db8:1000:22::/64`
  - Gateway (S3a): `2001:db8:1000:22::1/64`
  - Hosts: `2001:db8:1000:22::2` - `2001:db8:1000:22::fb` (250 addresses)

### S2 Branch

#### S2 to R4
- **S2 ↔ R4 G0/0**: Same VLAN as S2
  - R4 G0/0: `2001:db8:1000:2::2/64`
  
- **R4 G0/1 → Server**: `2001:db8:1000:11::/127`
  - R4 G0/1: `2001:db8:1000:11::0/127`
  - Server: `2001:db8:1000:11::1/127`

#### S2 to R5
- **S2 ↔ R5 G0/0**: Same VLAN as S2
  - R5 G0/0: `2001:db8:1000:2::3/64`
  
- **R5 G0/1 → R6 G0/0**: `2001:db8:1000:12::/127`
  - R5 G0/1: `2001:db8:1000:12::0/127`
  - R6 G0/0: `2001:db8:1000:12::1/127`

#### R6 to S3b (Trunk for VLANs 4 & 5)
- **R6 G0/1 → S3b**: `2001:db8:1000:4::/64`
  - R6 Management VLAN: `2001:db8:1000:4::1/64`
  - S3b Management: `2001:db8:1000:4::2/64`

#### S3b VLANs (connected to R6 trunk)
- **VLAN 4 - 1024 hosts**: `2001:db8:1000:24::/64`
  - Gateway (S3b): `2001:db8:1000:24::1/64`
  - Hosts: `2001:db8:1000:24::2` - `2001:db8:1000:24::401` (1024 addresses)

- **VLAN 5 - 505 hosts**: `2001:db8:1000:28::/64`
  - Gateway (S3b): `2001:db8:1000:28::1/64`
  - Hosts: `2001:db8:1000:28::2` - `2001:db8:1000:28::1fa` (505 addresses)

---

## **Area 2: Class C Network - 2001:db8:2000::/36**

### ISP Connection
- **ISP G1/1/3 ↔ R7 G0/1**: `2001:db8:2000::/127`
  - ISP Interface: `2001:db8:2000::1/127`
  - R7 G0/1: `2001:db8:2000::0/127`

### R7 to L3-3
- **R7 G0/0 → L3-3**: Connected via VLAN 400

### L3-3 VLANs

- **VLAN 400 - 18 hosts**: `2001:db8:2000:400::/64`
  - Gateway (L3-3): `2001:db8:2000:400::1/64`
  - R7 G0/0: `2001:db8:2000:400::2/64`
  - Hosts: `2001:db8:2000:400::3` - `2001:db8:2000:400::14` (18 addresses)

- **VLAN 300 - 5 hosts**: `2001:db8:2000:300::/64`
  - Gateway (L3-3): `2001:db8:2000:300::1/64`
  - R10 G0/0: `2001:db8:2000:300::2/64`
  - Hosts: `2001:db8:2000:300::3` - `2001:db8:2000:300::7` (5 addresses)

- **VLAN 1 - 2 hosts**: `2001:db8:2000:1::/127`
  - L3-3 Interface: `2001:db8:2000:1::0/127`
  - L3-2 Interface: `2001:db8:2000:1::1/127`

### R10 Branch
- **R10 G0/1 → S6**: `2001:db8:2000:10::/64`
  - Gateway (R10 G0/1): `2001:db8:2000:10::1/64`
  - Hosts: `2001:db8:2000:10::2` - `2001:db8:2000:10::1a` (25 addresses)

### L3-2 VLANs

- **VLAN 200 - 12 hosts**: `2001:db8:2000:200::/64`
  - Gateway (L3-2): `2001:db8:2000:200::1/64`
  - R9 G0/0: `2001:db8:2000:200::2/64`
  - Hosts: `2001:db8:2000:200::3` - `2001:db8:2000:200::e` (12 addresses)

- **VLAN 100 - 8 hosts**: `2001:db8:2000:100::/64`
  - Gateway (L3-2): `2001:db8:2000:100::1/64`
  - R8 G0/0: `2001:db8:2000:100::2/64`
  - Hosts: `2001:db8:2000:100::3` - `2001:db8:2000:100::a` (8 addresses)

### R9 Branch
- **R9 G0/1 → S5**: `2001:db8:2000:11::/64`
  - Gateway (R9 G0/1): `2001:db8:2000:11::1/64`
  - Hosts: `2001:db8:2000:11::2` - `2001:db8:2000:11::3d` (60 addresses)

### R8 Branch
- **R8 G0/1 → S4**: `2001:db8:2000:12::/64`
  - Gateway (R8 G0/1): `2001:db8:2000:12::1/64`
  - Hosts: `2001:db8:2000:12::2` - `2001:db8:2000:12::f` (14 addresses)

---

## **Area 3: Class A Network - 2001:db8:3000::/36**

### ISP Connection
- **ISP G1/1/2 ↔ R11 G0/0**: `2001:db8:3000::/127`
  - ISP Interface: `2001:db8:3000::1/127`
  - R11 G0/0: `2001:db8:3000::0/127`

### R11 Connections

#### R11 to S7 (Trunk)
- **R11 G0/1 → S7 G0/1**: Trunk carrying VLANs 6 & 7

#### S7 VLANs
- **VLAN 6 - 202,000 hosts**: `2001:db8:3000:6::/48`
  - Gateway (S7): `2001:db8:3000:6::1/48`
  - Hosts: `2001:db8:3000:6::2` onwards
  - Range: `2001:db8:3000:6:0:0:0:2` - `2001:db8:3000:6:ffff:ffff:ffff:fffe`

- **VLAN 7 - 2,000 hosts**: `2001:db8:3000:7::/64`
  - Gateway (S7): `2001:db8:3000:7::1/64`
  - Hosts: `2001:db8:3000:7::2` - `2001:db8:3000:7::7d1` (2000 addresses)

#### R11 to L3-1
- **R11 G0/2 → L3-1**: Connected via VLAN 500

### L3-1 VLANs

- **VLAN 500 - 20 hosts**: `2001:db8:3000:500::/64`
  - Gateway (L3-1): `2001:db8:3000:500::1/64`
  - R11 G0/2: `2001:db8:3000:500::2/64`
  - Hosts: `2001:db8:3000:500::3` - `2001:db8:3000:500::16` (20 addresses)

- **VLAN 700 - 80 hosts**: `2001:db8:3000:700::/64`
  - Gateway (L3-1): `2001:db8:3000:700::1/64`
  - R12 G0/0: `2001:db8:3000:700::2/64`
  - Hosts: `2001:db8:3000:700::3` - `2001:db8:3000:700::52` (80 addresses)

- **VLAN 600 - 40 hosts**: `2001:db8:3000:600::/64`
  - Gateway (L3-1): `2001:db8:3000:600::1/64`
  - R13 G0/0: `2001:db8:3000:600::2/64`
  - Hosts: `2001:db8:3000:600::3` - `2001:db8:3000:600::2a` (40 addresses)

### R12 to S8 (Trunk)
- **R12 G0/1 → S8 G0/1**: Trunk carrying VLANs 8 & 9

#### S8 VLANs
- **VLAN 8 - 200,000 hosts**: `2001:db8:3000:8::/48`
  - Gateway (S8): `2001:db8:3000:8::1/48`
  - Hosts: `2001:db8:3000:8::2` onwards
  - Range: `2001:db8:3000:8:0:0:0:2` - `2001:db8:3000:8:ffff:ffff:ffff:fffe`

- **VLAN 9 - 10,000 hosts**: `2001:db8:3000:9::/64`
  - Gateway (S8): `2001:db8:3000:9::1/64`
  - Hosts: `2001:db8:3000:9::2` - `2001:db8:3000:9::2711` (10000 addresses)

### R13 to S9 (Trunk)
- **R13 G0/1 → S9 G0/1**: Trunk carrying VLANs 10 & 11

#### S9 VLANs
- **VLAN 10 - 5,000,000 hosts**: `2001:db8:3000:a::/40`
  - Gateway (S9): `2001:db8:3000:a::1/40`
  - Hosts: `2001:db8:3000:a::2` onwards
  - Range: `2001:db8:3000:a:0:0:0:2` - `2001:db8:3000:a:ff:ffff:ffff:fffe`

- **VLAN 11 - 5,000 hosts**: `2001:db8:3000:b::/64`
  - Gateway (S9): `2001:db8:3000:b::1/64`
  - Hosts: `2001:db8:3000:b::2` - `2001:db8:3000:b::1389` (5000 addresses)

---

## **ISP Router Summary**

- **G1/1/1** (to Area 1 - R1): `2001:db8:1000::1/127`
- **G1/1/3** (to Area 2 - R7): `2001:db8:2000::1/127`
- **G1/1/2** (to Area 3 - R11): `2001:db8:3000::1/127`
- **Public IPv6 Pool**: Can use global unicast addresses as needed

---

## **IPv6 Addressing Best Practices Used**

### 1. **Hierarchical Structure**
- Area 1: `2001:db8:1000::/36`
- Area 2: `2001:db8:2000::/36`
- Area 3: `2001:db8:3000::/36`

### 2. **Consistent Subnetting**
- Point-to-point links: `/127` (RFC 6164)
- Transit networks: `/64`
- Host networks: `/64` (standard)
- Large networks: `/48` or `/40` for massive host counts

### 3. **Simplified Addressing**
- Gateways always use `::1` in their subnet
- Routers use sequential numbers (`::2`, `::3`, etc.)
- Easy to remember and troubleshoot

### 4. **VLAN ID Mapping**
- VLAN numbers incorporated into IPv6 addresses where logical
- Example: VLAN 400 → `2001:db8:2000:400::/64`

### 5. **Scalability**
- Each `/64` subnet provides 18,446,744,073,709,551,616 addresses
- Sufficient for any growth in host count
- Simplified address assignment with SLAAC capability

---

## **Summary Statistics**

### Area 1 (2001:db8:1000::/36)
- Total subnets: 12
- Address space: Sufficient for 2,200+ hosts
- Point-to-point links: 4 × /127
- Host networks: 8 × /64
- Switches: S1, S2, S3a, S3b

### Area 2 (2001:db8:2000::/36)
- Total subnets: 9
- Address space: Sufficient for 126+ hosts
- Point-to-point links: 2 × /127
- Host networks: 7 × /64

### Area 3 (2001:db8:3000::/36)
- Total subnets: 10
- Address space: Sufficient for 5,417,120+ hosts
- Point-to-point links: 1 × /127
- Large networks: 3 × /48 or /40
- Standard networks: 6 × /64

### Total Network
- **Total subnets**: 31
- **Addressing philosophy**: Hierarchical and scalable
- **Future-proof**: Massive address space available
- **Standards compliant**: RFC 6164 for point-to-point links

---

## **Additional IPv6 Features**

### Link-Local Addresses
All interfaces also have link-local addresses (fe80::/10) for:
- Neighbor discovery
- Router advertisements
- Local network communication

### Address Configuration Methods
1. **Static Assignment**: For infrastructure (routers, gateways)
2. **SLAAC**: For end hosts (Stateless Address Autoconfiguration)
3. **DHCPv6**: For controlled assignment with additional options

### Security Considerations
- IPsec built into IPv6
- No NAT required (true end-to-end connectivity)
- Privacy extensions available for client devices (RFC 4941)
