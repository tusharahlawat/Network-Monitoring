import psutil
import socket
import time
import subprocess
import re

def get_ip_address():
    # Get the hostname
    hostname = socket.gethostname()
    # Retrieve the IP address
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def get_connection_type():
    # Get the type of network connections
    network_interfaces = psutil.net_if_stats()
    connection_type = "Unknown"

    for interface, stats in network_interfaces.items():
        if stats.isup:
            if "Wi-Fi" in interface or "Wireless" in interface or "wlan" in interface.lower():
                connection_type = "Wi-Fi"
            elif "Ethernet" in interface or "eth" in interface.lower():
                connection_type = "Ethernet"
            elif "ppp" in interface.lower():
                connection_type = "PPP (Dial-up)"
            # Add more conditions if needed for other types of connections

    return connection_type

def get_external_devices():
    # List IP addresses connected externally to the PC (ignoring local/loopback)
    external_devices = []

    # Check active network connections using psutil
    connections = psutil.net_connections()
    for conn in connections:
        if conn.status == 'ESTABLISHED' and conn.raddr:
            remote_ip = conn.raddr.ip

            # Ignore local connections (127.0.0.1) and private IP ranges
            if not is_local_ip(remote_ip):
                if remote_ip not in external_devices:
                    external_devices.append(remote_ip)

    return len(external_devices), external_devices

def is_local_ip(ip_address):
    # Check if an IP address is local (e.g., loopback or private IP ranges)
    private_ip_ranges = [
        "10.",      # Class A private range
        "172.16.",  # Class B private range
        "172.17.",
        "172.18.",
        "172.19.",
        "172.20.",
        "172.21.",
        "172.22.",
        "172.23.",
        "172.24.",
        "172.25.",
        "172.26.",
        "172.27.",
        "172.28.",
        "172.29.",
        "172.30.",
        "172.31.",
        "192.168.", # Class C private range
        "127."      # Loopback range
    ]

    # Check if the IP address starts with any of the private IP ranges
    return any(ip_address.startswith(prefix) for prefix in private_ip_ranges)

def get_connected_devices_to_network():
    # Use the `arp` command to get the list of devices connected to the network
    try:
        # Run the arp command
        output = subprocess.check_output("arp -a", shell=True).decode('utf-8')

        # Count the number of connected devices by identifying lines with IP and MAC addresses
        connected_devices = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", output)

        # Return the unique IP addresses (excluding broadcast/multicast)
        unique_devices = set(connected_devices)
        unique_devices.discard('0.0.0.0')  # Remove any irrelevant IPs
        return len(unique_devices), unique_devices

    except Exception as e:
        print(f"Error retrieving connected devices: {str(e)}")
        return 0, set()

def monitor_connection():
    # Capture the initial connection time
    start_time = time.time()
    ip_address = get_ip_address()
    connection_type = get_connection_type()

    print(f"IP Address: {ip_address}")
    print(f"Connection Type: {connection_type}")

    try:
        while True:
            # Calculate the total connection time
            current_time = time.time()
            connection_duration = current_time - start_time
            formatted_time = time.strftime("%H:%M:%S", time.gmtime(connection_duration))

            # Get the number of external devices connected directly to the PC
            external_device_count, external_devices = get_external_devices()

            # Get the number of devices connected to the network router
            network_device_count, network_devices = get_connected_devices_to_network()

            # Display connection details
            print(f"Total Connection Time: {formatted_time} | "
                  f"External Devices Connected to PC: {external_device_count} | "
                  f"Devices Connected to Router: {network_device_count}", end='\r')

            time.sleep(1)  # Update every 1 seconds

    except KeyboardInterrupt:
        print("\nConnection monitoring stopped.")

if __name__ == "__main__":
    print("Monitoring connection details. Press Ctrl+C to stop.")
    monitor_connection()
