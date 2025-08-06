# 🛡️ XSS Tools – Automated XSS Scanner & Exploit Generator

**XSS Tools** is a terminal-based Python toolkit designed to detect XSS (Cross-Site Scripting) vulnerabilities and automatically generate context-aware JavaScript exploit scripts. It features a modular architecture for easy expansion and customization.

---

## 🚀 Features

- 🔍 Detect reflected XSS vulnerabilities in URL parameters
- 🧠 Context-aware scanning: supports `<script>`, HTML, and attribute injection
- ⚙️ Generates ready-to-use JavaScript exploits based on detected contexts
- 🪓 Organized, extensible architecture (for stored, DOM, and POST-based XSS)
- 📊 Clean terminal output powered by `tabulate`

---

## 📁 Project Structure

```
xsstools/
├── main.py             # Main terminal interface & result display
├── scanner.py          # Core scanner & context detection logic
├── xss_script/         # JavaScript exploit templates
│   ├── xss_stored.js   # Stored XSS script template
│   ├── xss_based.js    # Reflected XSS script template
│   └── xss_dom.js      # DOM-based XSS script template
```

---

## 🧑‍💻 Usage

1. **Install dependencies** (Python 3 required):
    ```bash
    pip install requests tabulate
    ```

2. **Run the tool**:
    ```bash
    python tampilan.py
    ```

3. **Enter a target URL with parameters**:
    ```
    https://example.com/page.php?query=test
    ```

### 📜 Sample Output

```
🛡️  XSS Toolkit by Kyra
==================================================
Enter target URL (example: https://site.com/page?name=halo): https://victim.com/?q=test

📊 Scan Results:
╒════════╤═════════════╤════════════════════╕
│ Param  │ Vulnerable  │ Context            │
╞════════╪═════════════╪════════════════════╡
│ q      │ True        │ Inside HTML        │
╘════════╧═════════════╧════════════════════╛

🚨 Parameter 'q' detected as VULNERABLE!
🧠 Context: Inside HTML
📜 Recommended Script:
document.write("<h1>XSS Detected</h1>");
```

---

## 🧠 How It Works

- The tool injects a basic XSS test payload into each parameter of the target URL.
- It analyzes the server's response to determine if the payload is reflected.
- Detects the context (e.g., script block, attribute, or raw HTML) where the payload appears.
- Recommends a matching JavaScript exploit based on the detected context using pre-built templates.

### 📂 Exploit Templates

Located in the `xss_script/` folder, each `.js` file contains a sample exploit:
- **xss_stored.js** – Injected content that persists on page load (stored XSS)
- **xss_based.js** – Reflected payloads (e.g., `alert(document.cookie)`)
- **xss_dom.js** – DOM-based XSS exploits (e.g., using `document.write` or URL fragments)

---

## ⚠️ Disclaimer

This tool is intended for educational and authorized security testing purposes only.
**Do NOT use it on targets without explicit permission.**

---

## 📌 Author

Created with dedication and precision by Kyra —
Developer and cyber explorer with a mission to master data and decode the matrix.

---

## 💡 Future Plans

- Support for POST-based XSS scanning
- Stored XSS detection via crawling
- Auto report generation (.html / .json)
- Web UI version (Flask or FastAPI)
