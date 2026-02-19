import os
import random
import subprocess
import time
import logging

# ---- Set up logging ----
log_dir = os.getcwd()  # Get the current working directory
log_file = f"{log_dir}/ip-changer.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger()

def log(message):
    logger.info(f"[ip-changer] {message}")
    print(f"[ip-changer] {message}")

def die(message):
    log(f"ERROR: {message}")
    exit(1)

def have(command):
    """Check if a command is installed."""
    try:
        subprocess.run([command, "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except:
        return False

# ---- Dynamic File Location ----
def get_phrases_file():
    """Look for phrases.txt in the current directory or user directory."""
    current_dir = os.getcwd()
    phrases_file = os.path.join(current_dir, "phrases.txt")
    if not os.path.exists(phrases_file):
        phrases_file = os.path.join("/home/pc-9", "phrases.txt")
    return phrases_file

# ---- Function to Get Network Interface ----
def get_interface():
    try:
        iface = subprocess.check_output("ip route show default 0.0.0.0/0", shell=True).decode().split()[4]
        return iface
    except Exception:
        die("Failed to get network interface.")

# ---- Function to Rotate MAC Address ----
def rotate_mac(iface):
    if have("macchanger"):
        log("MAC -> rotating")
        subprocess.run(f"sudo ip link set {iface} down", shell=True, check=False)
        subprocess.run(f"macchanger -r {iface}", shell=True, check=False)
        subprocess.run(f"sudo ip link set {iface} up", shell=True, check=True)

# ---- Function to Rotate IP Address with Custom Pattern ----
def rotate_ip(iface):
    """Force IPv4 address refresh using dhclient or nmcli, with custom pattern."""
    ip_patterns = [
        "5.5.5.5",  # All fives
        "6.6.6.6",  # All sixes
        "9.9.9.9",  # All nines
        "1.1.1.1",  # All ones
    ]
    
    # Pick an IP pattern
    ip = random.choice(ip_patterns)
    log(f"Setting IP to {ip}")
    
    # Force setting static IP (this is not common and may not work on every system)
    subprocess.run(f"sudo ifconfig {iface} {ip} netmask 255.255.255.0", shell=True, check=True)

    log(f"IP set to: {ip}")

# ---- Function to Set Hostname ----
def set_hostname(phrase):
    new_host = phrase if phrase != "(no phrases file)" else "default-hostname"
    subprocess.run(f"hostnamectl set-hostname {new_host}", shell=True, check=True)
    log(f"Hostname -> {new_host}")

# ---- Main Loop for Identity Rotation ----
while True:
    # ---- Pick Phrase for Hostname ----
    phrase = "(no phrases file)"
    phrases_file = get_phrases_file()

    if os.path.exists(phrases_file) and os.path.getsize(phrases_file) > 0:
        with open(phrases_file, 'r') as f:
            phrases = f.readlines()
        phrase = random.choice(phrases).strip()  # Randomly choose a phrase

    log(f"Cycle start")
    log(f"Phrase -> {phrase}")

    iface = get_interface()  # Get active interface
    log(f"Interface -> {iface}")

    set_hostname(phrase)  # Set the hostname
    rotate_mac(iface)  # Rotate MAC address
    rotate_ip(iface)  # Rotate IP address with pattern

    log("Cycle complete")
    time.sleep(180)  # 3-minute loop
