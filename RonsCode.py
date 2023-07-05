# Import packages
import anndata
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scanpy as sc
from sklearn.decomposition import TruncatedSVD
from scipy import sparse, io
import dynamo as dyn

# This is just some setup stuff that is not used by dynamo - it is likely a good idea to yeet this stuff
matplotlib.rcParams.update({'font.size': 12})
%config InlineBackend.figure_format = 'retina'

# This step runs `kb` to pseudoalign the reads, and then generate the cells x gene matrix in h5ad format.
# This command should run from the shell, unlear if the format is bash or power shell or doesn't matter
# The file names will be your fastq files - they can be in gzip format
# This is also the part that needs the index - index.idx will get replaced by it
# Unclear what the t2g.txt is - we will need to look into the kb-python documentation for that
!kb count -i index.idx -g t2g.txt -x 10xv2 --h5ad -t 2 \ SRR8599150_S1_L001_R1_001.fastq.gz SRR8599150_S1_L001_R2_001.fastq.gz

# Now we start in dynamo

# Dynamo visualization defaults - none of this is probably needed, but will probably make things prettier
# You'll need to choose, just comment out what you don't want
dyn.configuration.set_figure_params('dynamo', background='white') # jupter notebooks
dyn.configuration.set_figure_params('dynamo', background='black') # presentation
dyn.configuration.set_pub_style() # manuscript

# Load data - this will be the h5ad file you want to run
# For multiple files, we can make a loop to do the dynamo steps over and over
adata = dyn.read(filename)

# Pre-process
# Looks like this uses monocle-3
dyn.pp.recipe_monocle(adata)

# Check gene kinetics and velocities
dyn.tl.dynamics(adata)
# dyn.tl.moments(adata) # I believe this function is called automatically as part of tl.dynamics

# QC check on data
# You may need to filter out the low-confidence vectors - this will require more code if so
dyn.tl.gene_wise_confidence(adata, group='group', lineage_dict={'Progenitor': ['terminal_cell_state']})

# Dimensional Reduction
dyn.tl.reduceDimension(adata)

# Project velocity vectors
# There is another kernal called Ito that you can use here - I don't know what that is, but if you need it I am guessing it will just be an arg we can add to the function
dyn.tl.cell_velocities(adata)
# dyn.tl.cell_velocities(adata, basis='pca') # If you would rather use PCA than umap

# QC check on velocities
dyn.tl.cell_wise_confidence(adata)

# This is extra stuff dynamo does which might be beyond what you want, but I am just going to continue the workflow

# This extapolates out your vector field to predict things like cell fate
dyn.vf.VectorField(adata)

# Map topology/topography (unsure which)
dyn.vf.topography(adata, basis='umap')

# Map potential landscape
dyn.ext.ddhodge(adata)
dyn.vf.Potential(adata)

# Some visualizations you can do
dyn.pl.cell_wise_vectors(adata, color=colors, ncols=3)
dyn.pl.grid_vectors(adata, color=colors, ncols=3)
dyn.pl.stremline_plot(adata, color=colors, ncols=3)
dyn.pl.line_integral_conv(adata)

# Visualizing 2D vector field topography
dyn.vf.VectorField(adata, basis='umap')
dyn.pl.topography(adata)

# Dynamo plot example - this will actually export a visualization
fig1, f1_axes = plt.subplots(ncols=2, nrows=2, constrained_layout=True, figsize=(12, 10))
f1_axes
f1_axes[0, 0] = dyn.pl.cell_wise_vectors(adata, color='umap_ddhodge_potential', pointsize=0.1, alpha = 0.7, ax=f1_axes[0, 0], quiver_length=6, quiver_size=6, save_show_or_return='return')
f1_axes[0, 1] = dyn.pl.grid_vectors(adata, color='speed_umap', ax=f1_axes[0, 1], quiver_length=12, quiver_size=12, save_show_or_return='return')
f1_axes[1, 0] = dyn.pl.streamline_plot(adata, color='divergence_pca', ax=f1_axes[1, 0], save_show_or_return='return')
f1_axes[1, 1] = dyn.pl.topography(adata, color='acceleration_umap', ax=f1_axes[1, 1], save_show_or_return='return')
plt.show() # I would probably write this into a PNG output or something