# Remove warnings
import warnings
warnings.filterwarnings('ignore')

# Import
import pandas as pd
import numpy as np
import seaborn as sns
import statsmodels.api as sm

from scipy.stats import norm
from statsmodels.nonparametric.kernel_regression import KernelReg
from pygam import LinearGAM, s, f, LogisticGAM
from sklearn.preprocessing import PolynomialFeatures, LabelEncoder
from patsy import dmatrix

# Import matplotlib for graphs
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

# Set global parameters
plt.style.use('seaborn-white')
plt.rcParams['lines.linewidth'] = 3
plt.rcParams['figure.figsize'] = (10,6)
plt.rcParams['figure.titlesize'] = 20
plt.rcParams['axes.titlesize'] = 18
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['legend.fontsize'] = 14


# Figure 7.1
def plot_predictions(X, y, x_grid, y01, y_hat1, y01_hat1, title):
    
    # Init figure
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(12,5))
    fig.suptitle(title)

    # Scatter plot with polynomial regression line
    ax1.scatter(X, y, facecolor='None', edgecolor='k', alpha=0.2)
    ax1.plot(x_grid, y_hat1, color='b')
    ax1.set_ylim(ymin=0)

    # Logistic regression showing Pr(wage>250) for the age range.
    ax2.plot(x_grid, y01_hat1, color='b')

    # Run plot showing the distribution of wage>250 in the training data.
    ax2.scatter(X, y01/5, s=30, c='grey', marker='|', alpha=0.7)

    ax2.set_ylim(-0.01,0.21)
    ax2.set_xlabel('age')
    ax2.set_ylabel('Pr(wage>250|age)');
    
# Figure 7.3
def plot_splines(df_short, x_grid, preds):

    # Init figure
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, figsize=(12,10))
    fig.suptitle('Figure 7.3')

    # Discontinuous piecewise cubic
    ax1.plot(x_grid, preds[0], color='b')
    ax1.set_title('Discontinuous piecewise cubic')
    # Continuous piecewise cubi
    ax2.plot(x_grid, preds[1], color='g')
    ax2.set_title('Continuous piecewise cubic')
    # Cubic (continuous)
    ax3.plot(x_grid, preds[2], color='r')
    ax3.set_title('Cubic')
    # Continuous piecewise linear
    ax4.plot(x_grid, preds[3], color='y')
    ax4.set_title('Continuous piecewise linear')

    for ax in (ax1,ax2,ax3,ax4):
        ax.scatter(df_short.age, df_short.wage, facecolor='None', edgecolor='k', alpha=0.3)
        ax.axvline(x=50, color='k', linestyle='--', alpha=0.5)
        
        
# Figure 7.4
def compare_predictions(X, y, x_grid, preds, labels):

    # Init figure
    fig, ax = plt.subplots(1,1)
    fig.suptitle('Figure 7.4')

    # Scatter
    ax.scatter(X, y, facecolor='None', edgecolor='k', alpha=0.1)
    for pred, label in zip(preds, labels):
        ax.plot(x_grid, pred, label=label)
    [ax.vlines(i , 0, 350, linestyles='dashed', lw=2, colors='k') for i in [25,40,60]]
    ax.legend(bbox_to_anchor=(1.5, 1.0))
    ax.set_xlabel('age'), ax.set_ylabel('wage');
    
    
# Make new figure 1
def plot_simulated_data(X_sim, y_sim, X_grid, y_grid):

    # Init
    fig, ax = plt.subplots(1,1)
    fig.suptitle('Simulated data');

    # Plot
    ax.scatter(X_sim, y_sim, facecolor='None', edgecolor='k', alpha=0.5, label='data');
    ax.plot(X_grid, y_grid, label='True relationship');
    ax.set_xlabel('X'); ax.set_ylabel('y'); 
    ax.legend();
    return fig, ax

    
# Figure 7.9a
def make_figure_7_9a(fig, ax, X_sim, y_hat):
    ax.plot(X_sim, y_hat[0], label='LLN Estimate');
    ax.legend();
    return fig, ax
    

# Figure 7.9b
def make_figure_7_9b(fig, ax, X_tilde, y_tilde, X_grid_tilde, y_grid_tilde, x_i, y_i_hat):

    # Add local details
    ax.scatter(X_tilde, y_tilde, facecolor='orange', edgecolor='None', alpha=0.5);
    ax.scatter(x_i, y_i_hat, facecolor='r', alpha=1);
    ax.plot(X_grid_tilde, y_grid_tilde, color='r', label='Local OLS');

    # Legend
    ax.legend();
    ax.annotate("$x_i$", (x_i, y_i_hat-0.2), color='r', fontsize=20);
    ax.set_xlabel('X'); ax.set_ylabel('y'); 
    
    
# Figure 7.9 - d
def make_figure_7_9d(X_sim, y_sim, w, results, X_grid, x_i, y_i_hat):

    # Init
    fig, ax = plt.subplots()
    fig.suptitle('Local Weighted Least Squares');

    # Zoom in
    points = ax.scatter(X_sim, y_sim, c=w, cmap="YlOrRd", edgecolors='lightgrey', alpha=.7, s=80);
    plt.colorbar(points, label='gaussian weights')
    ax.plot(X_grid, results.params[0] + results.params[1]*X_grid, color='r')
    ax.scatter(x_i, y_i_hat, facecolor='r', alpha=1);
    ax.annotate("$x_i$", (x_i, y_i_hat-0.1), color='r', fontsize=20);
    ax.set_xlabel('local X'); ax.set_ylabel('local y'); 
    
    
# Figure 7.13
def plot_gam(gam):
    
    # Init
    fig, axs = plt.subplots(1,3,figsize=(15,5));
    fig.suptitle('Figure 7.13')

    # Plot
    titles = ['year', 'age', 'education']
    for i, ax in enumerate(axs):
        XX = gam.generate_X_grid(term=i)
        pdep, confi = gam.partial_dependence(term=i, width=.95)
        ax.plot(XX[:, i], pdep)
        ax.plot(XX[:, i], confi, c='k', ls=':', alpha=0.5)
        if i == 0:
            ax.set_ylim(-40,40)
        ax.set_xlabel(titles[i]);