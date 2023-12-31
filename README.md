# CodexScriptum  
Scripts I made for research and data analysis  

# reponecalcs580v.py  
Python script that does the full data analysis for a study validating a linear position transducer (RepOne) as a power measuring device during a sit-to-stand task against motion analysis and force platform gold standard measure of power.  
Script pulls in raw data, makes all necessary calculations, runs all needed stats, then outputs graphs and text files for all results.  

# TOST_power.R  
R script that runs a power analysis for a TOST test of equivalency with given upper and lower equivalency bounds.  
Used in a study validating power measured with a linear position transducer in the sit-to-stand against gold standard motion analysis and force plate.  

# TOST_power2.py  
Python script that runs a power analysis for a TOST test of equivalency using a proportional acceptance region.  
Used in a preliminary power analysis for the RepOne validation study.  

# icc_sample_size.R  
R script used to calculate needed sample size for an absolute agreement ICC.  

# NTValidation.R  
R script that runs all the stats for the validation of a novel digital neuropsych battery  

# ntvbuilder.R  
R script used to pull in neuropsych data, compute test results, then export the results into a csv for final statistical analysis.  

# PrelimSEM.R  
R script that fits CFA and SEM models for latent measures of muscle quality and walking ability and reports fit indices.  

# parseGFF.py  
Python script that parses the COVID-19 genome using fasta output.  

# write_pinnacle_slurm.py  
Python script that provides a template for creating SLURM scheduler scripts for an HPC cluster. Also contains the framewok for command line functionality with arguments.  

# RonsCode.py  
Python workflow for creating gene transcription trajectories using dynamo.  
Note: this is not working code, rather it was created as a template for another researcher who was unfamiliar with omics work in python.  

# DCMreport.py  
Python script which produced the post-study reports provided to participants following the conclusion of a large NIH grant-funded research project. Automatically pulls in data, produces graphs, and compiles everything into a 55-page PDF for each participant. Command line argument parsing was not implemented, but commented code framework exists for that functionality.  

# DCM_T4_LinearMixedModel.R  
R script to assemble our standard (wide format) study database into long/nested format and run the analysis for our study as a linear mixed model with random intercepts and slopes. Produces fixed and random effects for the model as ANOVA or ANOVA-like tables.  

# SEM_NHANES.R  
R script that tests data extracted from the NHANES study for multivariate normality and then fits CFA and SEM models measuring metabolic syndrome severity as a latent variable and regressing it on sedentary behavior duration and physical activity/exercise duration.  
