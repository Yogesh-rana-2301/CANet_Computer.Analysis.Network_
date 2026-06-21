# 🔍 DNS — Domain Name System

> DNS is the **"phone book of the internet"** — it translates human-readable domain names into IP addresses.

---

## 1. Why DNS Exists

Computers communicate using **IP addresses** (e.g., `142.250.68.46`), but humans prefer memorable names like `google.com`. DNS bridges this gap automatically.

```
You type:        www.google.com
DNS resolves:  → 142.250.68.46
Browser uses:    142.250.68.46 to connect
```

Without DNS, you'd have to memorize IPs for every website.

---

## 2. DNS Hierarchy

DNS is organized as a **distributed, hierarchical, globally distributed database** — no single server knows everything.

```
                         . (Root)
                        / | \
               .com   .org  .in   .net   .edu  ...
              /    \
        google   amazon
        /    \
      www    mail
```

### Levels of the DNS Hierarchy

```
Root (.)
 └── Top-Level Domain (TLD)
      ├── Generic TLDs: .com, .org, .net, .edu, .gov
      ├── Country Code TLDs (ccTLD): .in, .uk, .us, .jp
      └── New TLDs: .app, .io, .dev
           └── Second-Level Domain (SLD)
                └── google (.com)
                     └── Subdomain
                          └── www.google.com
                              mail.google.com
```

### DNS Name Structure

```
   www    .   google   .   com   .
   ───         ───         ───     ─
subdomain    2nd-level    TLD    root
             domain             (implicit)

FQDN (Fully Qualified Domain Name) = www.google.com.
                                                   ↑ trailing dot = root
```

---

## 3. DNS Components

### 3.1 DNS Resolver (Recursive Resolver)

- Also called **Local DNS Server** or **Recursive Resolver**
- Usually provided by your **ISP** or services like `8.8.8.8` (Google), `1.1.1.1` (Cloudflare)
- **Your first point of contact** when you query a domain
- Does the heavy lifting — queries other servers on your behalf
- Caches results to speed up future lookups

```
Your Computer
  └── Recursive Resolver (ISP / 8.8.8.8)
        ├── Root Name Server
        ├── TLD Name Server
        └── Authoritative Name Server
```

### 3.2 Root Name Servers

- **13 sets** of root name servers (labeled A through M), operated by different organizations
- Don't know the IP of `google.com` — but know which **TLD server** to ask
- Globally distributed (hundreds of physical servers via anycast)

```
Root server knows:
  ".com  → TLD server at 192.5.6.30"
  ".org  → TLD server at 199.19.56.1"
  ".in   → TLD server at 37.209.192.12"
```

### 3.3 TLD Name Servers

- Manage top-level domains (`.com`, `.org`, `.in`, etc.)
- Operated by domain registries (VeriSign manages `.com`)
- Know which **Authoritative Name Server** handles each domain

```
.com TLD server knows:
  "google.com → Authoritative NS at ns1.google.com (216.239.32.10)"
  "amazon.com → Authoritative NS at ns1.p31.dynect.net"
```

### 3.4 Authoritative Name Server

- The **final authority** for a specific domain
- Stores the actual **DNS records** (A, AAAA, MX, CNAME, etc.)
- Returns the definitive answer

```
ns1.google.com knows:
  "www.google.com  → A record: 142.250.68.46"
  "mail.google.com → MX record: aspmx.l.google.com"
```

---

## 4. DNS Resolution — How It Works

### 4.1 Full DNS Resolution (When Not Cached)

```
Browser: "What's the IP for www.google.com?"

Step 1: Check LOCAL CACHE (browser cache, OS cache)
        → Not found!

Step 2: Ask Recursive Resolver (e.g., 8.8.8.8)
        Resolver checks its cache → Not found
        → Resolver starts querying on your behalf

Step 3: Resolver asks ROOT SERVER
        Root: "I don't know google.com, but .com is handled by:
               TLD server at 192.5.6.30"

Step 4: Resolver asks .COM TLD SERVER
        TLD: "I don't know www.google.com, but google.com is handled by:
              Authoritative NS: ns1.google.com at 216.239.32.10"

Step 5: Resolver asks AUTHORITATIVE SERVER (ns1.google.com)
        Auth NS: "www.google.com = 142.250.68.46" ✅

Step 6: Resolver returns 142.250.68.46 to your browser
        (and caches it for future queries)

Step 7: Browser connects to 142.250.68.46
```

#### Visual Timeline
```
Your PC          Resolver        Root NS       .com TLD NS    Auth NS (Google)
  │                │               │               │               │
  │──www.google──→ │               │               │               │
  │               │──www.google──→│               │               │
  │               │←─ ask .com ───│               │               │
  │               │──www.google──────────────────→│               │
  │               │←─ ask google NS ──────────────│               │
  │               │──www.google────────────────────────────────→  │
  │               │←─ 142.250.68.46 ──────────────────────────────│
  │←─142.250.68.46│               │               │               │
  │               │               │               │               │
```

---

## 5. Recursive vs Iterative Queries

### 5.1 Recursive Query

The client asks the resolver to **do all the work** and return a final answer.

```
Client → Resolver: "Give me the IP for www.google.com"
                    (Resolver does everything)
Resolver → Client: "Here's the IP: 142.250.68.46"

Client gets a COMPLETE answer — no partial answers.
```

**Who uses recursive queries?**
- Your computer → Recursive Resolver (always recursive)

### 5.2 Iterative Query

The resolver asks each server in sequence; each server **returns a referral** (not the final answer) to the next server to query.

```
Resolver → Root: "What's www.google.com?"
Root → Resolver: "I don't know. Ask .com TLD at 192.5.6.30"

Resolver → .com TLD: "What's www.google.com?"
.com TLD → Resolver: "I don't know. Ask ns1.google.com at 216.239.32.10"

Resolver → ns1.google.com: "What's www.google.com?"
ns1.google.com → Resolver: "It's 142.250.68.46" ✅
```

**Who uses iterative queries?**
- Resolver → Root NS → TLD NS → Auth NS (always iterative)

### 5.3 Visual Comparison

```
RECURSIVE (Client → Resolver):          ITERATIVE (Resolver → Each Server):

Client                                  Resolver     Root    TLD     Auth
  │──query──→ Resolver                     │──query──→│        │       │
               │ (handles                   │←─referral─│        │       │
               │  everything)               │──query──────────→ │       │
               │                            │←─referral──────────│       │
  │←─answer──  │                            │──query────────────────────→│
                                            │←─answer───────────────────│
```

### 5.4 Comparison Table

| Feature | Recursive | Iterative |
|---------|-----------|-----------|
| **Who does the work** | Resolver | Resolver (but asking step by step) |
| **Response type** | Complete answer or error | Answer or referral to next server |
| **Load on client** | Low | N/A (resolver handles it) |
| **Load on resolver** | High | High (multiple queries) |
| **Used between** | Client ↔ Resolver | Resolver ↔ Root/TLD/Auth |

> **Key exam point**: Client uses **recursive** to ask Resolver. Resolver uses **iterative** to query Root/TLD/Auth servers.

---

## 6. DNS Caching

### 6.1 Why Caching?

Without caching, every domain lookup would require ~4 queries (Root → TLD → Auth → Resolver). Caching saves time and reduces load on DNS servers.

### 6.2 TTL — Time To Live

Every DNS record has a **TTL** (in seconds) that tells resolvers how long to cache it:

```
$ nslookup google.com
Server: 8.8.8.8
Name:   google.com
Address: 142.250.68.46
TTL: 300  ← cache for 300 seconds (5 minutes)
```

- **Short TTL** (60–300s): Frequent changes (CDNs, failover)
- **Long TTL** (86400s = 1 day): Stable records (rarely change)

### 6.3 Cache Levels

```
Level 1: Browser Cache
  Chrome/Firefox cache DNS results for a short time
  (chrome://net-internals/#dns to inspect)

Level 2: OS Cache
  Operating system maintains its own DNS cache
  (Windows: ipconfig /displaydns; Linux: systemd-resolved)

Level 3: Recursive Resolver Cache
  Your ISP's or Google's resolver caches results
  Serves millions of users → huge cache hit rate

Level 4: Authoritative Server
  Only queried on cache miss — rare for popular domains
```

### 6.4 Cache Invalidation Problem

When a DNS record changes (e.g., you move servers), old cached entries persist until TTL expires:

```
Old IP: 1.2.3.4 (TTL was 1 day = 86400 seconds)
New IP: 5.6.7.8

Timeline:
  T=0:    Change DNS record at authoritative server
  T=0→86400: Users with cached old IP still reach old server!
  T=86400: Cache expires, users get new IP ✅

Solution: Lower TTL BEFORE making the change (give time for propagation)
```

### 6.5 Negative Caching

If a domain **doesn't exist** (NXDOMAIN), resolvers also cache this fact:

```
nslookup thisdoesnotexist12345.com
** server can't find thisdoesnotexist12345.com: NXDOMAIN

This "doesn't exist" result is cached too (per SOA record's negative TTL)
```

---

## 7. DNS Record Types

| Record | Purpose | Example |
|--------|---------|---------|
| **A** | IPv4 address | `google.com → 142.250.68.46` |
| **AAAA** | IPv6 address | `google.com → 2607:f8b0:4004::200e` |
| **CNAME** | Alias/canonical name | `www.google.com → google.com` |
| **MX** | Mail exchange server | `google.com → aspmx.l.google.com` |
| **NS** | Name server for domain | `google.com → ns1.google.com` |
| **TXT** | Text record (SPF, DKIM, domain verification) | `"v=spf1 include:..."` |
| **SOA** | Start of Authority — zone info | Serial, refresh intervals |
| **PTR** | Reverse DNS (IP → name) | `142.250.68.46 → google.com` |
| **SRV** | Service location | Used by SIP, XMPP |

---

## 8. DNS Security

### 8.1 DNS Spoofing / Cache Poisoning

Attacker injects **fake DNS records** into a resolver's cache:

```
Attacker → Resolver: "bank.com = 5.5.5.5 (attacker's server)"
User asks Resolver: "What's bank.com?"
Resolver: "5.5.5.5" (poisoned!) → User connects to fake bank!
```

### 8.2 DNSSEC — DNS Security Extensions

Adds **cryptographic signatures** to DNS records:
- Authoritative servers sign their records
- Resolvers verify signatures
- Prevents cache poisoning

### 8.3 DNS over HTTPS (DoH) / DNS over TLS (DoT)

Traditional DNS queries are **unencrypted** — anyone on the network can see what sites you're visiting:

```
Traditional: Your PC →→ (plaintext DNS) →→ Resolver (ISP can see all!)
DoH:         Your PC →→ (HTTPS encrypted) →→ Resolver (private!)
DoT:         Your PC →→ (TLS encrypted) →→ Resolver (private!)
```

---

## 9. Interview Questions

**Q1: What is DNS and why is it needed?**
> DNS (Domain Name System) translates human-readable domain names (google.com) into machine-readable IP addresses (142.250.68.46). It's needed because humans can't memorize IP addresses for every website, but computers need IPs to establish connections.

**Q2: Explain the DNS resolution process step by step.**
> 1) Browser checks its cache. 2) OS checks its cache. 3) OS asks the Recursive Resolver. 4) Resolver checks its cache; if miss, asks the Root NS. 5) Root NS returns the TLD NS address. 6) Resolver asks TLD NS; it returns the Authoritative NS address. 7) Resolver asks Authoritative NS; gets the IP. 8) Resolver caches and returns IP to the client.

**Q3: What is the difference between recursive and iterative DNS queries?**
> In a recursive query, the client asks the resolver to return a complete answer — the resolver does all the work. In an iterative query, each server returns either the answer or a referral to the next server to ask. Clients use recursive queries to resolvers; resolvers use iterative queries to Root/TLD/Authoritative servers.

**Q4: What is DNS TTL and why does it matter?**
> TTL (Time To Live) is the duration in seconds that a DNS record can be cached by resolvers. Shorter TTLs mean changes propagate faster but increase DNS query load. Longer TTLs reduce load but delay propagation of changes.

**Q5: What is a DNS A record vs CNAME record?**
> An A record maps a domain directly to an IPv4 address. A CNAME record is an alias that points one domain name to another domain name (not an IP). CNAME records add an extra lookup but allow multiple domains to point to the same destination, making it easy to update.

**Q6: What is DNS cache poisoning?**
> An attacker injects fake DNS records into a resolver's cache, redirecting users to malicious servers. For example, poisoning the record for `bank.com` to point to a phishing site. DNSSEC prevents this by cryptographically signing DNS records.

**Q7: How many root name servers are there?**
> There are **13 sets** of root name servers (labeled A through M), but physically there are hundreds of servers distributed worldwide using anycast routing. Each "root server" is actually a cluster of servers.

**Q8: What is the difference between an authoritative and recursive DNS server?**
> An authoritative server is the definitive source for a domain's DNS records — it has the final answer. A recursive resolver is the intermediary that queries multiple authoritative servers on behalf of a client and caches results. When you query 8.8.8.8 (Google DNS), you're querying a recursive resolver.

---

*Next: [02 — HTTP & HTTPS →](./02_HTTP_HTTPS.md)*
