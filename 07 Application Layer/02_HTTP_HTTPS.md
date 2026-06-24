#   HTTP & HTTPS

> **HTTP** is the foundation of all data exchange on the Web. Understanding it deeply is essential for any software/networking interview.

---

## 1. What is HTTP?

**HTTP (HyperText Transfer Protocol)** is an **application-layer protocol** used for transmitting hypermedia documents (HTML, JSON, images, etc.) between a client (browser) and a server.

```
Client (Browser)                       Server (Web Server)
      │                                       │
      │──── HTTP Request (GET /index.html) ──→│
      │                                       │
      │←─── HTTP Response (200 OK + HTML) ────│
      │                                       │
```

**Key facts:**
- Runs on top of **TCP** (port 80 for HTTP, port 443 for HTTPS)
- **Stateless** — each request is independent
- Text-based (human-readable)
- Client-server model

---

## 2. Stateless Nature of HTTP

### 2.1 What Does "Stateless" Mean?

HTTP is **stateless** — the server **does not remember** anything about previous requests. Each HTTP request is completely independent.

```
Request 1: "Hi, I'm user John. Show me my cart."
Server: "OK, here's John's cart." → (forgets John)

Request 2: "Add an item to my cart."
Server: "Who are you? I don't remember you!" ← Stateless!
```

### 2.2 Why Stateless?

| Advantage | Explanation |
|-----------|-------------|
| **Scalability** | Any server can handle any request — no session affinity needed |
| **Simplicity** | Server doesn't store per-client state |
| **Reliability** | Server crash doesn't lose client state |

### 2.3 How State is Added (Workarounds)

Since HTTP is stateless, applications use **cookies, sessions, and tokens** to simulate state:

```
Stateless HTTP                     State Added via Cookies
──────────────────────────────     ──────────────────────────────────
Request 1: (no identity)           Request 1: (no cookie) → Login
Server: "Who are you?"             Server: "Here's a cookie: sessionID=abc"

Request 2: (no identity)           Request 2: Cookie: sessionID=abc
Server: "Still don't know you"     Server: "Welcome back, John!" ✅
```

---

## 3. HTTP Request Structure

```
GET /api/users?id=42 HTTP/1.1          ← Request Line (Method + URL + Version)
Host: api.example.com                  ← Headers (key: value)
Accept: application/json
Authorization: Bearer eyJhbGci...
User-Agent: Mozilla/5.0
Connection: keep-alive
                                       ← Empty line (separates headers from body)
{                                      ← Request Body (optional, for POST/PUT)
  "name": "John"
}
```

### HTTP Request Components

| Part | Description | Example |
|------|-------------|---------|
| **Method** | Action to perform | `GET`, `POST`, `PUT`, `DELETE` |
| **URL/Path** | Resource location | `/api/users?id=42` |
| **HTTP Version** | Protocol version | `HTTP/1.1`, `HTTP/2` |
| **Headers** | Metadata | `Content-Type: application/json` |
| **Body** | Data payload (optional) | JSON, form data |

---

## 4. HTTP Methods

### 4.1 The Core Methods

| Method | Purpose | Has Body | Idempotent | Safe |
|--------|---------|----------|-----------|------|
| **GET** | Retrieve a resource | ❌ No | ✅ Yes | ✅ Yes |
| **POST** | Create a new resource | ✅ Yes | ❌ No | ❌ No |
| **PUT** | Replace entire resource | ✅ Yes | ✅ Yes | ❌ No |
| **PATCH** | Partially update resource | ✅ Yes | ❌ No | ❌ No |
| **DELETE** | Remove a resource | ❌ No | ✅ Yes | ❌ No |
| **HEAD** | GET without response body | ❌ No | ✅ Yes | ✅ Yes |
| **OPTIONS** | What methods are allowed? | ❌ No | ✅ Yes | ✅ Yes |

> **Idempotent**: Making the same request multiple times produces the same result (no side effects from repeating).
> **Safe**: The request does NOT modify any server state (read-only).

### 4.2 GET — Retrieve Data

```
GET /api/products/123 HTTP/1.1
Host: shop.example.com

→ Retrieves product with ID 123
→ Data passed in URL (query params), NOT in body
→ Can be cached, bookmarked
→ Should never change server state
```

**Example:**
```
GET /search?q=laptop&page=2&sort=price HTTP/1.1
```

### 4.3 POST — Create Data

```
POST /api/users HTTP/1.1
Host: api.example.com
Content-Type: application/json

{
  "name": "Alice",
  "email": "alice@example.com"
}

→ Creates a new user
→ Data sent in REQUEST BODY (not URL)
→ NOT idempotent: calling twice creates two users!
→ Not cached
```

### 4.4 PUT — Replace (Full Update)

```
PUT /api/users/42 HTTP/1.1
Content-Type: application/json

{
  "name": "Alice Updated",
  "email": "alice.new@example.com",
  "age": 30
}

→ Replaces the ENTIRE user resource
→ Must send ALL fields (missing fields = deleted)
→ Idempotent: same request = same result
```

### 4.5 DELETE — Remove Data

```
DELETE /api/users/42 HTTP/1.1
Host: api.example.com

→ Deletes user 42
→ Idempotent: deleting twice → same result (already gone)
```

### 4.6 GET vs POST — Key Differences

| Feature | GET | POST |
|---------|-----|------|
| **Data location** | URL (query string) | Request body |
| **Data visibility** | Visible in URL, browser history | Hidden in body |
| **Caching** | ✅ Can be cached | ❌ Not cached |
| **Bookmarkable** | ✅ Yes | ❌ No |
| **Data size limit** | ~2000 chars (URL limit) | No practical limit |
| **Use case** | Fetching, searching | Form submission, creating |
| **Idempotent** | ✅ Yes | ❌ No |

---

## 5. HTTP Response Structure

```
HTTP/1.1 200 OK                        ← Status Line (Version + Code + Reason)
Content-Type: application/json         ← Response Headers
Content-Length: 256
Cache-Control: max-age=3600
Date: Sat, 21 Jun 2025 10:21:25 GMT
                                       ← Empty line
{                                      ← Response Body
  "id": 42,
  "name": "Alice",
  "email": "alice@example.com"
}
```

---

## 6. HTTP Status Codes

Status codes are **3-digit numbers** grouped by their first digit:

| Range | Category | Meaning |
|-------|----------|---------|
| **1xx** | Informational | Request received, processing... |
| **2xx** | Success | Request successfully processed |
| **3xx** | Redirection | Client must take further action |
| **4xx** | Client Error | Client made a bad request |
| **5xx** | Server Error | Server failed to process a valid request |

### 6.1 Common Status Codes (Must Know!)

#### 2xx — Success
| Code | Name | Meaning |
|------|------|---------|
| **200** | OK | Request succeeded, response body contains result |
| **201** | Created | Resource successfully created (after POST) |
| **204** | No Content | Success, but no body to return (after DELETE) |

#### 3xx — Redirection
| Code | Name | Meaning |
|------|------|---------|
| **301** | Moved Permanently | Resource moved to new URL (cache this redirect) |
| **302** | Found | Temporary redirect (don't cache) |
| **304** | Not Modified | Cached version is still valid (no need to re-download) |

#### 4xx — Client Errors
| Code | Name | Meaning |
|------|------|---------|
| **400** | Bad Request | Malformed syntax, invalid request |
| **401** | Unauthorized | Not authenticated (no/invalid credentials) |
| **403** | Forbidden | Authenticated but not authorized |
| **404** | Not Found | Resource doesn't exist at this URL |
| **405** | Method Not Allowed | Method not supported for this resource |
| **408** | Request Timeout | Server waited too long for request |
| **429** | Too Many Requests | Rate limit exceeded |

#### 5xx — Server Errors
| Code | Name | Meaning |
|------|------|---------|
| **500** | Internal Server Error | Generic server-side error |
| **502** | Bad Gateway | Upstream server returned invalid response |
| **503** | Service Unavailable | Server overloaded or under maintenance |
| **504** | Gateway Timeout | Upstream server didn't respond in time |

### 6.2 401 vs 403 — Classic Interview Question

```
401 Unauthorized:
  "Who are you? Please log in first."
  Server doesn't know your identity.
  → Include an Authorization header and try again.

403 Forbidden:
  "I know who you are, but you're not allowed here."
  Server knows your identity but denies access.
  → Logging in again won't help.
```

---

## 7. HTTP Versions

| Version | Year | Key Feature |
|---------|------|-------------|
| **HTTP/0.9** | 1991 | Only GET, HTML only |
| **HTTP/1.0** | 1996 | Headers, status codes, one request per connection |
| **HTTP/1.1** | 1997 | **Persistent connections**, pipelining, chunked transfer |
| **HTTP/2** | 2015 | **Multiplexing**, header compression, server push, binary |
| **HTTP/3** | 2022 | **QUIC over UDP**, built-in encryption, faster handshake |

### HTTP/1.1 Persistent Connections
```
HTTP/1.0: Open connection → Request → Response → CLOSE → Open again for next...
HTTP/1.1: Open connection → Request → Response → Request → Response → (reuse!)
                                                            ↑ Connection: keep-alive
```

### HTTP/2 Multiplexing
```
HTTP/1.1: Req1 → Resp1 → Req2 → Resp2 → Req3 → Resp3 (sequential)
HTTP/2:   Req1 ──┐
          Req2 ──┼──→ Server processes all, responds in parallel
          Req3 ──┘
          ← Resp2 ← Resp1 ← Resp3 (out of order, interleaved!)
```

---

## 8. HTTP vs HTTPS

### 8.1 The Problem with HTTP

HTTP sends data in **plain text** — anyone between client and server can read it:

```
HTTP:
You → (Username: alice, Password: mypassword123) → Server
                        ↑
               Attacker reads this! (Man-in-the-Middle)
```

### 8.2 HTTPS — HTTP Secure

**HTTPS = HTTP + TLS (Transport Layer Security)**

TLS provides:
1. **Encryption** — data is unreadable to eavesdroppers
2. **Authentication** — proves you're talking to the real server (not an impostor)
3. **Integrity** — detects if data was tampered with in transit

```
HTTPS:
You → (🔒 encrypted gibberish) → Server
                        ↑
               Attacker sees gibberish, can't read!
```

### 8.3 TLS Handshake — How HTTPS Works

```
Client                                    Server
  │                                          │
  │── ClientHello ──────────────────────────→│
  │   (TLS version, cipher suites, random)   │
  │                                          │
  │←─ ServerHello ────────────────────────── │
  │   (chosen cipher, server random,         │
  │    server's SSL CERTIFICATE)             │
  │                                          │
  │ [Client verifies certificate with CA]    │
  │                                          │
  │── Client Key Exchange ─────────────────→ │
  │   (pre-master secret, encrypted with     │
  │    server's public key)                  │
  │                                          │
  [Both derive session keys from pre-master + randoms]
  │                                          │
  │── ChangeCipherSpec + Finished ─────────→ │
  │←─ ChangeCipherSpec + Finished ────────── │
  │                                          │
  │════ Encrypted HTTP data ════════════════ │  ← Secure tunnel established!
```

### 8.4 SSL Certificates

A **digital certificate** proves a server is who it claims to be:

```
Certificate contains:
  - Domain name (google.com)
  - Public key
  - Issuer (Certificate Authority: DigiCert, Let's Encrypt, etc.)
  - Validity period (expiry date)
  - Digital signature of the CA
```

**Certificate Chain:**
```
Root CA (trusted by OS/browser)
  └── Intermediate CA
        └── Server Certificate (google.com)

Browser trusts Root CA → trusts Intermediate CA → trusts Server
```

### 8.5 HTTP vs HTTPS Comparison

| Feature | HTTP | HTTPS |
|---------|------|-------|
| **Port** | 80 | **443** |
| **Encryption** | ❌ None (plain text) | ✅ TLS/SSL |
| **Authentication** | ❌ No server verification | ✅ Certificate-based |
| **Integrity** | ❌ Data can be tampered | ✅ Tamper-evident |
| **Speed** | Slightly faster | Slightly slower (TLS overhead) |
| **SEO** | Lower ranking | Google prefers HTTPS |
| **Browser indicator** | ⚠️ "Not Secure" | 🔒 Padlock icon |
| **Use case** | Static, public content | Anything sensitive |

---

## 9. Cookies vs Sessions

Both are used to **maintain state** across stateless HTTP requests.

### 9.1 Cookies

A **cookie** is a small piece of data the server sends to the browser, which the browser stores and sends back with every subsequent request.

```
Server → Browser: "Set-Cookie: userId=42; Expires=Thu, 01 Jan 2026; Path=/"
Browser stores this cookie.

Next request:
Browser → Server: "Cookie: userId=42"
Server: "Oh, it's user 42!" ✅
```

**Cookie Attributes:**

| Attribute | Purpose |
|-----------|---------|
| `Name=Value` | The actual data |
| `Expires` / `Max-Age` | When the cookie expires |
| `Domain` | Which domain gets this cookie |
| `Path` | Which paths get this cookie |
| `Secure` | Only send over HTTPS |
| `HttpOnly` | JS cannot access it (prevents XSS theft) |
| `SameSite` | Controls cross-site sending (CSRF protection) |

**Types of Cookies:**
| Type | Description |
|------|-------------|
| **Session cookie** | No expiry — deleted when browser closes |
| **Persistent cookie** | Has expiry — survives browser restarts |
| **Secure cookie** | Sent only over HTTPS |
| **HttpOnly cookie** | Not accessible by JavaScript |
| **Third-party cookie** | Set by a different domain (ads tracking) |

### 9.2 Sessions

A **server-side session** stores user data on the server; the client only holds a **session ID** (usually in a cookie).

```
Step 1: User logs in
  Server creates session: { sessionID: "abc123", userId: 42, role: "admin" }
  Server stores this in memory/DB
  Server sends: "Set-Cookie: sessionID=abc123"

Step 2: Subsequent requests
  Browser sends: "Cookie: sessionID=abc123"
  Server looks up session by ID → finds { userId: 42, role: "admin" }
  Server knows who the user is ✅
```

### 9.3 Cookies vs Sessions Comparison

| Feature | Cookies | Sessions |
|---------|---------|---------|
| **Storage location** | **Client** (browser) | **Server** (memory/DB) |
| **Data size** | Small (4KB max) | No practical limit |
| **Security** | Less secure (data exposed) | More secure (data on server) |
| **Expiry** | Set by server | Managed by server |
| **Performance** | Fast (no server lookup) | Requires DB/cache lookup |
| **Scalability** | Easy (stateless) | Harder (needs shared session store) |
| **Sensitive data** | ⚠️ Avoid (use HttpOnly at minimum) | ✅ Safe to store |

### 9.4 Modern Alternative: JWT (JSON Web Token)

```
JWT = Header.Payload.Signature (all base64 encoded)

Header: { "alg": "HS256", "typ": "JWT" }
Payload: { "userId": 42, "role": "admin", "exp": 1735689600 }
Signature: HMAC-SHA256(header.payload, secret_key)

Client stores JWT (in localStorage or cookie).
Server verifies signature — no DB lookup needed! (Stateless auth)
```

---

## 10. Important HTTP Headers

### Request Headers
| Header | Purpose | Example |
|--------|---------|---------|
| `Host` | Target server | `Host: www.google.com` |
| `Authorization` | Auth credentials | `Authorization: Bearer <token>` |
| `Content-Type` | Body format | `Content-Type: application/json` |
| `Accept` | Expected response format | `Accept: text/html` |
| `Cookie` | Send stored cookies | `Cookie: sessionID=abc` |
| `User-Agent` | Client software info | `User-Agent: Mozilla/5.0` |
| `Cache-Control` | Caching directives | `Cache-Control: no-cache` |

### Response Headers
| Header | Purpose | Example |
|--------|---------|---------|
| `Content-Type` | Response body format | `Content-Type: application/json` |
| `Set-Cookie` | Set a cookie | `Set-Cookie: id=42; HttpOnly` |
| `Cache-Control` | How to cache response | `Cache-Control: max-age=3600` |
| `Location` | Redirect destination | `Location: /new-page` |
| `Access-Control-Allow-Origin` | CORS header | `Access-Control-Allow-Origin: *` |

---

## 11. Interview Questions

**Q1: What does "stateless" mean in HTTP?**
> HTTP is stateless — the server does not retain any information about previous requests. Each request is completely independent. The server cannot recognize the same client across two separate requests unless additional mechanisms like cookies, sessions, or tokens are used.

**Q2: What is the difference between GET and POST?**
> GET retrieves data — parameters go in the URL, it's cached, idempotent, and should not change server state. POST submits data — payload goes in the request body, it's not cached, not idempotent (two calls may create two resources), and is used for creating/submitting data.

**Q3: What is the difference between 401 and 403?**
> 401 Unauthorized means the client is NOT authenticated — "who are you? please log in." 403 Forbidden means the client IS authenticated but NOT authorized — "I know who you are, but you don't have permission."

**Q4: What is the difference between HTTP and HTTPS?**
> HTTP transmits data in plain text — vulnerable to eavesdropping and tampering. HTTPS adds TLS encryption, server authentication via certificates, and integrity checking. HTTPS operates on port 443; HTTP on port 80.

**Q5: What is the difference between cookies and sessions?**
> Cookies store data on the client (browser) — small, portable but exposed. Sessions store data on the server; the client only holds a session ID (usually in a cookie). Sessions are more secure for sensitive data but require server-side storage and management.

**Q6: What is the TLS handshake?**
> TLS handshake establishes a secure connection: 1) Client sends supported cipher suites. 2) Server responds with chosen cipher and its certificate. 3) Client verifies certificate. 4) Client sends encrypted pre-master secret. 5) Both derive session keys. 6) Both confirm and start encrypted communication.

**Q7: What is CORS?**
> Cross-Origin Resource Sharing — a browser security policy preventing scripts from one origin making requests to another origin. Browsers send an `Origin` header; servers respond with `Access-Control-Allow-Origin` to permit or deny the request.

**Q8: What are idempotent HTTP methods?**
> An operation is idempotent if repeating it produces the same result. GET, PUT, DELETE, HEAD, OPTIONS are idempotent. POST and PATCH are NOT (multiple POST requests may create multiple resources).

---

*Next: [03 — Other Protocols (FTP, SMTP, DHCP) →](./03_Other_Protocols.md)*
