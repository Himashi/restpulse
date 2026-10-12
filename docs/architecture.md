# Architecture & Middleware Pipeline

`restpulse` is designed around a modular **middleware pipeline** built on top of `httpx`. Instead of tangling retry logic, security masking, and tracing into a single monolithic client, `restpulse` delegates outgoing requests through a clean, ordered stack of asynchronous middleware components.

## The Execution Pipeline

When an application calls an asynchronous request method (e.g., `client.get_async("/path")`), the request flows sequentially through the middleware layers before hitting the network, and the response flows backward through the stack.

```text
Outgoing Request
             │
             ▼
┌───────────────────────────────────┐
│  1. OpenTelemetry Middleware      │ ──► Injects W3C traceparent headers for distributed APM tracing
└───────────────────────────────────┘
             │
             ▼
┌───────────────────────────────────┐
│  2. Data Masking Middleware       │ ──► Redacts sensitive PII / API keys before transmission
└───────────────────────────────────┘
             │
             ▼
┌───────────────────────────────────┐
│  3. Rate Limiting Middleware      │ ──► Checks sliding-window thresholds; prevents 429 throttling
└───────────────────────────────────┘
             │
             ▼
┌───────────────────────────────────┐
│  4. Circuit Breaker Middleware    │ ──► Short-circuits request if target server is known to be down
└───────────────────────────────────┘
             │
             ▼
┌───────────────────────────────────┐
│  5. Smart Connection Pool         │ ──► Reuses open sockets/connections via keep-alive HTTPX core
└───────────────────────────────────┘
             │
             ▼
      [ Remote API ]
```

## Core Components
**1. OpenTelemetry Middleware (OpenTelemetryMiddleware)**

**Role:** Instruments outbound HTTP requests with OpenTelemetry spans.

**Behavior:** Automatically generates or propagates W3C trace context headers (traceparent and tracestate) to ensure distributed tracing continuity across microservices.

**2. Data Masking Middleware (DataMaskingMiddleware)**

**Role:** Security and compliance enforcement.

**Behavior:** Inspects request payloads, headers, and query parameters using regex pattern matching to scrub sensitive Personally Identifiable Information (PII), API keys, and credentials before they leave the client boundary.

**3. Rate Limiting Middleware (RateLimitMiddleware)**

**Role:** Client-side traffic control.

**Behavior:** Enforces sliding window thresholds to prevent overwhelming downstream services and handles automated delays or Retry-After header parsing.

**4. Circuit Breaker Middleware (CircuitBreakerMiddleware)**

**Role:** Resiliency and fault tolerance.

**Behavior:** Tracks rolling failure rates. If downstream failures cross a configured threshold, the circuit trips to OPEN, failing requests locally to prevent cascading outages and thundering herds.

**5. Smart Connection Pool (ConnectionPoolConfig)**

**Role:** Performance optimization.

**Behavior:** Manages underlying httpx.AsyncClient socket pooling, keep-alive durations, and maximum concurrent connection limits to minimize TCP handshake overhead.