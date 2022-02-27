# Remove warnings
import warnings
warnings.filterwarnings('ignore')

# General packages
import pandas as pd
import numpy as np
import seaborn as sns
import time

# Sklean
from sklearn.preprocessing import scale
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from scipy.cluster import hierarchy
from scipy.cluster.hierarchy import linkage, dendrogram, cut_tree

# Import matplotlib for graphs
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from IPython.display import clear_output

# Set global parameters
plt.style.use('seaborn-white')
plt.rcParams['lines.linewidth'] = 3
plt.rcParams['figure.figsize'] = (10,6)
plt.rcParams['figure.titlesize'] = 20
plt.rcParams['axes.titlesize'] = 18
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['legend.fontsize'] = 14

# Figure 10.1 a
def make_figure_10_1a(df_dim2, df_weights):

    # Init
    fig, ax1 = plt.subplots(figsize=(10,10))
    ax1.set_title('Figure 10.1');

    # Plot Principal Components 1 and 2
    for i in df_dim2.index:
        ax1.annotate(i, (df_dim2.PC1.loc[i], -df_dim2.PC2.loc[i]), ha='center', fontsize=14)

    # Plot reference lines
    m = np.max(np.abs(df_dim2.values))*1.2
    ax1.hlines(0,-m,m, linestyles='dotted', colors='grey')
    ax1.vlines(0,-m,m, linestyles='dotted', colors='grey')
    ax1.set_xlabel('First Principal Component')
    ax1.set_ylabel('Second Principal Component')
    ax1.set_xlim(-m,m); ax1.set_ylim(-m,m)

    # Plot Principal Component loading vectors, using a second y-axis.
    ax1b = ax1.twinx().twiny() 
    ax1b.set_ylim(-1,1); ax1b.set_xlim(-1,1)
    for i in df_weights[['PC1', 'PC2']].index:
        ax1b.annotate(i, (df_weights.PC1.loc[i]*1.05, -df_weights.PC2.loc[i]*1.05), color='orange', fontsize=16)
        ax1b.arrow(0,0,df_weights.PC1[i], -df_weights.PC2[i], color='orange', lw=2)
        
        
# Figure 10.1 b
def make_figure_10_1b(df_dim2, df_dim2_u, df_weights, df_weights_u):

    # Init
    fig, (ax1,ax2) = plt.subplots(1,2,figsize=(18,9))

    # Scaled PCA
    for i in df_dim2.index:
        ax1.annotate(i, (df_dim2.PC1.loc[i], -df_dim2.PC2.loc[i]), ha='center', fontsize=14)
    ax1b = ax1.twinx().twiny() 
    ax1b.set_ylim(-1,1); ax1b.set_xlim(-1,1)
    for i in df_weights[['PC1', 'PC2']].index:
        ax1b.annotate(i, (df_weights.PC1.loc[i]*1.05, -df_weights.PC2.loc[i]*1.05), color='orange', fontsize=16)
        ax1b.arrow(0,0,df_weights.PC1[i], -df_weights.PC2[i], color='orange', lw=2)
    ax1.set_title('Scaled')

    # Unscaled PCA
    for i in df_dim2_u.index:
        ax2.annotate(i, (df_dim2_u.PC1.loc[i], -df_dim2_u.PC2.loc[i]), ha='center', fontsize=14)
    ax2b = ax2.twinx().twiny() 
    ax2b.set_ylim(-1,1); ax2b.set_xlim(-1,1)
    for i in df_weights_u[['PC1', 'PC2']].index:
        ax2b.annotate(i, (df_weights_u.PC1.loc[i]*1.05, -df_weights_u.PC2.loc[i]*1.05), color='orange', fontsize=16)
        ax2b.arrow(0,0,df_weights_u.PC1[i], -df_weights_u.PC2[i], color='orange', lw=2)
    ax2.set_title('Unscaled')

    # Plot reference lines
    for ax,df in zip((ax1,ax2), (df_dim2,df_dim2_u)):
        m = np.max(np.abs(df.values))*1.2
        ax.hlines(0,-m,m, linestyles='dotted', colors='grey')
        ax.vlines(0,-m,m, linestyles='dotted', colors='grey')
        ax.set_xlabel('First Principal Component')
        ax.set_ylabel('Second Principal Component')
        ax.set_xlim(-m,m); ax.set_ylim(-m,m)


# Figure 10.2
def make_figure_10_2(pca4):

    # Init
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(12,5))
    fig.suptitle('Figure 10.2');

    # Relative 
    ax1.plot([1,2,3,4], pca4.explained_variance_ratio_)
    ax1.set_ylabel('Prop. Variance Explained')
    ax1.set_xlabel('Principal Component');

    # Cumulative
    ax2.plot([1,2,3,4], np.cumsum(pca4.explained_variance_ratio_))
    ax2.set_ylabel('Cumulative Variance Explained');
    ax2.set_xlabel('Principal Component');
    
# Figure new 4
def make_new_figure_4(linkages, titles):
    
    # Init
    fig, (ax1,ax2,ax3) = plt.subplots(1,3, figsize=(18,10))

    # Plot
    for linkage, t, ax in zip(linkages, titles, (ax1,ax2,ax3)):
        dendrogram(linkage, ax=ax)
        ax.set_title(t)