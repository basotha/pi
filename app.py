from flask import Flask, send_from_directory, request
import os

app = Flask(__name__, static_folder=".", static_url_path="/")

# ========= ROUTES =========
@app.route("/")
def serve_index():
    return send_from_directory('.', "index.html")

@app.route("/<path:path>")
def serve_file(path):
    # Chặn truy cập file nhạy cảm
    if path.startswith('.') or path in ['app.py', 'requirements.txt']:
        return "Forbidden", 403
    return send_from_directory('.', path)

@app.route("/robots.txt")
def robots():
    return send_from_directory('.', "robots.txt")

@app.route("/sitemap.xml")
def sitemap():
    # Tự động nhận diện domain
    domain = request.host_url.rstrip('/')
    
    try:
        with open('sitemap.xml', 'r', encoding='utf-8') as f:
            sitemap_content = f.read()
    except FileNotFoundError:
        # Fallback sitemap nếu file chưa có
        sitemap_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://piwallet.top/</loc>
    <lastmod>2026-06-08</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>'''
    
    # Thay thế domain động
    sitemap_content = sitemap_content.replace('https://piwallet.top', domain)
    
    return sitemap_content, 200, {'Content-Type': 'application/xml'}

# ========= MAIN =========
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Tool đang chạy tại: http://0.0.0.0:{port}")
    print(f"📱 Truy cập từ máy khác trong cùng mạng: http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)