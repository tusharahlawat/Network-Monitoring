import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Excel file
file_path = 'network_stats.xlsx'  # Replace with your actual file path
data = pd.read_excel(file_path)

# Convert 'Timestamp' to a pandas datetime object (if not already in datetime format)
data['Timestamp'] = pd.to_datetime(data['Timestamp'])

# Calculate throughput (Bytes Sent and Received per second)
data['Time Diff'] = data['Timestamp'].diff().dt.total_seconds().fillna(1)
data['Throughput Sent'] = data['Bytes Sent'] / data['Time Diff']
data['Throughput Received'] = data['Bytes Received'] / data['Time Diff']

# Calculate packet success rate and packet loss
data['Packet Success Rate (%)'] = (data['Packets Received'] / data['Packets Sent']) * 100
data['Packet Loss'] = data['Packets Sent'] - data['Packets Received']

# Set larger figure size to reduce congestion
plt.figure(figsize=(12, 8))

# Visualization: Throughput over time
plt.subplot(2, 1, 1)
plt.plot(data['Timestamp'], data['Throughput Sent'], label='Throughput Sent', color='blue', alpha=0.7)
plt.plot(data['Timestamp'], data['Throughput Received'], label='Throughput Received', color='green', alpha=0.7)
plt.xlabel('Time')
plt.ylabel('Throughput (Bytes per second)')
plt.title('Network Throughput Over Time')
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)

# Visualization: Packet Success Rate over time
plt.subplot(2, 1, 2)
sns.lineplot(x=data['Timestamp'], y=data['Packet Success Rate (%)'], label='Packet Success Rate', color='purple', alpha=0.7)
plt.xlabel('Time')
plt.ylabel('Packet Success Rate (%)')
plt.title('Packet Success Rate Over Time')
plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()
plt.show()

# Packet Loss over time
plt.figure(figsize=(12, 6))
sns.barplot(x=data['Timestamp'], y=data['Packet Loss'], palette='magma', alpha=0.8)
plt.xlabel('Time')
plt.ylabel('Packet Loss')
plt.title('Packet Loss Over Time')
plt.xticks(rotation=45, visible=False)  # Hide some x-axis ticks for clarity
plt.grid(True)

plt.tight_layout()
plt.show()

# Summary statistics
print("Summary Statistics:")
print(data[['Throughput Sent', 'Throughput Received', 'Packet Success Rate (%)', 'Packet Loss']].describe())
