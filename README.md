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

You will need access to the audiomoth dataset + have python installed.

### Clone respository

<pre>
cd your_working_folder
git clone https://github.com/kjchesh/audiomoth-analysis.git
cd audiomoth-analysis  </pre>

### Create and Activate a Virtual Environment

<pre>python -m venv .venv</pre>
#### Windows
<pre>.venv\Scripts\activate </pre>

#### macOS/Linux
<pre>
source .venv/bin/activate</pre>

### Install Dependencies
<pre>pip install -r requirements.txt</pre>


### Data

    Create a folder in the repo root called data_raw

    Paste your excel data into the folder and call it helman_tor_audiomoth_data

Processed data will be stored in  
<pre>data_processed/</pre>

Tables saved within notebooks are stored (as csv files) in  
<pre>outputs/</pre>

### Register Environment as a Kernel

<pre>python -m ipykernel install --user --name audiomoth-analysis --display-name "Python (audiomoth-analysis)" </pre>


### Launch Jupyter
<pre>jupyter lab</pre>

#### Inside Jupyter:

    Open a notebook (start with 01_data_preparation since the other notebooks rely on the data_processed/analysis_df output created in that notebook)

    Go to Kernel → Change Kernel

    Select the environment named Python (audiomoth-analysis)

    Go to Run → Run All Cells
