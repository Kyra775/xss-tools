from scanner import scan_xss
from tabulate import tabulate
import os
import sys
import time
import json
import random

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

def display_banner():
    print(f"\n{PURPLE}{BOLD}")
    print(" ██╗░░██╗██╗░░██╗░██████╗   ████████╗░█████╗░░█████╗░██╗░░░░░")
    print(" ╚██╗██╔╝╚██╗██╔╝██╔════╝   ╚══██╔══╝██╔══██╗██╔══██╗██║░░░░░")
    print(" ░╚███╔╝░░╚███╔╝░╚█████╗░     ░██║░░░██║░░██║██║░░██║██║░░░░░")
    print(" ░██╔██╗░░██╔██╗░░╚═══██╗     ░██║░░░██║░░██║██║░░██║██║░░░░░")
    print(" ██╔╝╚██╗██╔╝╚██╗██████╔╝     ░██║░░░╚█████╔╝╚█████╔╝███████╗")
    print(" ╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝      ╚═╝░░░░╚════╝░░╚════╝░╚══════╝")
    print(f"{RESET}")
    print(f"{CYAN}▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓{RESET}")
    print(f"{BOLD}{BLUE}   ADVANCED XSS SCANNER v4.0 | BY KYRA | 0xSECURITY | ULTIMATE EDITION{RESET}")
    print(f"{CYAN}▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓{RESET}\n")

def display_progress(duration, message="SCANNING"):
    for i in range(101):
        time.sleep(duration / 100)
        width = 50
        filled = int(width * i / 100)
        bar = "█" * filled + "-" * (width - filled)
        sys.stdout.write(f"\r{BLUE}[{BOLD}{message}{RESET}{BLUE}] |{bar}| {i}%")
        sys.stdout.flush()
    print()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def display_menu():
    print(f"\n{BOLD}{CYAN}▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ MAIN MENU ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓{RESET}")
    print(f"{BOLD}{YELLOW}1.{RESET} 🔍 Scan Single URL")
    print(f"{BOLD}{YELLOW}2.{RESET} 📂 Scan Multiple URLs from File")
    print(f"{BOLD}{YELLOW}3.{RESET} ⚙️  Configure Scanner Settings")
    print(f"{BOLD}{YELLOW}4.{RESET} 📜 View Scan History")
    print(f"{BOLD}{YELLOW}5.{RESET} 📘 Help & Documentation")
    print(f"{BOLD}{YELLOW}6.{RESET} 🧪 Generate XSS Test Page")
    print(f"{BOLD}{RED}0.{RESET} 🚪 Exit Program")
    print(f"{BOLD}{CYAN}▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓{RESET}")

def display_results(results, url):
    if not results:
        print(f"\n{YELLOW}⚠️  No parameters found or connection failed!{RESET}")
        return

    table_data = []
    for res in results:
        if res["Vulnerable"] is True:
            status = f"{RED}VULNERABLE{RESET}"
        elif res["Vulnerable"] is False:
            status = f"{GREEN}SAFE{RESET}"
        else:
            status = f"{YELLOW}ERROR{RESET}"
            
        table_data.append({
            "Parameter": f"{CYAN}{res['Param']}{RESET}",
            "Status": status,
            "Context": f"{PURPLE}{res['Context']}{RESET}",
            "Payload": res["Payload"][:50] + "..." if len(res["Payload"]) > 50 else res["Payload"]
        })

    print(f"\n{BOLD}{BLUE}🔍 SCAN RESULTS FOR: {url}{RESET}")
    print(tabulate(table_data, headers="keys", tablefmt="fancy_grid", stralign="left"))

    vuln_count = sum(1 for r in results if r["Vulnerable"] is True)
    safe_count = sum(1 for r in results if r["Vulnerable"] is False)
    error_count = len(results) - vuln_count - safe_count

    print(f"\n{BOLD}{PURPLE}📊 VULNERABILITY SUMMARY{RESET}")
    print(f"{GREEN}✅ Secure Parameters: {safe_count}{RESET}")
    print(f"{RED}🚨 Vulnerable Parameters: {vuln_count}{RESET}")
    print(f"{YELLOW}⚠️  Errors: {error_count}{RESET}")
    
    for res in results:
        if res["Vulnerable"] is True:
            print(f"\n{BOLD}{RED}🚨 CRITICAL: Param '{res['Param']}' is VULNERABLE!{RESET}")
            print(f"{BOLD}🧠 Context Type: {PURPLE}{res['Context'].upper()}{RESET}")
            print(f"{BOLD}📦 Payload: {YELLOW}{res['Payload']}{RESET}")
            print(f"{BOLD}🔧 Recommended Exploit:{RESET}")
            print(get_exploit_script(res["Context"]))

def get_exploit_script(context):
    context_map = {
        "script": "reflected.js",
        "attribute": "dom.js",
        "html": "stored.js",
        "href": "dom.js",
        "svg": "dom.js"
    }
    
    filename = context_map.get(context.lower(), "")
    if not filename:
        return "// No specialized exploit for this context"
    
    try:
        with open(f"xss_script/{filename}", "r") as f:
            return f.read()
    except FileNotFoundError:
        return f"// Script file not found: xss_script/{filename}"
    except Exception as e:
        return f"// Error reading script: {str(e)}"

def scan_single_url():
    try:
        url = input(f"\n{BOLD}🌐 Enter Target URL (e.g., https://example.com?search=test): {RESET}").strip()
        if not url.startswith("http"):
            url = "https://" + url
            
        print(f"\n{BOLD}{YELLOW}🚀 Scanning {url}{RESET}")
        display_progress(3.5, "ANALYZING")
        
        results = scan_xss(url)
        display_results(results, url)
        save_history(url, results)
        
    except Exception as e:
        print(f"\n{RED}❌ Error during scanning: {str(e)}{RESET}")

def scan_from_file():
    try:
        filename = input(f"\n{BOLD}📁 Enter filename with URLs (one per line): {RESET}").strip()
        with open(filename, "r") as f:
            urls = [line.strip() for line in f.readlines() if line.strip()]
        
        print(f"\n{BOLD}{PURPLE}📄 Found {len(urls)} URLs to scan{RESET}")
        
        for i, url in enumerate(urls, 1):
            if not url.startswith("http"):
                url = "https://" + url
                
            print(f"\n{BOLD}{CYAN}[{i}/{len(urls)}] Scanning {url}{RESET}")
            display_progress(1.5, "PROCESSING")
            
            results = scan_xss(url)
            display_results(results, url)
            save_history(url, results)
            
    except Exception as e:
        print(f"\n{RED}❌ File error: {str(e)}{RESET}")

def configure_settings():
    print(f"\n{BOLD}{PURPLE}⚙️  SCANNER CONFIGURATION{RESET}")
    print(f"{BOLD}{YELLOW}This feature is under development...{RESET}")
    print(f"{BOLD}Available in v5.0: Payload customization, timeout settings")
    input(f"\n{BOLD}{CYAN}Press Enter to continue...{RESET}")

def save_history(url, results):
    try:
        history = []
        if os.path.exists("scan_history.json"):
            with open("scan_history.json", "r") as f:
                history = json.load(f)
                
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        vuln_count = sum(1 for r in results if r["Vulnerable"] is True)
        
        history.append({
            "url": url,
            "timestamp": timestamp,
            "vulnerabilities": vuln_count,
            "total_params": len(results)
        })
        
        with open("scan_history.json", "w") as f:
            json.dump(history, f, indent=2)
            
    except Exception:
        pass

def view_history():
    try:
        if not os.path.exists("scan_history.json"):
            print(f"\n{YELLOW}No scan history found{RESET}")
            return
            
        with open("scan_history.json", "r") as f:
            history = json.load(f)
            
        if not history:
            print(f"\n{YELLOW}No scan history found{RESET}")
            return
            
        print(f"\n{BOLD}{PURPLE}📜 SCAN HISTORY{RESET}")
        for i, entry in enumerate(history, 1):
            print(f"\n{BOLD}{CYAN}{i}. {entry['timestamp']}{RESET}")
            print(f"URL: {entry['url']}")
            print(f"Parameters: {entry['total_params']} | Vulnerabilities: {entry['vulnerabilities']}")
            
    except Exception as e:
        print(f"\n{RED}Error loading history: {str(e)}{RESET}")

def show_documentation():
    clear_screen()
    display_banner()
    print(f"{BOLD}{YELLOW}\n📘 XSS SCANNER DOCUMENTATION{RESET}")
    print(f"{BOLD}{CYAN}\n▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓{RESET}")
    print(f"{BOLD}🔍 What This Tool Detects:{RESET}")
    print("  - Reflected XSS in URL parameters")
    print("  - DOM-based XSS vulnerabilities")
    print("  - HTML attribute injection")
    print("  - JavaScript URI schemes")
    print("  - SVG vector attacks")
    print("  - Template injection flaws")
    
    print(f"\n{BOLD}⚙️ Technical Features:{RESET}")
    print("  - 7 different payload types")
    print("  - Context-aware detection")
    print("  - WAF bypass techniques")
    print("  - Token-based verification")
    print("  - Automated exploit generation")
    
    print(f"\n{BOLD}🚀 Usage Tips:{RESET}")
    print("  1. Always test on authorized systems")
    print("  2. Use HTTPS URLs for best results")
    print("  3. Include query parameters in URLs")
    print("  4. Review recommendations carefully")
    
    print(f"\n{BOLD}⚠️ Legal Disclaimer:{RESET}")
    print("  This tool is for educational and")
    print("  authorized testing only. Never use")
    print("  for illegal activities.")
    print(f"{BOLD}{CYAN}▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓{RESET}")
    input(f"\n{BOLD}{CYAN}Press Enter to return to menu...{RESET}")

def generate_test_page():
    try:
        filename = input(f"\n{BOLD}📝 Enter filename to save test page (e.g., test.html): {RESET}").strip()
        if not filename.endswith(".html"):
            filename += ".html"
            
        page_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>XSS Test Page</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; }}
        .vuln {{ color: red; font-weight: bold; }}
        .safe {{ color: green; }}
    </style>
</head>
<body>
    <h1>XSS Vulnerability Test Page</h1>
    <p>This page contains intentional XSS vulnerabilities for testing purposes</p>
    
    <h2>Reflected XSS Tests:</h2>
    <ul>
        <li><a href="?test=injection">Script Context</a></li>
        <li><a href="?attr=injection">Attribute Context</a></li>
        <li><a href="?html=injection">HTML Context</a></li>
    </ul>
    
    <h2>DOM XSS Tests:</h2>
    <div id="dom-output"></div>
    <script>
        const query = new URLSearchParams(window.location.search);
        document.getElementById('dom-output').innerHTML = 
            "DOM Output: " + query.get('dom');
    </script>
    
    <h2>Sample Vulnerable Outputs:</h2>
    <p>Script: <script>document.write(new URLSearchParams(window.location.search).get('test'))</script></p>
    <p>Attribute: <div id="test" data-value="{random.choice(['safe', 'vulnerable'])}"></div></p>
    <p>HTML: <div>{random.choice(['<b>safe</b>', '<img src=x onerror=alert(1)>'])}</div></p>
    
    <footer>
        <p>Generated by XSS Toolkit {time.strftime("%Y-%m-%d")}</p>
    </footer>
</body>
</html>"""
        
        with open(filename, "w") as f:
            f.write(page_content)
            
        print(f"\n{GREEN}✅ Test page generated successfully: {filename}{RESET}")
        print(f"{YELLOW}⚠️ Open this file in a browser and test with various payloads{RESET}")
        
    except Exception as e:
        print(f"\n{RED}❌ Error generating test page: {str(e)}{RESET}")

def main():
    clear_screen()
    display_banner()
    
    while True:
        try:
            display_menu()
            choice = input(f"\n{BOLD}👉 Select option [0-6]: {RESET}").strip()
            
            if choice == "1":
                clear_screen()
                display_banner()
                scan_single_url()
                input(f"\n{BOLD}{CYAN}Press Enter to continue...{RESET}")
                clear_screen()
                display_banner()
                
            elif choice == "2":
                clear_screen()
                display_banner()
                scan_from_file()
                input(f"\n{BOLD}{CYAN}Press Enter to continue...{RESET}")
                clear_screen()
                display_banner()
                
            elif choice == "3":
                clear_screen()
                display_banner()
                configure_settings()
                clear_screen()
                display_banner()
                
            elif choice == "4":
                clear_screen()
                display_banner()
                view_history()
                input(f"\n{BOLD}{CYAN}Press Enter to continue...{RESET}")
                clear_screen()
                display_banner()
                
            elif choice == "5":
                show_documentation()
                clear_screen()
                display_banner()
                
            elif choice == "6":
                clear_screen()
                display_banner()
                generate_test_page()
                input(f"\n{BOLD}{CYAN}Press Enter to continue...{RESET}")
                clear_screen()
                display_banner()
                
            elif choice == "0":
                print(f"\n{BOLD}{GREEN}Exiting... Thank you for using XSS Toolkit!{RESET}")
                time.sleep(1)
                clear_screen()
                sys.exit(0)
                
            else:
                print(f"\n{RED}❌ Invalid option! Please choose 0-6{RESET}")
                time.sleep(1)
                clear_screen()
                display_banner()
                
        except KeyboardInterrupt:
            print(f"\n{RED}❌ Operation cancelled by user{RESET}")
            time.sleep(1)
            clear_screen()
            display_banner()
            
        except Exception as e:
            print(f"\n{RED}❌ Unexpected error: {str(e)}{RESET}")
            time.sleep(2)
            clear_screen()
            display_banner()

if __name__ == "__main__":
    main()
