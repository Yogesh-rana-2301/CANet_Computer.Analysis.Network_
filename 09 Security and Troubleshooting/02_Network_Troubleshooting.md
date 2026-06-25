#   Network Troubleshooting

> Knowing how to diagnose network problems is as important as knowing how networks work. These tools and concepts are asked in both SDE and SRE/DevOps interviews.

---

## 1. The Troubleshooting Mindset

**Systematic approach — always work top-down or bottom-up through the OSI model:**

```
Top-down (Application → Physical):
  Can you reach the website? (Application)
  Can you make a TCP connection? (Transport)
  Can you ping the IP? (Network)
  Is the ARP table correct? (Data Link)
  Is the cable plugged in? (Physical)

Bottom-up (Physical → Application):
  Is the link up? (Physical)
  Are you getting a DHCP address? (Data Link/Network)
  Can you ping the gateway? (Network)
  Can you reach external IPs? (Network/Routing)
  Is DNS resolving? (Application)
  Is the application responding? (Application)
```

---

## 2. Ping Command ⭐

### 2.1 What is Ping?

`ping` is the most fundamental network diagnostic tool. It tests **reachability** and measures **round-trip time (RTT)** between your machine and a remote host using **ICMP Echo Request/Reply**.

```
You ──[ ICMP Echo Request ]──→ Target
You ←─[ ICMP Echo Reply   ]── Target

RTT = time from sending request to receiving reply
```

### 2.2 How Ping Works

```
Step 1: ping sends ICMP Type 8 (Echo Request) with:
  - Identifier: process ID
  - Sequence number: increments each packet
  - Data: timestamp + padding

Step 2: Target responds with ICMP Type 0 (Echo Reply):
  - Copies identifier + sequence number back
  - Echoes the data

Step 3: ping displays:
  64 bytes from 8.8.8.8: icmp_seq=1 ttl=118 time=12.4 ms
  64 bytes from 8.8.8.8: icmp_seq=2 ttl=118 time=11.9 ms
  64 bytes from 8.8.8.8: icmp_seq=3 ttl=118 time=12.1 ms
```

### 2.3 Reading Ping Output

```
$ ping google.com
PING google.com (142.250.68.46): 56 data bytes
64 bytes from 142.250.68.46: icmp_seq=0 ttl=118 time=12.456 ms
64 bytes from 142.250.68.46: icmp_seq=1 ttl=118 time=11.923 ms
64 bytes from 142.250.68.46: icmp_seq=2 ttl=118 time=12.341 ms
^C
--- google.com ping statistics ---
3 packets transmitted, 3 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 11.923/12.240/12.456/0.222 ms
```

| Field | Meaning |
|-------|---------|
| `64 bytes` | Reply size |
| `142.250.68.46` | Resolved IP |
| `icmp_seq=0` | Sequence number (check for gaps = packet loss) |
| `ttl=118` | Time To Live remaining when reply arrived |
| `time=12.456 ms` | Round-trip time |
| `0.0% packet loss` | No packets dropped |
| `min/avg/max/stddev` | RTT statistics |

### 2.4 Interpreting Ping Results

| Scenario | Possible Cause |
|---------|---------------|
| `Request timeout` | Host down, ICMP blocked by firewall, routing problem |
| `Host Unreachable` | No route to host (routing table issue) |
| `Network Unreachable` | No route to network |
| `TTL expired` | Routing loop (packet circles forever) |
| High RTT (e.g., >200ms) | Congestion, long path, satellite link |
| `Ping OK` to IP but not name | DNS problem |
| `Ping OK` to gateway but not internet | ISP/routing problem beyond gateway |
| Varying RTT with packet loss | Network congestion |

### 2.5 Common Ping Options

```
ping -c 5 google.com       # Send exactly 5 packets
ping -i 0.2 google.com     # Send every 0.2 seconds (flood test)
ping -s 1400 google.com    # Use 1400-byte packet size (MTU testing)
ping -t 64 google.com      # Set TTL to 64
ping -D google.com         # Print timestamps
```

### 2.6 Diagnostic Use Cases

```
Scenario: "I can't access www.example.com"

Step 1: ping 127.0.0.1   → Tests local TCP/IP stack
  ❌ Fail → OS networking broken

Step 2: ping 192.168.1.1  → Tests local gateway
  ❌ Fail → Local network issue (cable, WiFi, DHCP)

Step 3: ping 8.8.8.8     → Tests internet connectivity (IP level)
  ❌ Fail → ISP issue or default route problem

Step 4: ping www.example.com → Tests DNS + internet
  ❌ Fail → DNS resolution problem

Step 5: All pings OK → Problem is application-specific (port 80/443 blocked, web server down)
```

### 2.7 Why Ping Might Fail Incorrectly

Many servers and firewalls **block ICMP** for security reasons:
```
ping google.com → Request timeout
  But: The website loads fine in a browser!

This means ICMP is blocked, not that the host is unreachable.
Use traceroute or curl to verify.
```

---

## 3. Traceroute ⭐ IMPORTANT

### 3.1 What is Traceroute?

`traceroute` (Linux/Mac) / `tracert` (Windows) reveals the **complete path** a packet takes from source to destination, showing every router (hop) along the way and the **latency to each hop**.

```
Your PC → ISP Router → Backbone → Peering → Destination
  ↑           ↑            ↑          ↑            ↑
 Hop 1       Hop 2        Hop 3      Hop 4        Hop 5
```

### 3.2 How Traceroute Works — The TTL Trick ⭐

Traceroute exploits the **TTL (Time To Live)** field in IP packets:

- Every router **decrements TTL by 1**
- When TTL reaches **0**: router **drops the packet** and sends **ICMP Time Exceeded (Type 11)** back to the source

Traceroute sends probes with **incrementally increasing TTL** (1, 2, 3, ...):

```
Probe with TTL=1:
  Your PC → Router1 (TTL becomes 0!) → Router1 sends "Time Exceeded" back
  Result: "Hop 1 = Router1, RTT = X ms"

Probe with TTL=2:
  Your PC → Router1 (TTL=1) → Router2 (TTL=0!) → Router2 sends "Time Exceeded"
  Result: "Hop 2 = Router2, RTT = Y ms"

Probe with TTL=3:
  Your PC → R1 → R2 → Router3 (TTL=0!) → Router3 sends "Time Exceeded"
  Result: "Hop 3 = Router3, RTT = Z ms"

...

Probe with TTL=N:
  Your PC → ... → Destination
  Destination sends ICMP Echo Reply (or ICMP Port Unreachable for UDP)
  Result: "Reached destination! RTT = W ms"
```

### 3.3 Traceroute Output Explained

```
$ traceroute google.com
traceroute to google.com (142.250.68.46), 30 hops max, 60 byte packets
 1  192.168.1.1       1.2 ms   1.1 ms   1.0 ms    ← Home router
 2  10.20.30.1        8.5 ms   8.3 ms   8.7 ms    ← ISP gateway
 3  172.20.50.1      10.2 ms  10.1 ms  10.5 ms    ← ISP backbone
 4  203.0.113.4      12.1 ms  11.9 ms  12.3 ms    ← ISP core
 5  72.14.204.1      13.5 ms  13.2 ms  14.1 ms    ← Google peering
 6  142.251.48.1     14.2 ms  14.0 ms  14.5 ms    ← Google internal
 7  142.250.68.46    14.8 ms  14.6 ms  14.9 ms    ← Destination! ✅
```

| Column | Meaning |
|--------|---------|
| `1`, `2`, `3`... | Hop number |
| `192.168.1.1` | IP of the router at that hop |
| `1.2 ms 1.1 ms 1.0 ms` | RTT for each of **3 probes** sent to that hop |

### 3.4 Reading Traceroute Output — Patterns to Recognize

**Pattern 1: Normal hop**
```
5  72.14.204.1  13.5 ms  13.2 ms  14.1 ms
```
→ Normal, consistent latency. ✅

**Pattern 2: Asterisks (***)**
```
6  * * *
```
→ Router at hop 6 either:
  - Blocks ICMP Time Exceeded
  - Rate-limits ICMP responses
  - Is very busy
This does NOT necessarily mean the hop is unreachable!

**Pattern 3: High latency spike at one hop, then normal**
```
4  203.0.113.4      5 ms
5  *  *  *
6  72.14.204.1    200 ms  ← spike here
7  142.251.48.1    15 ms  ← back to normal!
```
→ Hop 6's ICMP is rate-limited or deprioritized. **Actual path is fine** (hop 7 is normal).
→ The 200ms is how long the router takes to generate ICMP responses, not actual path latency.

**Pattern 4: Increasing latency (normal)**
```
1   1 ms
2   8 ms
3  15 ms
4  20 ms
5  30 ms  ← latency grows as we get farther
```
→ Normal — each hop adds propagation delay. ✅

**Pattern 5: Routing loop**
```
 5  203.0.113.4  5 ms
 6  203.0.113.1  6 ms
 7  203.0.113.4  7 ms   ← same IP as hop 5!
 8  203.0.113.1  8 ms   ← routing loop!
```
→ Routing loop — packets going back and forth between two routers. ⚠️

**Pattern 6: High latency throughout (from a certain hop)**
```
1   1 ms
2   5 ms
3   8 ms
4  150 ms  ← jump here
5  151 ms
6  153 ms
```
→ High latency introduced at hop 4 — problem is between hop 3 and hop 4 (e.g., congested link, intercontinental fiber). ⚠️

### 3.5 Linux vs Windows vs macOS Differences

| Feature | Linux/Mac (traceroute) | Windows (tracert) |
|---------|----------------------|------------------|
| Protocol | UDP (default) or ICMP (`-I`) | ICMP |
| Probes per hop | 3 | 3 |
| Max hops default | 30 | 30 |
| Port used | High UDP port (~33434+) | N/A (ICMP) |

```
# Linux — use ICMP (like Windows, better firewall compatibility):
sudo traceroute -I google.com

# macOS:
traceroute google.com

# Windows:
tracert google.com
```

### 3.6 Why Traceroute Uses UDP (by default, Linux)

Linux traceroute sends UDP packets to high port numbers (33434+). When the packet arrives at the destination, nobody is listening → destination sends **ICMP Port Unreachable (Type 3, Code 3)** — traceroute knows it reached the end!

```
TTL=1: Router sends ICMP Time Exceeded (identifies hop 1)
TTL=2: Router sends ICMP Time Exceeded (identifies hop 2)
...
TTL=N (destination): Destination sends ICMP Port Unreachable → Done! ✅
```

---

## 4. Other Essential Diagnostic Tools

### 4.1 nslookup / dig — DNS Debugging

```
# nslookup (basic):
$ nslookup google.com
Server:    8.8.8.8
Address:   8.8.8.8#53
Name:      google.com
Address:   142.250.68.46

# dig (detailed):
$ dig google.com
;; ANSWER SECTION:
google.com.    255   IN   A   142.250.68.46

;; Query time: 12 msec
;; SERVER: 8.8.8.8#53

# Specify DNS server:
$ dig @1.1.1.1 google.com

# Query specific record type:
$ dig MX gmail.com
$ dig NS google.com
$ dig AAAA google.com     # IPv6 address
```

**Use case:**
```
Symptom: Can ping 8.8.8.8, but can't reach google.com
Diagnosis: dig google.com → if fails → DNS problem
           nslookup google.com 8.8.8.8 → if works → local DNS broken
```

### 4.2 netstat / ss — Port and Connection Status

```
# Show all listening ports:
netstat -tlnp   (Linux)
ss -tlnp        (modern Linux)

# Show active connections:
netstat -an

# Check if specific port is listening:
netstat -tlnp | grep :80
ss -tlnp | grep :443

# Windows:
netstat -ano
```

**Use cases:**
```
"Is the web server running?" → check if :80 or :443 is LISTENING
"Is someone connected?" → check ESTABLISHED connections
"What ports am I using?" → view all connections
```

### 4.3 curl / wget — HTTP Debugging

```
# Basic HTTP request:
curl http://example.com

# Show only headers (useful for checking status codes, redirects):
curl -I http://example.com

# Verbose mode (see TLS handshake, headers, etc.):
curl -v https://example.com

# Follow redirects:
curl -L http://example.com

# Check specific IP (bypass DNS):
curl --resolve example.com:80:93.184.216.34 http://example.com

# Test with specific headers:
curl -H "Authorization: Bearer token" https://api.example.com
```

### 4.4 arp — ARP Cache Inspection

```
# View ARP table:
arp -a

# Delete stale ARP entry:
arp -d 192.168.1.50

# Add static ARP entry:
arp -s 192.168.1.50 aa:bb:cc:dd:ee:ff
```

**Use case:**
```
"Can't reach 192.168.1.50"
→ Check arp -a → if IP is there but wrong MAC → ARP poisoning attack!
→ if IP not in ARP table → device unreachable or ARP failing
```

### 4.5 ip / ifconfig / ipconfig — Interface Status

```
# Linux — view interfaces:
ip addr show
ip link show

# Linux — routing table:
ip route show

# macOS/old Linux:
ifconfig

# Windows:
ipconfig /all
ipconfig /flushdns     # Clear DNS cache
ipconfig /release      # Release DHCP lease
ipconfig /renew        # Renew DHCP lease
```

---

## 5. Common Network Issues and Diagnosis

### 5.1 Troubleshooting Table

| Symptom | Possible Cause | Tool to Diagnose | Fix |
|---------|---------------|-----------------|-----|
| Can't ping gateway | No IP / wrong gateway / cable | `ip addr`, `ipconfig` | Check DHCP, cable |
| Can reach IPs, not names | DNS broken | `nslookup`, `dig` | Change DNS server |
| High latency | Congestion, long path | `ping`, `traceroute` | Identify bottleneck |
| Packet loss | Congestion, bad cable, interference | `ping`, `mtr` | Check hardware, route |
| Port not responding | Service down, firewall | `curl`, `netstat` | Restart service, check FW |
| Intermittent drops | Physical layer issues | Long `ping` run | Check cables, WiFi signal |
| Slow website | CDN, server, DNS | `curl -v`, `dig` | CDN, optimize |

### 5.2 Packet Loss — Causes and Diagnosis

**Packet loss** occurs when data packets fail to reach their destination:

```
Causes of packet loss:
  1. Network congestion (buffers overflow → packets dropped)
  2. Physical layer issues (bad cable, weak WiFi signal)
  3. Hardware failure (faulty NIC, malfunctioning router)
  4. Firewall dropping packets
  5. Buffer bloat (over-buffering causing queue buildup)

Effects:
  → TCP detects loss → retransmits → latency spikes
  → Video calls stutter (UDP doesn't retransmit → pixelation)
  → Downloads slow (TCP backs off)
```

**Measuring packet loss with ping:**
```
$ ping -c 100 8.8.8.8
--- 8.8.8.8 ping statistics ---
100 packets transmitted, 93 packets received, 7.0% packet loss
                                              ↑
                            7% packet loss! Significant problem!
```

**Acceptable thresholds:**
| Packet Loss | Quality |
|------------|---------|
| 0% | Perfect |
| 0.1–1% | Good (minor congestion) |
| 1–5% | Noticeable (VoIP issues) |
| 5–10% | Serious degradation |
| >10% | Severe problem |

### 5.3 MTU Issues

```
Symptom: Can ping small packets but large transfers fail
Cause: MTU mismatch (often VPN or PPPoE reduces MTU below 1500)

Diagnosis:
$ ping -s 1472 -D 8.8.8.8   # -D = Don't Fragment, -s = size
  (1472 + 28 bytes header = 1500 bytes total)
  
If this works → 1500 MTU OK
If ping -s 1400 -D works but ping -s 1450 -D fails → MTU is between 1428-1478

Fix: Reduce MTU on interface or set TCP MSS clamping on router
```

### 5.4 Diagnosing Slow Network — mtr

`mtr` (My Traceroute) combines **ping + traceroute** in real-time:

```
$ mtr google.com

My TraceRoute [v0.93]
Host                        Loss%   Snt   Last    Avg   Best   Wrst  StDev
1. 192.168.1.1              0.0%    20    1.2     1.1   0.9    1.5    0.1
2. 10.20.30.1               0.0%    20    8.3     8.5   8.1    9.1    0.2
3. 172.20.50.1              5.0%    20   10.2    10.5   9.9   12.1    0.6  ← 5% loss!
4. 203.0.113.4              5.0%    20   12.1    12.3  11.9   13.5    0.4
5. 142.250.68.46            0.0%    20   14.8    14.6  14.2   15.1    0.2

The 5% loss at hop 3 (and hop 4 inheriting it) suggests the problem
is on the link between hop 2 and hop 3.
```

---

## 6. Checklist: Systematic Network Troubleshooting

```
┌─────────────────────────────────────────────────────────────┐
│          NETWORK TROUBLESHOOTING CHECKLIST                  │
└─────────────────────────────────────────────────────────────┘

PHYSICAL LAYER:
□ Is the cable plugged in? (Check link lights on NIC/switch)
□ Is WiFi connected? (Check signal strength)
□ Run: ip link show / ipconfig

DATA LINK / NETWORK — LOCAL:
□ Do I have an IP address? (DHCP working?)
□ Is the subnet mask correct?
□ Is the default gateway set?
□ Can I ping my own IP? (ping 127.0.0.1)
□ Can I ping my gateway? (ping 192.168.1.1)

NETWORK — INTERNET:
□ Can I ping an internet IP? (ping 8.8.8.8)
□ Is the routing correct? (ip route show)
□ Any firewall blocking outbound? (curl http://example.com)

APPLICATION — DNS:
□ Can I resolve names? (nslookup google.com)
□ Is it a specific domain? Try different domains
□ Flush DNS cache and retry

APPLICATION — SERVICE:
□ Is the right port open? (netstat -tlnp)
□ Is the service running? (systemctl status nginx)
□ Are there error logs? (/var/log/nginx/error.log)
□ Is there a firewall blocking the port?
```

---

## 7. Interview Questions

**Q1: How does ping work?**
> Ping sends ICMP Echo Request (Type 8) to the target. If reachable, the target responds with ICMP Echo Reply (Type 0). Ping measures the RTT and reports packet loss. It uses the OS's network stack, going through all layers (IP, routing, etc.) to reach the destination.

**Q2: How does traceroute work?**
> Traceroute sends probes with incrementally increasing TTL (starting at 1). At each router, TTL is decremented. When TTL=0, the router drops the packet and sends ICMP Time Exceeded back. Traceroute records that router's IP and RTT as a hop. This continues until the destination is reached (which sends ICMP Port Unreachable or Echo Reply).

**Q3: What do asterisks (***) in traceroute mean?**
> The router at that hop is not sending ICMP Time Exceeded responses — either it blocks ICMP, rate-limits it, or deprioritizes it. It does NOT necessarily mean the router is down or the path is broken — subsequent hops still working proves traffic is passing through.

**Q4: You can ping 8.8.8.8 but can't browse the web. What's wrong?**
> DNS is broken. The network is up (ping to IP works), but name resolution is failing. Diagnose with `nslookup google.com`. Fix: check DNS server configuration, try a different DNS server (8.8.8.8 or 1.1.1.1).

**Q5: What is packet loss and how is it measured?**
> Packet loss occurs when sent packets fail to reach the destination (congestion, hardware failure, interference). Measured with ping: `ping -c 100 8.8.8.8` shows "X% packet loss". Above 1% is concerning for real-time apps; above 5% indicates a serious problem.

**Q6: What is the difference between ping and traceroute?**
> Ping tests end-to-end reachability and RTT to a single destination. Traceroute reveals the complete path (every router hop), RTT to each hop, and helps identify WHERE in the path a problem exists — not just that a problem exists.

**Q7: A website is slow. How would you diagnose it?**
> 1) `ping` the server — measure RTT and packet loss. 2) `traceroute` — find where latency is high. 3) `dig` — check DNS resolution time. 4) `curl -v` — measure time to connect, time to first byte, total download time. 5) Check server-side logs and resource usage (CPU, memory, disk I/O).

---

*← Back to [Index](./README.md)*
