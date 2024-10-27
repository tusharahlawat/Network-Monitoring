import psutil
import asyncio
import openpyxl
import time

# Asynchronous function to retrieve network stats
async def get_network_stats():
    net_stats = psutil.net_io_counters()
    return {
        'bytes_sent': net_stats.bytes_sent,
        'bytes_received': net_stats.bytes_recv,
        'packets_sent': net_stats.packets_sent,
        'packets_received': net_stats.packets_recv
    }

# Function to write network stats to Excel
def write_to_excel(timestamp, sent_bytes, received_bytes, sent_packets, received_packets):
    try:
        workbook = openpyxl.load_workbook("network_stats.xlsx")
        sheet = workbook.active
    except FileNotFoundError:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(["Timestamp", "Bytes Sent", "Bytes Received", "Packets Sent", "Packets Received"])

    # Append network data
    sheet.append([timestamp, sent_bytes, received_bytes, sent_packets, received_packets])
    workbook.save("network_stats.xlsx")

# Asynchronous monitoring function
async def monitor_network(interval=1):
    previous_stats = await get_network_stats()
    
    while True:
        await asyncio.sleep(interval)
        current_stats = await get_network_stats()

        sent_bytes = current_stats['bytes_sent'] - previous_stats['bytes_sent']
        received_bytes = current_stats['bytes_received'] - previous_stats['bytes_received']
        sent_packets = current_stats['packets_sent'] - previous_stats['packets_sent']
        received_packets = current_stats['packets_received'] - previous_stats['packets_received']

        print("Network performance in the last {} seconds:".format(interval))
        print(f"Bytes Sent: {sent_bytes} | Bytes Received: {received_bytes}")
        print(f"Packets Sent: {sent_packets} | Packets Received: {received_packets}")
        print("=" * 50)

        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        write_to_excel(timestamp, sent_bytes, received_bytes, sent_packets, received_packets)

        previous_stats = current_stats

if __name__ == "__main__":
    try:
        print("Monitoring network performance using asynchronous I/O. Press Ctrl+C to stop.")
        asyncio.run(monitor_network(interval=1))  # Run the async monitor
    except KeyboardInterrupt:
        print("\nNetwork monitoring stopped.")
