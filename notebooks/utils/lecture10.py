# Remove warnings
import warnings
warnings.filterwarnings('ignore')

# General packages
import pandas as pd
import numpy as np
import seaborn as sns
import time
from scipy.stats import multivariate_normal

# Sklean
from sklearn.preprocessing import scale
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from scipy.cluster import hierarchy
from scipy.cluster.hierarchy import linkage, dendrogram, cut_tree

# Import matplotlib for graphs
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
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
    fig, ax1 = plt.subplots(figsize=(8,8))
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


# Figure new 1
def make_new_figure_1(X):
    
    # Init
    fig, ax = plt.subplots(figsize=(6, 5))
    fig.suptitle("Baseline")

    # Plot
    ax.scatter(X[:,0], X[:,1], s=50, alpha=0.5, c='k') 
    ax.set_xlabel('X0'); ax.set_ylabel('X1');
    

# Figure new 2
def make_new_figure_2(X, clusters0):
    
    # Init
    fig, ax = plt.subplots(figsize=(6, 5))
    fig.suptitle("Random assignment")

    # Plot
    ax.scatter(X[clusters0==0,0], X[clusters0==0,1], s=50, alpha=0.5) 
    ax.scatter(X[clusters0==1,0], X[clusters0==1,1], s=50, alpha=0.5)
    ax.set_xlabel('X0'); ax.set_ylabel('X1');


# Plot assignment
def plot_assignment(X, centroids, clusters, d, i):
    clear_output(wait=True)
    fig, ax = plt.subplots(figsize=(6, 5))
    fig.suptitle("Iteration %.0f: inertia=%.1f" % (i,d))

    # Plot
    ax.clear()
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color'];
    K = np.size(centroids,0)
    for k in range(K):
        ax.scatter(X[clusters==k,0], X[clusters==k,1], s=50, c=colors[k], alpha=0.5) 
        ax.scatter(centroids[k,0], centroids[k,1], marker = '*', s=300, color=colors[k])
        ax.set_xlabel('X0'); ax.set_ylabel('X1');
    
    # Show
    plt.show();
    
# Figure new 3
def make_new_figure_3(d):
    
    # Init
    plt.figure(figsize=(25, 10))
    plt.title('Hierarchical Clustering Dendrogram')

    # calculate full dendrogram
    plt.xlabel('sample index')
    plt.ylabel('distance')
    d
    plt.show()
    
    
# Figure new 4
def make_new_figure_4(linkages, titles):
    
    # Init
    fig, (ax1,ax2,ax3) = plt.subplots(1,3, figsize=(15,6))

    # Plot
    for linkage, t, ax in zip(linkages, titles, (ax1,ax2,ax3)):
        dendrogram(linkage, ax=ax)
        ax.set_title(t)
        
        
def get_cov_ellipse(distr, nstd, **kwargs):
    """
    Return a matplotlib Ellipse patch representing a standard distribution around the mean
    """

    # Find and sort eigenvalues and eigenvectors into descending order
    eigvals, eigvecs = np.linalg.eigh(distr.cov)
    order = eigvals.argsort()[::-1]
    eigvals, eigvecs = eigvals[order], eigvecs[:, order]

    # The anti-clockwise angle to rotate our ellipse by 
    vx, vy = eigvecs[:,0][0], eigvecs[:,0][1]
    theta = np.arctan2(vy, vx)

    # Width and height of ellipse to draw
    width, height = 2 * nstd * np.sqrt(eigvals)
    return Ellipse(xy=distr.mean, width=width, height=height,
                   angle=np.degrees(theta), **kwargs)


# Plot assignment
def plot_assignment_gmm(X, clusters, distr, i, logL):
    clear_output(wait=True)
    fig, ax = plt.subplots(figsize=(6, 5))
    fig.suptitle(f"Iteration {i}, logL={logL:.2}")

    # Plot
    ax.clear()
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color'];
    K = len(distr)
    for k in range(K):
        ax.scatter(X[clusters==k,0], X[clusters==k,1], s=50, c=colors[k], alpha=0.5) 
        ax.scatter(distr[k].mean[0], distr[k].mean[1], marker = '*', s=300, color=colors[k])
        for i in [0.5, 1, 2]:
            ax.add_artist(get_cov_ellipse(distr[k], nstd=i, color=colors[k], alpha=0.05))
        ax.set_xlabel('X0'); ax.set_ylabel('X1');
    
    # Show
    plt.show();