# 🛡️ XSS Tools – Automated XSS Scanner & Exploit Generator

**XSS Tools** is a terminal-based Python toolkit designed to detect XSS (Cross-Site Scripting) vulnerabilities and automatically generate context-aware JavaScript exploit scripts. Built with modularity and flexibility in mind, it's perfect for penetration testers, bug bounty hunters, and ethical hackers.

---

## 🚀 Features

- 🔍 Detect reflected XSS vulnerabilities in URL parameters
- 🧠 Context-aware scanning: `<script>`, HTML, and attribute injection
- ⚙️ Generates ready-to-use JavaScript exploits
- 🪓 Organized architecture for further expansion (stored/DOM/POST)
- 📊 Clean terminal output using `tabulate`

---

## 📁 Project Structure

xsstools/
├── tampilan.py # Main terminal interface & result display
├── detect.py # Core scanner & context detection logic
├── xss_script/ # JavaScript exploit templates
│ ├── xss_stored.js # Stored XSS script
│ ├── xss_based.js # Reflected XSS script
│ └── xss_dom.js # DOM-based XSS script

yaml
Salin
Edit

---

## 🧑‍💻 Usage

1. 🔧 Install dependencies (Python 3 required):
   ```bash
   pip install requests tabulate
▶️ Run the tool:

bash
Salin
Edit
python tampilan.py
📍 Enter a target URL with parameters:

bash
Salin
Edit
https://example.com/page.php?query=test
📜 Output Example
text
Salin
Edit
🛡️  XSS Toolkit by Kyra
==================================================
Masukkan URL target (contoh: https://site.com/page?name=halo): https://victim.com/?q=test

📊 Hasil Scan:
╒════════╤═════════════╤════════════════════╕
│ Param  │ Vulnerable  │ Context            │
╞════════╪═════════════╪════════════════════╡
│ q      │ True        │ Inside HTML        │
╘════════╧═════════════╧════════════════════╛

🚨 Param 'q' terdeteksi VULNERABLE!
🧠 Konteks: Inside HTML
📜 Script rekomendasi:
document.write("<h1>XSS Detected</h1>");
🧠 How It Works
The tool injects a basic XSS test payload into each parameter.

It analyzes whether the payload is reflected in the response.

Context is detected (script block, attribute, or raw HTML).

Based on the context, a matching JavaScript exploit is suggested using pre-built templates.

📂 Templates
Located in the xss_script/ folder, each .js file contains an example exploit:

xss_stored.js – Injected content that persists on page load

xss_based.js – Reflected payload like alert(document.cookie)

xss_dom.js – DOM-based XSS exploit using document.write or URL fragments

⚠️ Disclaimer
This tool is intended for educational and authorized security testing only.
Do NOT use it on targets without explicit permission.

📌 Author
Created with pain and precision by Kyra —
A developer and cyber explorer with a mission to dominate data and decode the matrix.

💡 Future Plans
 Support for POST-based XSS scanning

 Stored XSS detection via crawling

 Auto report generation (.html / .json)

 Web UI version (Flask or FastAPI)
