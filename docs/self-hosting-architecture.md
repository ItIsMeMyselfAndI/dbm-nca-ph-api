# Architecture: Cloudflare Tunnel Self-Hosting

## 1. The Problem

### ISP Blocks Ports 80/443

Most residential ISPs (including Globe/PLDT in the Philippines) block inbound traffic on ports 80 and 443. This prevents running a standard HTTPS server from home.

Even if they didn't:

- Home routers sit behind **NAT** — one public IP shared among many devices
- You'd need to **forward ports** on the router, and the router's WAN port is what receives the traffic
- The Huawei EG8041X6-10 ONT is both a modem and a router; ISP locks restrict customisation

### Port Forwarding Isn't Enough

Some ISPs use **CGNAT** (Carrier-Grade NAT) where your router doesn't even get a real public IP — it gets a private IP from the ISP's own NAT layer. In that case port forwarding is impossible; you're double-NATed.

Even with a public IP (like this server: `27.49.19.15`), ISP-level firewalls still drop ports 80/443 before they reach your router.

---

## 2. Considered Solutions

| Solution | Result |
|---|---|
| Direct port forwarding (80/443) | Blocked by ISP |
| Tailscale Funnel | Works but routes all traffic through Tailscale's relay; extra latency, single point of failure, and requires users to install Tailscale or trust a non-standard funnel domain |
| Cloudflare Proxy (orange cloud) | Cloudflare proxies on ports 80/443 only unless you pay for Pro ($20/mo) to use a custom origin port |
| **Cloudflare Tunnel (selected)** | `cloudflared` makes a single outbound connection to Cloudflare; zero inbound ports needed. Free tier works. |

---

## 3. How Cloudflare Tunnel Works

```
┌──────────┐   HTTPS    ┌──────────────┐   outbound    ┌───────────┐   localhost    ┌──────────┐
│  Client  │ ────────→  │  Cloudflare  │ ←───tunnel─── │cloudflared│ ────────────→  │  Nginx   │
│ (browser)│            │    Edge      │               │  (daemon)  │               │127.0.0.1:│
└──────────┘            └──────────────┘               └───────────┘               │   8080   │
                                                                                    └────┬─────┘
                                                                                         │ proxy_pass
                                                                                    ┌─────▼─────┐
                                                                                    │  Uvicorn  │
                                                                                    │127.0.0.1: │
                                                                                    │   8000    │
                                                                                    └───────────┘
```

### Step by step:

1. **`cloudflared`** on the server opens an **outbound TCP connection** to Cloudflare's edge (connect.cloudflare.com). This is just a regular HTTPS connection — the ISP sees only an outbound request to Cloudflare, which is never blocked.

2. This connection stays open indefinitely (heartbeat keepalives). It's the **tunnel**.

3. You create a DNS record: `dbm-nca-ph-api.losarim.site → CNAME → <tunnel-id>.cfargotunnel.com`. This tells Cloudflare: "requests for this hostname go through that tunnel."

4. When a browser visits `https://dbm-nca-ph-api.losarim.site`, DNS resolves to Cloudflare's IP (because Cloudflare manages the nameservers). The client sends the HTTPS request to Cloudflare's edge.

5. Cloudflare decrypts the HTTPS (they have the SSL cert), looks up the tunnel for that hostname, and pushes the request **down the already-open tunnel** to your `cloudflared` daemon.

6. `cloudflared` receives the request and matches the hostname against its ingress rules (`/etc/cloudflared/config.yml`). It proxies to `http://127.0.0.1:8080` (Nginx).

7. Nginx receives the request on localhost:8080, reads the `Host` header to match the `server_name`, and proxies to `http://127.0.0.1:8000` (uvicorn).

8. Uvicorn serves the FastAPI response. The response travels back through the same chain.

### Key insight

The tunnel is **outbound**. Your router never receives an unsolicited inbound connection. The ISP's port block on 80/443 is irrelevant because `cloudflared` initiated the connection to Cloudflare, not the other way around.

---

## 4. Why Nginx in Front of Uvicorn?

The tunnel could point directly at uvicorn (`http://127.0.0.1:8000`). We keep Nginx in front for:

- **Rate limiting** — Nginx's `limit_req_zone` blocks abusive clients before they reach the app
- **Header sanitisation** — proxy headers are stripped/set correctly
- **Static files** — if needed, Nginx serves them far more efficiently than Python
- **Multiple apps** — if another service is added later, Nginx can route by hostname or path

---

## 5. SSL / HTTPS

Cloudflare handles SSL **at the edge**. The cert is between the browser and Cloudflare's network. The tunnel itself is encrypted internally (Cloudflare-to-cloudflared). No cert is needed on the server. No Certbot or Let's Encrypt is involved.

---

## 6. Summary

| Requirement | How it's met |
|---|---|
| ISP blocks ports 80/443 | Tunnel uses outbound-only connection; no inbound ports needed |
| Public HTTPS | Cloudflare edge terminates TLS, free SSL cert included |
| No CGNAT issue | Tunnel works even behind CGNAT — outbound connections are always allowed |
| No monthly cost | Cloudflare free plan covers tunnels, DNS, and SSL |
| Simple setup | One daemon (`cloudflared`), one config file, three commands |

---

**Step-by-step instructions:** [`docs/guides/hosting-guide.md`](./guides/hosting-guide.md)
