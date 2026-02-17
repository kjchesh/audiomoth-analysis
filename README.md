# AudioMoth Data Analysis

This project explores and analyses bird detections from AudioMoth deployments using BirdNET-style outputs. The focus is on understanding spatial and temporal detection and species patterns across sites and devices.

## Currently includes

- Python utilities for loading, cleaning, and validating detection data

- Derivation of deployment effort metrics (active device days)

- Effort-standardised detection summaries at device and site level

## Jupyter notebooks for exploratory and applied analysis of:

- Species richness and activity across sites

- Dominant species patterns

- Detection confidence across sites and species

- Hourly, weekly and monthly detection patterns across sites and devices

## Running the Project Notebooks

You will need access to the audiomoth dataset

### Clone respository

<pre>git clone kjchesh/audiomoth-analysis  
cd <YOUR_REPO_FOLDER> </pre>

### Create & Activate a Virtual Environment

#### Windows
<pre>python -m venv .venv  
.venv\Scripts\activate </pre>

#### macOS/Linux
<pre>python -m venv .venv  
source .venv/bin/activate</pre>

### Install Dependencies
<pre>pip install -r requirements.txt</pre>


### Launch Jupyter
<pre>jupyter lab</pre>

#### Inside Jupyter:

    Open a notebook

    Go to Kernel → Change Kernel

    Select the environment named .venv


### Data

    Paste your excel data into the folder  
    data_raw/

    processed data will be stored in  
    data_processed/

    Tables saved within notebooks are stored (as csv files) in  
    outputs/
