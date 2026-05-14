#!/usr/bin/env python3
import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
from datetime import datetime
import hashlib

TARGET_URL = os.environ.get('TARGET_URL', 'https://www.wikipedia.org')
DOCS_DIR = 'docs'
ASSETS_DIR = f'{DOCS_DIR}/assets'

def setup_dirs():
    os.makedirs(DOCS_DIR, exist_ok=True)
    os.makedirs(ASSETS_DIR, exist_ok=True)
    os.makedirs(f'{ASSETS_DIR}/css', exist_ok=True)
    os.makedirs(f'{ASSETS_DIR}/js', exist_ok=True)
    os.makedirs(f'{ASSETS_DIR}/img', exist_ok=True)

def fetch_url(url, binary=False):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }
    try:
        response = requests.get(url, headers=headers, timeout=30, allow_redirects=True)
        response.raise_for_status()
        return response.content if binary else response.text
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
        return None

def download_asset(url, asset_type):
    """دانلود و ذخیره CSS, JS, Images"""
    try:
        content = fetch_url(url, binary=True)
        if not content:
            return None
        
        # ساخت نام فایل یونیک
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        ext = url.split('.')[-1].split('?')[0][:4]
        filename = f"{url_hash}.{ext}"
        
        filepath = f"{ASSETS_DIR}/{asset_type}/{filename}"
        with open(filepath, 'wb') as f:
            f.write(content)
        
        return f"assets/{asset_type}/{filename}"
    except Exception as e:
        print(f"⚠️  Failed to download {url}: {e}")
        return None

def process_html(html, base_url):
    """پردازش HTML و دانلود منابع"""
    soup = BeautifulSoup(html, 'lxml')
    
    # دانلود CSS
    for link in soup.find_all('link', rel='stylesheet'):
        if link.get('href'):
            css_url = urljoin(base_url, link['href'])
            local_path = download_asset(css_url, 'css')
            if local_path:
                link['href'] = local_path
    
    # دانلود JS
    for script in soup.find_all('script', src=True):
        js_url = urljoin(base_url, script['src'])
        local_path = download_asset(js_url, 'js')
        if local_path:
            script['src'] = local_path
    
    # دانلود تصاویر
    for img in soup.find_all('img', src=True):
        img_url = urljoin(base_url, img['src'])
        local_path = download_asset(img_url, 'img')
        if local_path:
            img['src'] = local_path
    
    # حذف لینک‌های خارجی (اختیاری)
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('http') and not href.startswith(base_url):
            a['href'] = '#'
            a['title'] = f"External link: {href}"
    
    return str(soup)

def save_metadata(url, status):
    """ذخیره اطلاعات fetch"""
    metadata = {
        'url': url,
        'timestamp': datetime.now().isoformat(),
        'status': status
    }
    
    # خواندن تاریخچه
    history_file = f'{DOCS_DIR}/history.json'
    history = []
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            history = json.load(f)
    
    history.insert(0, metadata)
    history = history[:50]  # نگه‌داری 50 رکورد آخر
    
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=2)

def main():
    print(f"🎯 Target: {TARGET_URL}")
    setup_dirs()
    
    html = fetch_url(TARGET_URL)
    if not html:
        save_metadata(TARGET_URL, 'failed')
        sys.exit(1)
    
    print("🔧 Processing HTML...")
    processed = process_html(html, TARGET_URL)
    
    with open(f'{DOCS_DIR}/content.html', 'w', encoding='utf-8') as f:
        f.write(processed)
    
    save_metadata(TARGET_URL, 'success')
    print("✅ Done!")

if __name__ == '__main__':
    main()
