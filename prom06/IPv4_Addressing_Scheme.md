# IPv4 Addressing Scheme for Multi-Area Network

## Overview
This document provides a complete IPv4 addressing scheme for the three-area network topology.

---

## **Area 1: Class B Network - 172.16.0.0/16**

### ISP Connection
- **ISP G1/1/1 ↔ R1 G0/0**: `172.16.0.0/30`
  - ISP Interface: `172.16.0.1/30`
  - R1 G0/0: `172.16.0.2/30`

### R1 to Switches
- **R1 G0/1 → S1**: `172.16.1.1/24` (R1 interface as gateway)
- **R1 G0/2 → S2**: `172.16.2.1/24` (R1 interface as gateway)

### S1 Branch

#### S1 to R2
- **S1 ↔ R2 G0/0**: VLAN on S1
  - R2 G0/0: `172.16.1.2/24`
  - **R2 G0/1 → Server**: `172.16.10.0/30`
    - R2 G0/1: `172.16.10.1/30`
    - Server: `172.16.10.2/30`

#### S1 to R3
- **S1 ↔ R3 G0/0**: VLAN on S1
  - R3 G0/0: `172.16.1.3/24`
  - **R3 G0/1 → S3a**: `172.16.3.0/24`
    - R3 G0/1: `172.16.3.1/24` (Gateway)
    - S3a Management: `172.16.3.2/24`

#### S3a VLANs (connected to R3)
- **VLAN 2 - 400 hosts**: `172.16.20.0/23` (512 addresses)
  - Network: `172.16.20.0/23`
  - Gateway (S3a): `172.16.20.1/23`
  - Usable: `172.16.20.2` - `172.16.21.254`
  - Broadcast: `172.16.21.255`

- **VLAN 3 - 250 hosts**: `172.16.22.0/24` (256 addresses)
  - Network: `172.16.22.0/24`
  - Gateway (S3a): `172.16.22.1/24`
  - Usable: `172.16.22.2` - `172.16.22.254`
  - Broadcast: `172.16.22.255`

### S2 Branch

#### S2 to R4
- **S2 ↔ R4 G0/0**: VLAN on S2
  - R4 G0/0: `172.16.2.2/24`
  - **R4 G0/1 → Server**: `172.16.11.0/30`
    - R4 G0/1: `172.16.11.1/30`
    - Server: `172.16.11.2/30`

#### S2 to R5
- **S2 ↔ R5 G0/0**: VLAN on S2
  - R5 G0/0: `172.16.2.3/24`
  - **R5 G0/1 → R6 G0/0**: `172.16.12.0/30`
    - R5 G0/1: `172.16.12.1/30`
    - R6 G0/0: `172.16.12.2/30`

#### R6 to S3b (Trunk for VLANs 4 & 5)
- **R6 G0/1 → S3b (trunk)**: `172.16.4.0/24`
  - R6 Management VLAN: `172.16.4.1/24`
  - S3b Management: `172.16.4.2/24`

#### S3b VLANs (connected to R6 trunk)
- **VLAN 4 - 1024 hosts**: `172.16.24.0/22` (1024 addresses)
  - Network: `172.16.24.0/22`
  - Gateway (S3b): `172.16.24.1/22`
  - Usable: `172.16.24.2` - `172.16.27.254`
  - Broadcast: `172.16.27.255`

- **VLAN 5 - 505 hosts**: `172.16.28.0/23` (512 addresses)
  - Network: `172.16.28.0/23`
  - Gateway (S3b): `172.16.28.1/23`
  - Usable: `172.16.28.2` - `172.16.29.254`
  - Broadcast: `172.16.29.255`

---

## **Area 2: Class C Network - 192.168.0.0/16**

### ISP Connection
- **ISP G1/1/3 ↔ R7 G0/1**: `192.168.0.0/30`
  - ISP Interface: `192.168.0.1/30`
  - R7 G0/1: `192.168.0.2/30`

### R7 to L3-3
- **R7 G0/0 → L3-3**: Connected via VLAN 400

### L3-3 VLANs

- **VLAN 400 - 18 hosts**: `192.168.1.0/27` (32 addresses)
  - Network: `192.168.1.0/27`
  - Gateway (L3-3): `192.168.1.1/27`
  - R7 G0/0: `192.168.1.2/27`
  - Usable: `192.168.1.3` - `192.168.1.30`
  - Broadcast: `192.168.1.31`

- **VLAN 300 - 5 hosts**: `192.168.2.0/29` (8 addresses)
  - Network: `192.168.2.0/29`
  - Gateway (L3-3): `192.168.2.1/29`
  - R10 G0/0: `192.168.2.2/29`
  - Usable: `192.168.2.3` - `192.168.2.6`
  - Broadcast: `192.168.2.7`

- **VLAN 1 - 2 hosts**: `192.168.3.0/30` (4 addresses)
  - Network: `192.168.3.0/30`
  - L3-3 Interface: `192.168.3.1/30`
  - L3-2 Interface: `192.168.3.2/30`

### R10 Branch
- **R10 G0/1 → S6**: `192.168.10.0/27` (32 addresses for 25 hosts)
  - Network: `192.168.10.0/27`
  - Gateway (R10 G0/1): `192.168.10.1/27`
  - Usable: `192.168.10.2` - `192.168.10.30`
  - Broadcast: `192.168.10.31`

### L3-2 VLANs

- **VLAN 200 - 12 hosts**: `192.168.4.0/28` (16 addresses)
  - Network: `192.168.4.0/28`
  - Gateway (L3-2): `192.168.4.1/28`
  - R9 G0/0: `192.168.4.2/28`
  - Usable: `192.168.4.3` - `192.168.4.14`
  - Broadcast: `192.168.4.15`

- **VLAN 100 - 8 hosts**: `192.168.5.0/28` (16 addresses)
  - Network: `192.168.5.0/28`
  - Gateway (L3-2): `192.168.5.1/28`
  - R8 G0/0: `192.168.5.2/28`
  - Usable: `192.168.5.3` - `192.168.5.14`
  - Broadcast: `192.168.5.15`

### R9 Branch
- **R9 G0/1 → S5**: `192.168.11.0/26` (64 addresses for 60 hosts)
  - Network: `192.168.11.0/26`
  - Gateway (R9 G0/1): `192.168.11.1/26`
  - Usable: `192.168.11.2` - `192.168.11.62`
  - Broadcast: `192.168.11.63`

### R8 Branch
- **R8 G0/1 → S4**: `192.168.12.0/27` (32 addresses for 14 hosts)
  - Network: `192.168.12.0/27`
  - Gateway (R8 G0/1): `192.168.12.1/27`
  - Usable: `192.168.12.2` - `192.168.12.30`
  - Broadcast: `192.168.12.31`

---

## **Area 3: Class A Network - 10.0.0.0/8**

### ISP Connection
- **ISP G1/1/2 ↔ R11 G0/0**: `10.0.0.0/30`
  - ISP Interface: `10.0.0.1/30`
  - R11 G0/0: `10.0.0.2/30`

### R11 Connections

#### R11 to S7 (Trunk)
- **R11 G0/1 → S7 G0/1**: Trunk carrying VLANs 6 & 7

#### S7 VLANs
- **VLAN 6 - 202,000 hosts**: `10.1.0.0/14` (262,144 addresses)
  - Network: `10.1.0.0/14`
  - Gateway (S7): `10.1.0.1/14`
  - Usable: `10.1.0.2` - `10.4.255.254`
  - Broadcast: `10.4.255.255`

- **VLAN 7 - 2,000 hosts**: `10.5.0.0/21` (2,048 addresses)
  - Network: `10.5.0.0/21`
  - Gateway (S7): `10.5.0.1/21`
  - Usable: `10.5.0.2` - `10.5.7.254`
  - Broadcast: `10.5.7.255`

#### R11 to L3-1
- **R11 G0/2 → L3-1**: Connected via VLAN 500

### L3-1 VLANs

- **VLAN 500 - 20 hosts**: `10.10.1.0/27` (32 addresses)
  - Network: `10.10.1.0/27`
  - Gateway (L3-1): `10.10.1.1/27`
  - R11 G0/2: `10.10.1.2/27`
  - Usable: `10.10.1.3` - `10.10.1.30`
  - Broadcast: `10.10.1.31`

- **VLAN 700 - 80 hosts**: `10.10.2.0/25` (128 addresses)
  - Network: `10.10.2.0/25`
  - Gateway (L3-1): `10.10.2.1/25`
  - R12 G0/0: `10.10.2.2/25`
  - Usable: `10.10.2.3` - `10.10.2.126`
  - Broadcast: `10.10.2.127`

- **VLAN 600 - 40 hosts**: `10.10.3.0/26` (64 addresses)
  - Network: `10.10.3.0/26`
  - Gateway (L3-1): `10.10.3.1/26`
  - R13 G0/0: `10.10.3.2/26`
  - Usable: `10.10.3.3` - `10.10.3.62`
  - Broadcast: `10.10.3.63`

### R12 to S8 (Trunk)
- **R12 G0/1 → S8 G0/1**: Trunk carrying VLANs 8 & 9

#### S8 VLANs
- **VLAN 8 - 200,000 hosts**: `10.20.0.0/14` (262,144 addresses)
  - Network: `10.20.0.0/14`
  - Gateway (S8): `10.20.0.1/14`
  - Usable: `10.20.0.2` - `10.23.255.254`
  - Broadcast: `10.23.255.255`

- **VLAN 9 - 10,000 hosts**: `10.24.0.0/18` (16,384 addresses)
  - Network: `10.24.0.0/18`
  - Gateway (S8): `10.24.0.1/18`
  - Usable: `10.24.0.2` - `10.24.63.254`
  - Broadcast: `10.24.63.255`

### R13 to S9 (Trunk)
- **R13 G0/1 → S9 G0/1**: Trunk carrying VLANs 10 & 11

#### S9 VLANs
- **VLAN 10 - 5,000,000 hosts**: `10.64.0.0/9` (8,388,608 addresses)
  - Network: `10.64.0.0/9`
  - Gateway (S9): `10.64.0.1/9`
  - Usable: `10.64.0.2` - `10.127.255.254`
  - Broadcast: `10.127.255.255`

- **VLAN 11 - 5,000 hosts**: `10.128.0.0/19` (8,192 addresses)
  - Network: `10.128.0.0/19`
  - Gateway (S9): `10.128.0.1/19`
  - Usable: `10.128.0.2` - `10.128.31.254`
  - Broadcast: `10.128.31.255`

---

## **ISP Router Summary**

- **G1/1/1** (to Area 1 - R1): `172.16.0.1/30`
- **G1/1/3** (to Area 2 - R7): `192.168.0.1/30`
- **G1/1/2** (to Area 3 - R11): `10.0.0.1/30`
- **Public IP Pool**: Can use public IP addresses as needed

---

## **Summary Statistics**

### Area 1 (Class B - 172.16.0.0/16)
- Total subnets: 12
- Total addressable hosts: ~2,200
- Largest subnet: VLAN 4 (1,024 hosts)
- Switches: S1, S2, S3a, S3b

### Area 2 (Class C - 192.168.0.0/16)
- Total subnets: 8
- Total addressable hosts: ~126
- Largest subnet: S5 (60 hosts)

### Area 3 (Class A - 10.0.0.0/8)
- Total subnets: 9
- Total addressable hosts: ~5,417,120
- Largest subnet: VLAN 10 (5,000,000 hosts)

### Total Network
- **Total subnets across all areas**: 29
- **Total addressable hosts**: ~5,419,446
- **Total router interfaces**: 39
- **Total VLANs**: 15
