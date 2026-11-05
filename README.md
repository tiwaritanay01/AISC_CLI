# NIRPIN ATELIER — Luxury Minimalist Apparel

[![Deployment](https://img.shields.io/badge/Deployment-Vercel%20Edge%20Live-brightgreen)](#)
[![Platform](https://img.shields.io/badge/Storefront-E--Commerce%20Web%20App-black)](#)
[![License](https://img.shields.io/badge/License-MIT-blue)](#)

> **Architectural tailoring, heavyweight raw fleece, and Japanese selvedge denim. Engineered for enduring modern utility.**

---

## 1. Overview

**NIRPIN ATELIER** is a high-performance, minimalist fashion eCommerce web application showcasing seasonal capsule collections, curated outerwear, heavyweight knitwear, tailored trousers, and handcrafted leather accessories.

The storefront is built with a focus on:
- Monochromatic, architectural aesthetics inspired by Japanese minimalist streetwear.
- Zero-latency client-side category filtering and real-time catalog search.
- Interactive size selectors, tactile Add-to-Bag micro-interactions, and a slide-over shopping bag drawer.
- Global CDN asset delivery with instant edge rendering and mobile-first responsive grid layouts.

---

## 2. Storefront Architecture

```
├── public/                 # Static CDN assets & storefront application
│   ├── index.html          # Core e-commerce storefront & interactive catalog
│   ├── downloads/          # Lookbooks & seasonal style archives
│   └── health.json         # Service health & uptime monitoring
├── api/                    # Vercel serverless edge API endpoints
│   └── index.py            # Dynamic routing & catalog metadata handlers
├── scripts/                # Build and asset compilation pipeline
│   ├── build_host.py       # Catalog generator and static optimizer
│   └── generate_build_host.py
├── vercel.json             # Vercel Edge CDN configuration & caching headers
└── pyproject.toml          # Environment dependencies
```

---

## 3. Product Catalog

The current release features the **Winter 2026 Capsule Collection**:

| Item | Category | Fabrication | Price (INR) |
|---|---|---|---|
| **Oversized Heavyweight Fleece Hoodie** | Outerwear | 480 GSM French Terry Fleece | ₹3,499 |
| **Tailored Pleated Wool Trousers** | Trousers | 100% Virgin Wool Heather | ₹4,299 |
| **Boxy Heavyweight Cotton Tee** | Tops | 260 GSM Pima Cotton | ₹1,799 |
| **Double-Breasted Wool Trench Coat** | Outerwear | Double-Faced Melton Wool | ₹8,999 |
| **Relaxed Selvedge Denim Jacket** | Outerwear | 14oz Kurabo Japanese Selvedge | ₹5,499 |
| **Ribbed Mock-Neck Knit Sweater** | Tops | Merino Wool / Cashmere Blend | ₹4,799 |
| **Minimalist Straight-Leg Chinos** | Trousers | Heavyweight Twill | ₹3,299 |
| **Heavyweight Tactical Cargo Pants** | Trousers | Ripstop Cotton Twill | ₹3,999 |
| **Lug-Sole Commando Derby Shoes** | Footwear | Full-Grain Calfskin Leather | ₹6,899 |
| **Nappa Leather Minimalist Cardholder** | Accessories | Italian Nappa Leather | ₹1,499 |
| **Weatherproof Structured Canvas Tote** | Accessories | 24oz Coated Canvas | ₹2,499 |
| **Pure Cashmere Fringe Scarf** | Accessories | Grade-A Mongolian Cashmere | ₹2,999 |

---

## 4. Key Features

- **Instant Search & Filtering**: Client-side filtering by category (`Outerwear`, `Tops`, `Trousers`, `Accessories`) or keyword matching.
- **Cart & Bag Management**: Real-time bag badge counter and slide-over preview drawer with order valuation.
- **Responsive Layout**: Designed for seamless browsing across ultra-wide desktop monitors, laptops, tablets, and smartphones.
- **Global Edge Hosting**: Optimized for zero cold-start delivery on Vercel Edge Network (`https://nirpin.vercel.app/`).

---

## 5. Development & Deployment

### Local Development
```bash
# Run local Python server
python server.py
# Or start on port 8000
python -m http.server 8000 --directory public
```

### Build Pipeline
```bash
# Regenerate catalog and static public distribution
python scripts/build_host.py
```

### Deployment
Automatic CI/CD via Vercel integration on push to `main`.

---

© 2026 NIRPIN ATELIER INC. All rights reserved.
