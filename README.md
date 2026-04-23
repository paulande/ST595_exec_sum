
# Chinook SAR Analysis — Upper Columbia Basin Spring-run ESU

## Overview

This repository contains data, code, and reporting files for a statistical analysis assessing the impact of ESU critical habitat designation on Spring-run Upper Columbia Basin Chinook Salmon. The analysis evaluates whether biological and environmental variables differ significantly between pre- and post-designation periods (split at September 2005), and investigates whether sea surface temperature (SST) explains variance in smolt-to-adult return (SAR) rates beyond designation period alone.

This project expands on prior work by Team Nexus (CS512, Oregon State University, Winter 2025) by extending the analytical timeframe to 1994–2024 and conducting all hypothesis testing and modeling in R.

---

## Repository Contents

- **chinook_SAR_anderson.Rmd**  
  Finalized R Markdown document containing all exploratory data analysis (EDA), assumption checks, hypothesis tests, linear modeling, and final type setting.

- **anderson_final.Rmd**  
  Source R Markdown document containing git changes from original hadoop and spark project.

- **chinook_SAR_anderson.pdf**  
  Rendered PDF report

- **final_data_post_dataprep.csv**  
  Cleaned and joined dataset following Dataprep scrubbing

- **imputed_dataset.csv**  
  Final dataset with KNN-imputed values for mean SAR and juvenile return

- **climate_data_sample.csv**  
  Sample of raw climatic data from NOAA NCEI

- **fish_data.csv**  
  Raw fish stock data retrieved from the Columbia Basin Research DART system

- **imputation.py**  
  Python script for KNN imputation using *scikit-learn*

- **spark_final.py**  
  Python script for initial data processing

- **gauge_data.py**  
  Python script for gauge and precipitation data processing

- **storm_events_inspection.py**  
  Python script for inspection of storm events data

- **storm_events.py**  
  Python script for storm events data processing

- **references.bib**  
  BibTeX reference file

- **df_schema.png**  
  BigQuery dataframe schema image

---

## Data Sources

- **Smolt-to-Adult Return (SAR) and Juvenile Return**  
  Columbia Basin Research DART System, University of Washington

- **Sea Surface Temperature (SST)**  
  NOAA Northwest Fisheries Science Center, California Current extent

- **Climatic Variables**  
  NOAA National Centers for Environmental Information (NCEI), 1994–2024

---

## Methods Summary

All hypothesis testing and modeling were conducted in R following data scrubbing in Google Cloud Dataprep. The analytical workflow includes:

- **Exploratory Data Analysis (EDA)**  
  Summary statistics, faceted boxplots, Q–Q plots, and autocorrelation (ACF) plots

- **Assumption validation**  
  Shapiro–Wilk normality tests, variance assessment, and independence checks

- **Hypothesis testing**  
  Welch’s two-sample *t*-tests comparing pre- and post-ESU designation periods for:
  - Mean SAR  
  - Juvenile return  
  - Mean SST  
  - Maximum SST  

- **Linear modeling**  
  Three competing OLS regression models evaluated using AIC, BIC, and adjusted R² to identify environmental predictors of mean SAR beyond ESU designation period alone

- **Missing data handling**  
  KNN imputation performed in Python using *scikit-learn* for mean SAR and juvenile return fields

---

## Key Findings

- No statistically significant difference was detected in mean SAR (*p* = 0.072) or juvenile return (*p* = 0.288) between pre- and post-designation periods
- Maximum SST was significantly higher in the post-designation period (*p* = 0.013)
- The model including maximum SST and ESU designation (M2) provided the best fit for predicting mean SAR (R² = 0.365, AIC = 48.187), with maximum SST emerging as a significant negative predictor (β = −0.273, *p* = 0.002)

---

## Requirements

### R Packages
`ggplot2`, `bookdown`, `GGally`, `tidyr`, `knitr`, `broom`, `backports`,  
`faraway`, `MASS`, `reshape`, `ggExtra`, `car`, `dplyr`,  
`reticulate`, `tinytex`, `kableExtra`, `here`

### Python Packages
`pandas`, `scikit-learn`, `glob`

---

## Citation

Anderson, P. *Evaluating the Effects of Habitat Designation and Climate on Spring-run Chinook Salmon Return Rates in the Upper Columbia River Basin.*  
ST595 Executive Summaries. Oregon State University. Spring 2026.
