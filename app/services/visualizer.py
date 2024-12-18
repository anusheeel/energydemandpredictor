# Visualization functions
import matplotlib.pyplot as plt

class Visualizer:
    @staticmethod
    def plot_energy_usage(data):
        """Generates a line plot for monthly energy usage."""
        plt.figure(figsize=(10, 6))
        plt.plot(data['Month'], data['Energy Usage (kWh)'], marker='o')
        plt.title('Monthly Energy Usage')
        plt.xlabel('Month')
        plt.ylabel('Energy Usage (kWh)')
        plt.grid()
        plt.tight_layout()
        plt.savefig('app/static/energy_usage_plot.png')
