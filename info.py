import psutil
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Configure the plot
fig, ax = plt.subplots()
ax.set_ylim(0, 100)
ax.set_xlim(0, 100)
ax.set_title('CPU and Memory Usage')
ax.set_xlabel('Time')
ax.set_ylabel('Usage (%)')
cpu_line, = ax.plot([], [], label='CPU', color='#FF5733')
mem_line, = ax.plot([], [], label='Memory', color='#C70039')
ax.legend()

# Add text to the CPU and Memory values
cpu_text = ax.text(0.77, 0.7, '', transform=ax.transAxes)
mem_text = ax.text(0.77, 0.6, '', transform=ax.transAxes)

# Update function for the plot
def update_chart(frame):
    # Get CPU usage information
    cpu_percent = psutil.Process().cpu_percent()

    # Get memory usage information
    memory_percent = psutil.Process().memory_percent()


    # Add data to the plot
    cpu_line.set_data(list(range(frame)), [cpu_percent]*frame)
    mem_line.set_data(list(range(frame)), [memory_percent]*frame)

    # Update the text with CPU and Memory values
    cpu_text.set_text(f'CPU: {cpu_percent:.1f}%')
    mem_text.set_text(f'Memory: {memory_percent:.1f}%')

    return cpu_line, mem_line, cpu_text, mem_text

# Animate the plot
animation = FuncAnimation(fig, update_chart, frames=100, interval=1000, blit=True)

# Style the plot lines
for line in [cpu_line, mem_line]:
    line.set_linewidth(2)
    line.set_marker('o')
    line.set_markersize(5)

# Set the background color of the plot
ax.set_facecolor('#F5F5F5')

# Show the plot
plt.show()