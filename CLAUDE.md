# AI Agent Instructions for `benhauptvogel.de`

Welcome to the codebase for Ben Hauptvogel's personal website. This document outlines the architectural decisions, design system, and scripts used in this project. Please adhere to these guidelines when making any modifications.

## 🏗 Tech Stack & Architecture
- **Zero-Build Static Site:** The website is built using **pure HTML, CSS, and vanilla JavaScript**.
- **No External Assets:** All CSS is contained within `<style>` tags in the `<head>` of each HTML file. All JavaScript is contained within `<script>` tags at the end of the `<body>`. Do not create separate `.css` or `.js` files.
- **Icons:** All icons are inline SVGs. Do not add icon font libraries (like FontAwesome).
- **Pages:**
  - `index.html`: Automatically redirects to `about.html`.
  - `about.html`: The main landing page, containing a short bio, professional experience, publications, education, and links.
  - `projects.html`: A portfolio showcasing projects in a CSS Grid layout with hover interactions.
  - `videos.html`: A video portfolio featuring a dynamic data table and embedded videos.

## 🎨 Design System

### Typography
- Font Family: `'Outfit', sans-serif` (imported from Google Fonts).

### Color Palette (Dark Theme)
- **Background:** `#1a1a1a`
- **Surface (Cards/Containers):** `#242424`
- **Text Primary:** `#eeeeee`
- **Text Secondary:** `#b0b0b0`
- **Accent Color:** `#16a34a` (Dark Green)

### Video Type Badge Colors
The `videos.html` page uses specific colors for different types of videos:
- **Film:** Orange (`#f97316`) / Background `rgba(249, 115, 22, 0.1)`
- **Short Film:** Yellow (`#eab308`) / Background `rgba(234, 179, 8, 0.1)`
- **Video:** Blue (`#3b82f6`) / Background `rgba(59, 130, 246, 0.1)`
- **Short Video:** Violet (`#a855f7`) / Background `rgba(168, 85, 247, 0.1)`

### UI Elements
- **Glassmorphism:** Used for info tooltips and hover overlays (e.g., `backdrop-filter: blur(12px); background-color: rgba(26, 26, 26, 0.95);`).
- **Hover Effects:** Project cards and thumbnails generally scale up slightly (`transform: scale(1.02)` or `scale(1.05)`) with a drop shadow on hover.

## 📊 Data Management (`videos.csv`)
- The data for `videos.html` is dynamically loaded from `videos.csv` using the browser's native `fetch()` API.
- **Columns:** Name, Year, Link, Notes, Type, Featured, Thumbnail.
- If you need to add a new video, edit `videos.csv` and then run the thumbnail script.

## 🛠 Scripts

### `scripts/download_thumbnails.py`
If you add or update YouTube links in `videos.csv`, you **must run this script**.
```bash
python3 scripts/download_thumbnails.py
```
**What it does:**
1. Parses `videos.csv` for YouTube URLs.
2. Extracts the video ID.
3. Downloads the highest resolution thumbnail from YouTube into the `thumbnails/` directory.
4. Uses the `Pillow` library to automatically detect and crop any baked-in black borders from the downloaded thumbnails.
5. Updates the `Thumbnail` column in `videos.csv` with the correct relative path.

*Note: Requires the `Pillow` Python package (`pip install Pillow`).*

## 🚀 Deployment
This website is hosted as a static site on GitHub Pages.
- Pushing changes to the `main` branch on GitHub automatically triggers a deployment.
- Domain: `https://benhauptvogel.de`
- Ensure all relative paths (e.g., to `assets/images/` or `thumbnails/`) remain intact so they load correctly in the production environment.
