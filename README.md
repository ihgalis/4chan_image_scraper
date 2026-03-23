# 4chan Image Scraper

A lightweight, high-performance tool built with **Scrapy 2.14+** and **Python 3.14+** to download images from 4chan boards directly to your local machine.

---

## 🚀 Quick Start (with Pixi)

[Pixi](https://pixi.sh) is the recommended way to run this scraper. It handles all dependencies (like Python, Scrapy, and Pillow) in an isolated environment automatically.

1. **Install Pixi**: If you don't have it, follow the [installation guide](https://pixi.sh/#installation).
2. **Start Scraping**:
   ```bash
   pixi run crawl
   ```
3. **Check your files**: Open the `images/full/` folder in your project directory to see the results.

---

## 📂 Where are the images?

By default, Scrapy saves images in a subfolder called `full/` inside the `images/` directory.
- **Path**: `./images/full/`
- **Filenames**: Files are named using a unique SHA-1 hash of their original URL to prevent duplicates.

---

## 🛠️ Customization

You can choose which boards to scrape and how deep the scraper should go by using environment variables in a single command.

### Example: Scrape 1 page from Technology (/g/) and Wallpaper (/wg/)
```bash
BOARDS="g,wg" MAX_PAGES_PER_BOARD=1 pixi run crawl
```
- **BOARDS**: Comma-separated board codes (default: `v,pol`).
- **MAX_PAGES_PER_BOARD**: Number of pages to crawl per board (default: `2`).

---

## 🛡️ Security & Ethics
- **Respectful**: Includes **AutoThrottle** (5s initial delay) and **User-Agent rotation** to avoid putting unnecessary load on 4chan's servers.
- **Integrity**: Uses SHA-256 hashing for internal data tracking.
- **Stealth**: Mimics real browser headers and handles cookies to avoid common bot detection blocks.

---

## 🧪 Development & Testing
To verify the parsing logic:
```bash
pixi run test
```
