# Oregon State University
# CS 512 - Final Project
# Date: 2025/03/16
# Author: Paul J Anderson - Starter code provided by Justin Wolford

import pyspark
from pyspark.sql import SparkSession
import pprint
import json
from pyspark.sql.types import StructType, FloatType, IntegerType, StructField
from pyspark.sql.functions import col, mean, stddev, count
from scipy import stats
import numpy as np
from statsmodels.stats.diagnostic import lilliefors
from statsmodels.stats.stattools import jarque_bera
from google.cloud import bigquery

# function to ensure numerical data
def To_numb(x):
    """Convert strings to integers and floats for the salmon data"""
    x['year'] = int(x.get('year', 0))
    x['esu'] = int(x.get('esu', 0))
    x['max_SST'] = float(x.get('max_SST', 0.0))
    x['Mean_SST'] = float(x.get('Mean_SST', 0.0))
    x['mean_SAR'] = float(x.get('mean_SAR', 0.0))
    x['juvenile_return'] = float(x.get('juvenile_return', 0.0))
    return x

# Function to perform Welch's t-test
def welch_t_test(df, group_col, value_cols):
    """
    Perform Welch's t-test on two groups for multiple variables
    
    Parameters:
    -----------
    df : pyspark.sql.DataFrame
        The input dataframe
    group_col : str
        The column name containing group identifiers (esu)
    value_cols : list
        List of column names to compare between groups
    
    Returns:
    --------
    dict
        Dictionary of test results for each variable
    """
    results = {}
    
    for col_name in value_cols:
        # Get the two groups
        group0 = df.filter(col(group_col) == 0).select(col_name).rdd.flatMap(lambda x: x).collect()
        group1 = df.filter(col(group_col) == 1).select(col_name).rdd.flatMap(lambda x: x).collect()
        
        # Perform Welch's t-test
        t_stat, p_value = stats.ttest_ind(group0, group1, equal_var=False)
        
        results[col_name] = {
            't_statistic': t_stat,
            'p_value': p_value
        }
    
    return results

# Function to test normality assumptions
def test_normality(data):
    """
    Test normality using Lilliefors and Jarque-Bera tests
    """
    # Lilliefors test
    lf_stat, lf_p_value = lilliefors(data)
    
    # Jarque-Bera test - get only first two values
    jb_results = jarque_bera(data)
    jb_stat, jb_p_value = jb_results[0], jb_results[1]
    
    return {
        'lilliefors': {'statistic': lf_stat, 'p_value': lf_p_value},
        'jarque_bera': {'statistic': jb_stat, 'p_value': jb_p_value}
    }

# Main analysis function
def analyze_data(df):
    """
    Perform statistical analysis on the data
    """
    # Variables to compare
    variables = ['max_SST', 'Mean_SST', 'mean_SAR', 'juvenile_return']
    
    # Calculate basic statistics for all variables
    stats_df = {}
    for var in variables:
        stats = df.select([
            mean(var).alias('mean'),
            stddev(var).alias('std'),
            count(var).alias('count')
        ]).collect()
        stats_df[var] = stats[0]
    
    # Perform Welch's t-test for all variables
    t_test_results = welch_t_test(df, 'esu', variables)
    
    # Test normality assumptions for all variables
    normality_results = {}
    for var in variables:
        values = df.select(var).rdd.flatMap(lambda x: x).collect()
        normality_results[var] = test_normality(values)
    
    return {
        'basic_stats': stats_df,
        't_test': t_test_results,
        'normality_tests': normality_results
    }

#Main Python file = ('gs://cs512_final_data/spark_final.py')

#PACKAGE_EXTENSIONS= ('gs://hadoop-lib/bigquery/bigquery-connector-hadoop2-latest.jar')

## SparkContext and Configuration
sc = pyspark.SparkContext()

# Set specific bucket and project details
project_id = "cs512-447721"
bucket_name = "cs512_final_data"
input_directory = f'gs://{bucket_name}/hadoop/tmp/bigquerry/pyspark_input'
output_directory = f'gs://{bucket_name}/pyspark_demo_output'

# Create hadoop directory in GCS bucket
hadoop_path = sc._jvm.org.apache.hadoop.fs.Path(input_directory)
hadoop_fs = hadoop_path.getFileSystem(sc._jsc.hadoopConfiguration())
if not hadoop_fs.exists(hadoop_path):
    hadoop_fs.mkdirs(hadoop_path)

# Create Spark session with BigQuery configuration
spark = SparkSession \
    .builder \
    .master('yarn') \
    .appName('salmon_analysis') \
    .config('spark.jars.packages', 
            'com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.27.1,' +
            'com.google.cloud.bigquery:bigquery-connector-hadoop2:1.2.0') \
    .config('spark.hadoop.fs.gs.impl', 'com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem') \
    .config('spark.hadoop.google.cloud.auth.service.account.enable', 'true') \
    .getOrCreate()

# Update configuration with explicit values
conf = {
    'temporaryGcsBucket': bucket_name,
    'project': project_id,
    'parentProject': project_id
}

# Read data from BigQuery
df1 = spark.read.format('bigquery') \
    .option('table', f'{project_id}.final_data.final_data_scrubbed') \
    .load()

# Partition the data
df1 = df1.repartition(6)

# Perform analysis
results = analyze_data(df1)

# Print results
print("\nBasic Statistics by Variable:")
pprint.pprint(results['basic_stats'])

print("\nWelch's t-test results by Variable:")
pprint.pprint(results['t_test'])

print("\nNormality test results by Variable:")
pprint.pprint(results['normality_tests'])

## Clean up temporary files
input_path = sc._jvm.org.apache.hadoop.fs.Path(input_directory)
input_path.getFileSystem(sc._jsc.hadoopConfiguration()).delete(input_path, True)