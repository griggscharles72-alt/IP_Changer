### README for IP Changer Script

#### Overview

This script will rotate your network identity, changing your **IP address**, **MAC address**, and **hostname** regularly. It utilizes common tools like `macchanger` and `dhclient` to rotate your identity for enhanced privacy or to evade detection (for activities like web scraping).

This script works on **Linux-based systems** and requires certain dependencies. The script is customizable and allows you to change the behavior of the host, IP, and MAC address at a set interval.

#### Dependencies

Before running this script, you need to make sure that your system has the following installed:

1. **macchanger** (for rotating MAC addresses)
2. **dhclient** (for changing IP address)
3. **nmcli** (optional, another way to change IP address)
4. **python3** (for running the script)

To install the necessary dependencies, you can run the following commands:

```bash
sudo apt update
sudo apt install macchanger isc-dhcp-client network-manager
```

#### Script Overview

* **log_dir**: The script writes logs to the current working directory where the script is run.
* **phrases.txt**: This file (placed in the same directory as the script) contains phrases to randomly assign as the hostname. If the file is not found, it defaults to "default-hostname".
* **Rotation Frequency**: The script rotates the identity (IP, MAC, and Hostname) every **3 minutes** by default.

---

#### Running the Script

1. **Download the script** and save it as `IP_Changer.py`.
2. Open a terminal and navigate to the folder where the script is saved.
3. Ensure the necessary dependencies are installed (as listed above).
4. Run the script using the following command:

   ```bash
   sudo python3 IP_Changer.py
   ```

#### Features

* **MAC Address Rotation**: The script uses `macchanger` to rotate your MAC address to a random one.
* **IP Address Refresh**: It uses `dhclient` or `nmcli` to release and request a new IP address, forcing a change.
* **Hostname Change**: The script sets the hostname to a randomly chosen phrase from `phrases.txt`.
* **Logging**: The script creates a log in the current directory to track the actions.

#### Customizing the Script

* You can edit the **phrases.txt** file to include phrases that will be randomly selected to change the hostname. The file should have one phrase per line.
* The interval between identity changes is set to 3 minutes (`180` seconds). You can modify this by changing the `time.sleep(180)` in the script to a different value (in seconds).

---

#### Sample Log Output

The log will be written to a file named `ip-changer.log` in the same directory as the script. The log entries will look something like this:

```
2026-02-19 08:47:47,638 - [ip-changer] Cycle start
2026-02-19 08:47:47,663 - [ip-changer] Phrase -> harmless_device
2026-02-19 08:47:47,748 - [ip-changer] Hostname -> harmless_device
2026-02-19 08:47:47,772 - [ip-changer] MAC -> rotating
2026-02-19 08:47:47,929 - [ip-changer] IP -> dhclient refresh (forcing IPv4)
2026-02-19 08:47:52,699 - [ip-changer] Cycle complete
```

