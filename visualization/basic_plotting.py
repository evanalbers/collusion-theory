import h5py
import numpy as np
import matplotlib.pyplot as plt
import os
from glob import glob

def plot_agent_data(filepath, agent_name=None):
    """Plot data for a single agent"""
    
    # Extract agent name from filepath if not provided
    if agent_name is None:
        agent_name = os.path.splitext(os.path.basename(filepath))[0]
    
    # Load data
    with h5py.File(filepath, 'r') as f:
        prices = f['prices'][:]
        capital = f['capital'][:]
        k_values = f['k_values'][:]
    
    # Create timesteps array
    timesteps = np.arange(len(prices))
    
    # Create figure with 3 subplots
    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    fig.suptitle(f'Agent: {agent_name}', fontsize=14, fontweight='bold')
    
    # Plot Capital
    axes[0].plot(timesteps, capital, color='green', linewidth=1.5, alpha=0.8)
    axes[0].set_ylabel('Capital', fontsize=12)
    axes[0].grid(True, alpha=0.3)
    axes[0].set_title('Capital over Time')
    
    # Plot Prices
    axes[1].plot(timesteps, prices, color='blue', linewidth=1.5, alpha=0.8)
    axes[1].set_ylabel('Price', fontsize=12)
    axes[1].grid(True, alpha=0.3)
    axes[1].set_title('Prices over Time')
    
    # Plot k values
    axes[2].plot(timesteps, k_values, color='red', linewidth=1.5, alpha=0.8)
    axes[2].set_ylabel('k value', fontsize=12)
    axes[2].set_xlabel('Timestep', fontsize=12)
    axes[2].grid(True, alpha=0.3)
    axes[2].set_title('k Values over Time')
    
    plt.tight_layout()
    return fig, axes

def plot_multiple_agents(directory, agent_pattern='*.h5'):
    """Plot data for multiple agents in same figure"""
    
    # Find all agent files
    pattern = os.path.join(directory, agent_pattern)
    files = glob(pattern)
    
    if not files:
        print(f"No files found matching pattern: {pattern}")
        return
    
    # Create figure
    fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)
    fig.suptitle('Multi-Agent Comparison', fontsize=14, fontweight='bold')
    
    # Colors for different agents
    colors = plt.cm.tab10(np.linspace(0, 1, len(files)))
    
    for idx, filepath in enumerate(sorted(files)):
        agent_name = os.path.splitext(os.path.basename(filepath))[0]
        
        with h5py.File(filepath, 'r') as f:
            prices = f['prices'][:]
            capital = f['capital'][:]
            k_values = f['k_values'][:]
        
        timesteps = np.arange(len(prices))
        color = colors[idx]
        
        # Plot with labels only on first iteration
        axes[0].plot(timesteps, capital, color=color, linewidth=1.5, 
                    alpha=0.7, label=agent_name)
        axes[1].plot(timesteps, prices, color=color, linewidth=1.5, 
                    alpha=0.7, label=agent_name)
        axes[2].plot(timesteps, k_values, color=color, linewidth=1.5, 
                    alpha=0.7, label=agent_name)
    
    # Format axes
    axes[0].set_ylabel('Capital', fontsize=12)
    axes[0].grid(True, alpha=0.3)
    axes[0].legend(loc='upper right', ncol=min(3, len(files)))
    axes[0].set_title('Capital over Time')
    
    axes[1].set_ylabel('Price', fontsize=12)
    axes[1].grid(True, alpha=0.3)
    axes[1].set_title('Prices over Time')
    
    axes[2].set_ylabel('k value', fontsize=12)
    axes[2].set_xlabel('Timestep', fontsize=12)
    axes[2].grid(True, alpha=0.3)
    axes[2].set_title('k Values over Time')
    
    plt.tight_layout()
    return fig, axes

def plot_summary_statistics(directory, agent_pattern='*.h5'):
    """Plot summary statistics across all agents"""
    
    pattern = os.path.join(directory, agent_pattern)
    files = glob(pattern)
    
    if not files:
        print(f"No files found matching pattern: {pattern}")
        return
    
    # Collect all data
    all_capital = []
    all_prices = []
    all_k = []
    agent_names = []
    
    for filepath in sorted(files):
        agent_name = os.path.splitext(os.path.basename(filepath))[0]
        agent_names.append(agent_name)
        
        with h5py.File(filepath, 'r') as f:
            all_capital.append(f['capital'][:])
            all_prices.append(f['prices'][:])
            all_k.append(f['k_values'][:])
    
    # Convert to arrays for easier manipulation
    all_capital = np.array(all_capital)
    all_prices = np.array(all_prices)
    all_k = np.array(all_k)
    
    timesteps = np.arange(all_capital.shape[1])
    
    # Create summary plot
    fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)
    fig.suptitle('Summary Statistics Across All Agents', fontsize=14, fontweight='bold')
    
    # Plot mean and std for each metric
    for ax, data, label, color in zip(axes, 
                                       [all_capital, all_prices, all_k],
                                       ['Capital', 'Price', 'k value'],
                                       ['green', 'blue', 'red']):
        mean = np.mean(data, axis=0)
        std = np.std(data, axis=0)
        
        ax.plot(timesteps, mean, color=color, linewidth=2, label='Mean')
        ax.fill_between(timesteps, mean - std, mean + std, 
                        alpha=0.3, color=color, label='±1 std')
        ax.set_ylabel(label, fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper right')
    
    axes[0].set_title('Average Capital ± Standard Deviation')
    axes[1].set_title('Average Price ± Standard Deviation')
    axes[2].set_title('Average k Value ± Standard Deviation')
    axes[-1].set_xlabel('Timestep', fontsize=12)
    
    plt.tight_layout()
    return fig, axes

# Main execution
if __name__ == "__main__":
    import sys
    
    # Get directory from command line or use current directory
    output_directory = sys.argv[1] if len(sys.argv) > 1 else "."
    
    # Plot individual agent (example)
    # fig1, ax1 = plot_agent_data(output_directory + '/agent_0.h5')
    
    # Plot all agents on same plot
    fig2, ax2 = plot_multiple_agents(output_directory)
    
    # Plot summary statistics
    fig3, ax3 = plot_summary_statistics(output_directory)
    
    plt.show()
    
    # Optional: Save figures
    # fig2.savefig('multi_agent_comparison.png', dpi=150, bbox_inches='tight')
    # fig3.savefig('summary_statistics.png', dpi=150, bbox_inches='tight')