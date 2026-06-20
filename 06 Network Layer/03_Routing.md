# 🗺️ Routing — Distance Vector, Link State, RIP vs OSPF vs BGP

---

## 1. What is Routing?

**Routing** is the process of **selecting a path** for traffic in a network. A **router** makes forwarding decisions based on its **routing table** — a map of known destinations and how to reach them.

```
Internet
   │
Router A ─────────── Router B ─────────── Router C
   │                     │                     │
  LAN-A               LAN-B                 LAN-C

When a packet arrives at Router A destined for LAN-C:
  Router A looks in routing table:
  "For 10.3.0.0/24 → send to Router B (next hop)"
```

### 1.1 Routing Table Entry

```
Destination     | Next Hop    | Metric | Interface
──────────────────────────────────────────────────
10.1.0.0/24     | 0.0.0.0     |   0    | eth0     (directly connected)
10.2.0.0/24     | 10.1.0.1    |   1    | eth0     (via Router B)
10.3.0.0/24     | 10.1.0.1    |   2    | eth0     (via Router B → C)
0.0.0.0/0       | 10.1.0.1    |   1    | eth0     (default route)
```

### 1.2 Types of Routing

| Type | Description | Example |
|------|-------------|---------|
| **Static Routing** | Manually configured routes | Home router default route |
| **Dynamic Routing** | Routers share info and auto-update | RIP, OSPF, BGP |
| **Default Routing** | One entry for all unmatched destinations (0.0.0.0/0) | Stub networks |

---

## 2. Distance Vector Routing

### 2.1 Concept

Each router maintains a **routing table** with:
- **Destination**: Each known network
- **Distance (metric)**: Cost to reach it (usually hop count)
- **Direction (vector)**: Next hop to get there

Routers share their **entire routing table** with their **direct neighbors** at regular intervals.

```
"I know how to reach network X in N hops — let me tell my neighbors"
```

### 2.2 Bellman-Ford Algorithm

Distance Vector routing is based on the **Bellman-Ford equation**:

$$D_x(y) = \min_{v \in \text{neighbors}(x)} \left[ c(x, v) + D_v(y) \right]$$

> "The distance from X to Y = the minimum of (cost to neighbor V + neighbor V's distance to Y), for all neighbors V."

```
Example: Router A wants to reach Z

Neighbors of A: B (cost=1), C (cost=4)
  B says: "I can reach Z in 3 hops"
  C says: "I can reach Z in 1 hop"

A calculates:
  Via B: 1 + 3 = 4
  Via C: 4 + 1 = 5
  Minimum: 4 → Use B as next hop!
```

### 2.3 How Routers Exchange Info

```
Each router sends its FULL routing table to each neighbor periodically
(e.g., every 30 seconds for RIP)

Router B shares:
  "I can reach A in 1 hop"
  "I can reach C in 1 hop"
  "I can reach D in 2 hops"

Router A receives and updates:
  A → C: via B, cost = 1(A→B) + 1(B→C) = 2
  A → D: via B, cost = 1(A→B) + 2(B→D) = 3
```

### 2.4 Convergence

**Convergence** = the time it takes all routers to agree on network topology after a change.

- Distance Vector converges **slowly** ("routing by rumor")
- Information spreads hop by hop, each router waits for neighbors to update

### 2.5 Count-to-Infinity Problem ⚠️

This is the **major flaw** of Distance Vector routing!

**Scenario:**
```
Network: A ──── B ──── C ──── [Network N]

A reaches N via B (2 hops). B reaches N via C (1 hop).

What happens if C loses connection to N?
```

**The Problem unfolds:**
```
Time 0:  A→N=2(via B), B→N=1(via C), C→N=0 (directly connected)

C loses N:
Time 1:  C table: N=∞ (unreachable)
         C hasn't sent update yet.

Time 1 (before C sends update):
         B still thinks: N=1 via C
         A still thinks: N=2 via B

B sends update:
         C receives: "B says N=2" → C thinks: "Oh! I can reach N via B in 3 hops!"
         C→N = 3 (via B) ← WRONG! B's route goes back through C!

A sends update:
         B receives: "A says N=3" (A→B + B→N=1+2=3)? Wait...
         B checks: C now says N=3, so B→N = 1+3 = 4
         ...

Infinite loop: distances keep increasing 1, 2, 3, 4, 5 ... → "Count to Infinity"
```

**Visual:**
```
┌──────────────────────────────────────────────┐
│  Time  │  A→N  │  B→N  │  C→N              │
│   0    │   2   │   1   │   0  (connected)  │
│   1    │   2   │   1   │   ∞  (link fails) │
│   2    │   2   │   3   │   4  ← C via B    │
│   3    │   4   │   5   │   6  ← keeps going│
│   ...  │  ...  │  ...  │  ... → infinity   │
└──────────────────────────────────────────────┘
Routers keep claiming they can reach N, distance grows forever!
```

### 2.6 Solutions to Count-to-Infinity

#### A. Maximum Metric (Infinity = 16 in RIP)
- Define a maximum hop count (RIP uses **16 = infinity**)
- Routing stops when metric reaches 16
- **Limitation**: Only works for small networks (max 15 hops)

#### B. Split Horizon
- **Don't advertise a route back** to the neighbor you learned it from
- "Don't tell B that you can reach N via B — B already knows!"

```
C learned N via B:
  With Split Horizon, C does NOT advertise N back to B
  B never thinks C has a valid route back → count-to-infinity prevented!
```

#### C. Poison Reverse (Route Poisoning)
- Instead of not advertising, **explicitly advertise with metric=infinity**
- More aggressive than split horizon; faster convergence

```
If C loses N:
  C immediately sends to all neighbors: "N = 16 (infinity)" ← Poisoned
  B gets: N=∞ via C → removes route to N
  No counting up!
```

#### D. Triggered Updates
- Send routing updates **immediately** when a route changes, don't wait for the next periodic update
- Speeds up convergence after a failure

---

## 3. Link State Routing

### 3.1 Concept

Each router:
1. Discovers its **neighbors** and their link costs
2. Broadcasts **LSAs (Link State Advertisements)** to the **entire network** — not just neighbors!
3. Builds a **complete map** (graph) of the entire network
4. Runs **Dijkstra's Shortest Path Algorithm** to compute optimal routes

```
"I know everything about the entire network topology"
```

### 3.2 Link State Advertisement (LSA)

Each router broadcasts its LSA to ALL routers using **flooding**:

```
Router A's LSA: "I am A. My neighbors are: B(cost=1), C(cost=4)"
Router B's LSA: "I am B. My neighbors are: A(cost=1), D(cost=2)"
Router C's LSA: "I am C. My neighbors are: A(cost=4), D(cost=1)"
Router D's LSA: "I am D. My neighbors are: B(cost=2), C(cost=1)"
```

After receiving all LSAs, every router has the complete topology:
```
    A
   /│
  1 4
 /  │
B   C
 \  /
  2 1
   \│
    D
```

### 3.3 Dijkstra's Algorithm

Each router runs Dijkstra's algorithm on its topology database:

**Example:** Find shortest paths from A

```
Graph:  A──1──B──2──D
        A──4──C──1──D

Step 1: Initialize
  Dist: {A:0, B:∞, C:∞, D:∞}
  Visited: {}

Step 2: Pick unvisited node with min distance → A (dist=0)
  Update neighbors: B=0+1=1, C=0+4=4
  Dist: {A:0, B:1, C:4, D:∞}
  Visited: {A}

Step 3: Pick next → B (dist=1)
  Update neighbors: D=1+2=3
  Dist: {A:0, B:1, C:4, D:3}
  Visited: {A, B}

Step 4: Pick next → D (dist=3)
  Update neighbors: C=min(4, 3+1)=4 (no improvement)
  Visited: {A, B, D}

Step 5: Pick next → C (dist=4)
  No better paths
  Visited: {A, B, D, C}

Result (from A):
  A→B: cost 1, via direct link
  A→D: cost 3, via B
  A→C: cost 4, via direct link (or via B→D→C = 4, same)
```

### 3.4 Distance Vector vs Link State — Comparison

| Feature | Distance Vector | Link State |
|---------|----------------|------------|
| **What is shared** | Routing table (to neighbors only) | LSAs (topology to ALL routers) |
| **Knowledge** | Only neighbors' tables | Complete network topology |
| **Algorithm** | Bellman-Ford | Dijkstra's SPF |
| **Convergence** | Slow | **Fast** |
| **Memory** | Low | High (stores full topology) |
| **CPU** | Low | High (Dijkstra computation) |
| **Count-to-infinity** | ⚠️ Yes — major problem | ❌ No (full topology prevents loops) |
| **Updates** | Periodic (every 30s) | Event-driven (only on change) |
| **Scalability** | Small networks | Large networks |
| **Protocols** | RIP | OSPF, IS-IS |

---

## 4. RIP vs OSPF vs BGP

### 4.1 Overview

| Protocol | Type | Category | Use Case |
|---------|------|---------|---------|
| **RIP** | Distance Vector | IGP | Small networks |
| **OSPF** | Link State | IGP | Enterprise/large networks |
| **BGP** | Path Vector | EGP | Internet (between ISPs/ASes) |

> **IGP** = Interior Gateway Protocol (within one AS)
> **EGP** = Exterior Gateway Protocol (between different ASes)
> **AS** = Autonomous System (a network under one administration)

### 4.2 RIP — Routing Information Protocol

```
Type: Distance Vector
Metric: Hop Count (max 15; 16 = infinity)
Update: Every 30 seconds (full table broadcast)
Port: UDP 520
Versions: RIPv1 (classful), RIPv2 (classless, CIDR support)
```

**Key Characteristics:**
- Simple, easy to configure
- Maximum 15 hops → only suitable for **small networks**
- Slow convergence (30-second updates)
- Count-to-infinity problem (mitigated by split horizon + poison reverse)

**RIP Timers:**
| Timer | Duration | Purpose |
|-------|----------|---------|
| Update | 30 sec | Send routing table |
| Invalid | 180 sec | Mark route as invalid if no update |
| Holddown | 180 sec | Ignore updates for invalid route |
| Flush | 240 sec | Remove invalid route from table |

### 4.3 OSPF — Open Shortest Path First

```
Type: Link State
Metric: Cost (bandwidth-based: Cost = 10^8 / bandwidth in bps)
Update: Event-driven (only when topology changes)
Protocol: IP Protocol 89 (not TCP/UDP)
Standard: RFC 2328 (OSPFv2 for IPv4), RFC 5340 (OSPFv3 for IPv6)
```

**Key Characteristics:**
- Fast convergence
- No hop limit (scales to large networks)
- Supports VLSM and CIDR
- Uses **Dijkstra's algorithm**
- Hierarchical design with **Areas** (Area 0 = backbone)
- Sends **Hello packets** to discover/maintain neighbors

**OSPF Areas:**
```
          Area 0 (Backbone)
         /        |        \
      Area 1    Area 2    Area 3
    (Finance) (Engineering) (HR)

All areas must connect to Area 0!
ABR (Area Border Router) connects non-backbone areas to backbone.
```

**OSPF Metric:**
$$\text{Cost} = \frac{10^8}{\text{bandwidth (bps)}}$$

| Link Type | Bandwidth | OSPF Cost |
|-----------|-----------|-----------|
| FastEthernet | 100 Mbps | 1 |
| Ethernet | 10 Mbps | 10 |
| T1 | 1.544 Mbps | 64 |
| Serial | 64 kbps | 1562 |

### 4.4 BGP — Border Gateway Protocol

```
Type: Path Vector (enhanced version of distance vector)
Metric: AS Path (list of autonomous systems to traverse)
Transport: TCP port 179
Version: BGP-4 (current)
Standard: RFC 4271
```

**Key Characteristics:**
- The **routing protocol of the Internet** — connects all ISPs
- Routes between **Autonomous Systems (AS)**, not individual networks
- Very **policy-driven** (ISPs choose paths based on business agreements, not just shortest path)
- Uses **TCP** for reliability (not UDP like RIP)
- Slow convergence (by design — stability over speed)

**BGP Types:**
```
iBGP (internal BGP): BGP sessions within the same AS
eBGP (external BGP): BGP sessions between different ASes

ISP-A (AS 100) ──eBGP── ISP-B (AS 200) ──eBGP── ISP-C (AS 300)
                                  │ iBGP between internal routers
```

**BGP Path Selection (simplified):**
1. Highest **Weight** (Cisco-specific)
2. Highest **Local Preference**
3. Shortest **AS Path** (fewer hops = preferred)
4. Lowest **Origin** type
5. Lowest **MED** (Multi-Exit Discriminator)
6. **eBGP** over **iBGP**

### 4.5 Complete Comparison Table

| Feature | RIP | OSPF | BGP |
|---------|-----|------|-----|
| **Type** | Distance Vector | Link State | Path Vector |
| **Category** | IGP | IGP | EGP |
| **Algorithm** | Bellman-Ford | Dijkstra (SPF) | Path selection policy |
| **Metric** | Hop count | Bandwidth cost | AS Path length |
| **Max hops** | **15** | Unlimited | Unlimited |
| **Convergence** | Slow | Fast | Very slow (stable) |
| **Updates** | Every 30s | Event-driven | Event-driven |
| **Transport** | UDP/520 | IP/89 | TCP/179 |
| **Scale** | Small | Large enterprise | Internet-scale |
| **Loops** | Count-to-infinity | No loops | AS path prevents loops |
| **Admin overhead** | Low | High | Very high |
| **Use case** | Simple/small nets | Enterprise | Internet routing |

---

## 5. Interview Questions

**Q1: What is the difference between Distance Vector and Link State routing?**
> Distance Vector routers share routing tables with direct neighbors only; they know costs but not topology (Bellman-Ford). Link State routers flood LSAs to all routers; each builds a complete topology map and runs Dijkstra's algorithm. Link State converges faster and doesn't have the count-to-infinity problem.

**Q2: What is the count-to-infinity problem?**
> When a link fails, Distance Vector routers can enter a loop where they keep incrementing the metric for an unreachable network (A thinks it can reach N via B; B thinks it can reach N via A; they keep counting up toward infinity). It occurs because routers know costs, not full topology.

**Q3: How does split horizon solve count-to-infinity?**
> Split horizon prevents a router from advertising a route back to the neighbor it learned that route from. This breaks the loop: if B told A about network N, A won't tell B about N. Poison reverse is the stronger variant — it explicitly sends metric=infinity back.

**Q4: What is OSPF's metric and how is it calculated?**
> OSPF uses bandwidth-based cost = 10⁸ / bandwidth in bps. Higher bandwidth = lower cost = preferred path. FastEthernet (100 Mbps) has cost 1; a 64 kbps serial link has cost ~1562.

**Q5: Why does BGP use TCP instead of UDP?**
> BGP requires reliable, ordered delivery of routing updates because losing or misdelivering a BGP update could cause serious routing problems. TCP (port 179) provides this reliability. BGP peers form long-lived TCP sessions.

**Q6: What is an Autonomous System (AS)?**
> An AS is a network or group of networks under a single administrative authority with a unified routing policy. Each AS has a unique ASN (Autonomous System Number). BGP routes between ASes; OSPF/RIP route within an AS.

**Q7: Why is RIP limited to 15 hops?**
> RIP uses hop count as its metric and defines 16 as infinity (unreachable). This limits RIP networks to 15 hops to prevent the count-to-infinity problem from running forever. This also means RIP is unsuitable for large networks.

---

*Next: [04 — Other Concepts (Fragmentation, Tunneling, NAT) →](./04_Other_Concepts.md)*
