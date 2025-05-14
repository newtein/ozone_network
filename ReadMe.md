# Network Analysis of Ground-Level Ozone (1980–2017)

**Network Analysis of Ground-Level Ozone: Implications for Environmental Policy and Air Quality Management** is an open-source project accompanying the accepted manuscript in *Environmental Modelling & Software* (May 2025). This repository contains code and data to model and analyze ground-level ozone as a **network of interconnected monitoring sites** across the continental United States, spanning 1980–2017. By leveraging network science and graph theory techniques, the project explores how ozone pollution networks evolve under different air quality regulatory frameworks. In particular, it contrasts **CARB** (California Air Resources Board) states (with stricter vehicle emission standards) versus **non-CARB** regions to assess the impact of environmental policies on ozone network structure and dynamics.

*\[TOC]*

* [Project Overview](#project-overview)
* [Graphical Abstract](#graphical-abstract)
* [Repository Structure](#repository-structure)
* [Installation & Requirements](#installation--requirements)
* [Data Sources & Access](#data-sources--access)
* [Usage Instructions](#usage-instructions)
* [Results Overview](#results-overview)
* [Citation](#citation)
* [License](#license)
* [Acknowledgments](#acknowledgments)

## Project Overview

Ground-level ozone is a key air pollutant influenced by emissions, weather, and regulatory controls. This project treats ozone monitoring data as a **complex network**, where nodes are monitoring sites (counties) and edges represent significant correlations in ozone levels between sites. By constructing annual ozone correlation networks from 1980 through 2017, the analysis can quantify changes in network connectivity, clustering, and other graph metrics over time. These network metrics serve as proxies for how *integrated* or *fragmented* regional ozone pollution patterns are, which in turn reflect the effectiveness of air quality management strategies.

Key goals of this project include:

* Building **ozone correlation networks** for each year and each state/region, capturing relationships between daily ozone concentration time series at different locations.
* Evaluating **temporal trends** in network properties (e.g. degree distribution, path length, clustering coefficient) to detect improvements or deteriorations in air quality cohesion.
* Identifying differences between **CARB vs. non-CARB states** – CARB states follow California’s stricter vehicle emissions standards – to gauge policy impacts on ozone network behavior.
* Mapping **policy effects**: linking changes in network metrics with historical environmental regulations and energy trends, thereby highlighting how policy and energy sector shifts influence ozone pollution connectivity.

By examining the ozone network’s evolution as regulations tighten or relax, the project provides insights for environmental policy and air quality management. The network approach uncovers the inherent interconnectedness of air pollution across regions, moving beyond isolated trends to a **system-level perspective** on ozone pollution.

## Graphical Abstract

&#x20;*Graphical Abstract: Visual summary of the US ozone monitoring network and its properties (1980–2017). (a) Map of ozone monitoring sites (green dots) across the contiguous US with edges (purple lines) indicating significant correlations between daily ozone levels (line thickness ∝ correlation strength). (b) Degree distribution of the ozone network (observed vs. expected for a random network, dotted green). (c) Distribution of Pearson cross-correlation coefficients among sites, from weak to strong connections. (d) Scatter plot of node degree vs. clustering coefficient for each site, indicating how more connected sites tend to exhibit higher clustering. (e) Table of key network statistics (number of nodes *N* and edges *L*, average degree, average path length, diameter vs. a comparable random network, average clustering coefficient, etc.), providing an overview of the network’s structural characteristics.*

## Repository Structure

The repository is organized to facilitate data processing, network construction, analysis, and figure generation. Below is a high-level overview of the key components:

* **Data Processing Scripts:** Python scripts for parsing raw data and constructing network datasets:

  * `parsingTheDataset.py` and variants (`parsingTheDatasetCARB.py`, `parsingTheDatasetPMJ.py`, etc.) – ingest raw EPA data (ozone and meteorological variables) and prepare structured datasets (e.g., time series per site or per state).
  * `calculateCorrelations.py` – compute correlation matrices between ozone monitoring sites (nodes) for specified regions/years.
  * `calculateNumberOfCorrelations.py` – analyze counts of significant correlations and possibly other summary stats from the correlation matrices.
  * `commonFunctions.py` & `excelFunctions.py` – utility functions for data handling (e.g. reading/writing Excel, common calculations used across notebooks).

* **Jupyter Notebooks (Analysis & Visualization):** A collection of Jupyter notebooks (Python) that perform exploratory analysis and generate the figures used in the manuscript:

  * **Network Construction & Metrics:** `NA.ipynb` (Network Analysis main workflow), `NAStats.ipynb` (network statistics calculations), `StatewiseClusteringCoef.ipynb` (compute clustering coefficients by state over time), `OzoneConcentration.ipynb` and `OzoneConcInCARBAndNonCARB.ipynb` (examining ozone concentration trends in CARB vs non-CARB states), among others. These notebooks build the ozone networks and compute metrics like degree, clustering coefficient, path lengths, etc., often on a per-year or per-state basis.
  * **Temporal/Regional Analysis:** Notebooks such as `Energy_OzoneMonitoringSites.ipynb` and `energy.ipynb` integrate energy data (from EIA) with ozone network metrics, while `NAPhily.ipynb` and `NAStats-Extreme.ipynb` explore specific case studies (e.g., extreme ozone events or specific regions like the Philadelphia area).
  * **Figure Reproduction:** Many notebooks correspond directly to figures in the paper, as indicated by their names:

    * `Figure2b.ipynb`, `Figure3a.ipynb`, `Hypothesis_Fig45.ipynb`, `CorrMonitoringClusteringCoefFig7ab.ipynb`, `OzoneMonitoringSites_fig7f.ipynb`, etc. – these generate sub-figures or perform analyses for Figures 2, 3, 4, 5, 7 (and possibly others) in the manuscript. For example, *Figure 4 and 5 analysis* is done in `Hypothesis_Fig45.ipynb`, and parts of *Figure 7* (clustering coefficient vs. monitoring sites) are produced in `CorrMonitoringClusteringCoefFig7ab.ipynb`.
    * Notebooks like `Figures1.ipynb` might correspond to supplemental or intermediary visualizations.
    * The notebooks often use the processed data (correlation matrices, etc.) to create final visualizations (charts, maps, tables) exactly as presented in the paper.

* **Visualization Scripts:** In addition to notebooks, several standalone Python scripts generate specific plots (often those used in the paper):

  * `plotBasemap.py`, `plotNA.py`, `plotCommunities.py` – routines for mapping networks on a US basemap (nodes and edges) and possibly community detection visuals.
  * `plotCarbNonCarbFigure4a.py`, `plotCarbNonCarbFigure7.py` (and `7c.py`) – scripts focusing on CARB vs non-CARB comparisons for specific figure panels (e.g., a plot comparing clustering coefficient trends for Figure 4a, and visualization for Figure 7 subplots).
  * `plotAbstractArt.py` – generates the Graphical Abstract visualization or a stylized network summary (the composite figure of map, distributions, etc., as shown above).
  * `plotChartFunctions.py` – helper functions for consistent plotting styles across different figures.

* **Dataset Directory:** `dataset/` – contains a `ReadMe.txt` with instructions for obtaining the data. (No raw data is stored in this repo due to size.) After downloading the data (see **Data Sources & Access** below), you should organize it as expected by the code (e.g., state folders or combined datasets as described). The code expects preprocessed data files (pickle and Excel) to be accessible at relative paths (for example, correlation matrices in subfolders like `USA/Correlations/o3/<Year>/correlations.pickle` or within state-specific directories).

*Note:* There is a large number of notebooks and scripts in this repository. Not every file may be needed for reproducing the main results – some are exploratory or legacy. Focus on the notebooks labeled by figure or topic for the core analyses used in the paper. Comments within code and markdown cells in notebooks provide additional context on the analysis steps.

## Installation & Requirements

This project uses **Python 3** (tested on Python 3.x) and a mix of scientific computing libraries. To set up the environment:

* **Python Dependencies:** The main libraries used include:

  * `pandas` and `numpy` for data manipulation and numerical computations.
  * `scipy` and `scikit-learn` (sklearn) for statistical analysis (e.g., significance testing, any machine learning if applicable).
  * `networkx` for constructing and analyzing networks/graphs.
  * `matplotlib` (plus `mpl_toolkits.basemap`) and `seaborn` for plotting graphs, maps, and charts.
  * `plotly` (optional, for interactive visualizations in some notebooks).
  * `pickle` (built-in) for reading/writing serialized data objects.
  * Other standard libraries: `os`, `csv`, `datetime`, `random`, `math`, etc., and utility modules provided in this repo (`commonFunctions.py`, etc.).
  * (Optional) `community` library for community detection (e.g., the Python Louvain modularity algorithm, if used in `plotCommunities.py`).
  * `xlsxwriter` or openpyxl if you need to re-export results to Excel (pandas will use these for writing `.xlsx` files).

  Ensure you have these installed. You can use `pip install -r requirements.txt` if such a file is provided, or install manually as needed.

* **R Requirements:** *If* using any R components (the analysis is primarily in Python; no direct `.R` scripts are included in this repository). However, if an R environment was used for any supplementary analysis or visualization, ensure you have a recent version of R and common packages (tidyverse, etc.). (By all indications, the provided code is in Python, so R setup may not be necessary unless specified by authors elsewhere.)

* **Environment Setup:** It is recommended to use a virtual environment or Conda environment. For example:

  ```bash
  conda create -n ozone-network python=3.9
  conda activate ozone-network
  pip install pandas numpy scipy scikit-learn networkx matplotlib basemap seaborn plotly
  ```

  (The Basemap toolkit may require additional steps to install, as it can be an older package; alternatively, the code may use a pre-drawn map background.)

* **Jupyter Notebooks:** To view and run the `.ipynb` files, you'll need Jupyter Notebook or JupyterLab. Launch Jupyter in the repository directory to get started:

  ```bash
  pip install jupyterlab
  jupyter lab
  ```

## Data Sources & Access

The analysis relies on multiple data sources, including raw environmental observations and energy statistics, as well as prepared datasets. Below is a summary of data sources and how to obtain them:

* **EPA Air Quality System (AQS) Data:** Ground-level ozone measurements and associated meteorological data (temperature, pressure, wind speed, relative humidity) were obtained from the U.S. EPA AQS *AirData* archive【7†】. Specifically, the study uses daily measurements from 1980 through 2017 for ozone and related variables, available through the EPA’s pre-generated data files repository. These files can be downloaded from the **EPA AirData Download site** (🌐 [aqs.epa.gov/aqsweb/airdata/download\_files.html](https://aqs.epa.gov/aqsweb/airdata/download_files.html)), which provides annual datasets for each pollutant and meteorological parameter. **Note:** You may need to download the “Daily Data” or “8-hour average ozone” files for each year and the corresponding meteorological data files (found under the *Criteria Gases* and *Meteorological* categories on the EPA site).

* **Energy Consumption & Production Data (SEDS/EIA):** State-level energy usage data were incorporated to analyze correlations between energy sector activity and ozone network changes. We used data from the U.S. Energy Information Administration’s **State Energy Data System (SEDS)**. These data (e.g., electricity generation, fuel consumption) can be accessed via the EIA portal. For example, the **EIA Electricity Grid Monitor** for the PJM interconnection region was used as a proxy for energy trends【7†】 (🌐 [eia.gov/electricity/gridmonitor/dashboard/electric\_overview/balancing\_authority/PJM](https://www.eia.gov/electricity/gridmonitor/dashboard/electric_overview/balancing_authority/PJM)). Users can retrieve similar state or regional energy datasets from the EIA website for the 1980–2017 period to replicate the analysis. (See EIA’s [State Energy Data System](https://www.eia.gov/state/seds/) for comprehensive state-level energy data.)

* **Preprocessed Dataset (Zenodo archive):** For convenience, all **preprocessed ozone network data** (correlation matrices, node lists, and summary metrics) are provided on Zenodo. The dataset is organized by state and year, containing correlation results ready for analysis. **Download the dataset** from Zenodo: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.13274569.svg)](https://doi.org/10.5281/zenodo.13274569). This archive (≈1.4 GB) includes yearly correlation matrices (in `.xlsx` and `.pickle` format) for each state, a compiled USA-level network, and summary files:

  * Each state has a folder with subfolders: `Correlations/o3/<Year>` containing `correlations.xlsx` (pairwise correlation matrix of sites) and corresponding `nodeNames.pickle`/`correlations.pickle` files for that year.
  * A `CorrelationsSummary` directory provides year-wise summary network metrics (e.g., number of edges, average clustering, etc.).
  * A `Data/o3` directory contains pickled time-series data used to compute the correlations.

  After downloading `data.zip` from Zenodo, **extract it into the repository folder**. You should have directories like `CA/Correlations/...`, `NY/Correlations/...`, etc., for each state (using EPA state codes or abbreviations), and possibly a `USA/` aggregate folder. Make sure the code can find these directories. (You can modify paths in the scripts or move the folders into the `dataset/` directory if needed.)

**Note on data usage:** The EPA and EIA data are publicly available. The Zenodo dataset is provided under the terms of this project’s license for transparency and reproducibility. If you use the preprocessed data, please cite the Zenodo archive (see [Citation](#citation) below).

## Usage Instructions

Once the environment is set up and data is in place, you can reproduce the analyses and figures. Below are general steps and examples to get started:

1. **Obtain and Prepare Data:** Download the preprocessed data from Zenodo (as described above) and extract it so that the code can access the files. By default, many scripts expect a relative path structure for data (you may place the extracted folders in the repository root or inside a `dataset` directory). If you prefer to start from raw data, adjust the scripts to point to the raw EPA data files and run the parsing/correlation scripts to generate the network data (this requires significant processing time and is not necessary if using the provided prepared data).

2. **Run Jupyter Notebooks for Analysis:** Open JupyterLab/Notebook in the repository. The main analyses can be run by executing the notebooks in a logical order:

   * It’s recommended to start with network construction or exploration notebooks (e.g., run `NA.ipynb` to construct or load the network for all states, then `NAStats.ipynb` to compute basic statistics).
   * To examine specific aspects, open the corresponding notebook. For example:

     * **Clustering coefficients over time:** Use `StatewiseClusteringCoef.ipynb` to compute and plot the average clustering coefficient per state for each year.
     * **Ozone trends in CARB vs non-CARB:** Run `OzoneConcInCARBAndNonCARB.ipynb` to visualize ozone concentration trends and perhaps network metrics differences in CARB vs other states.
     * **Energy vs Ozone Network:** Use `Energy_OzoneMonitoringSites.ipynb` to see how energy consumption/production trends relate to the number of monitoring sites or network connectivity.
   * Many notebooks are independent, but some may rely on outputs from others. Refer to any notes at the top of each notebook for prerequisites (e.g., some figure notebooks assume correlation matrices are already computed and saved by a parsing script).

3. **Generate Figures (Replication of Paper Figures):** For each figure in the paper, a dedicated notebook or script is provided:

   * Open the notebook matching the figure (for instance, to reproduce **Figure 3a**, open and run `Figure3a.ipynb`). It will typically load the necessary data (from pickle/Excel) and produce the plot. Ensure the paths in the notebook match where you placed the data.
   * For figure panels implemented as Python scripts (e.g., `plotCarbNonCarbFigure4a.py`), run them from the command line or an interactive session. For example:

     ```bash
     python plotCarbNonCarbFigure4a.py
     ```

     This should output the corresponding figure (often saved as an image file, e.g., `Figure4a.png` in the working directory).
   * Some complex figures with multiple subplots (like the Graphical Abstract or Figure 7) may require running several notebooks/scripts and assembling the subplots. The individual components (e.g., `CorrMonitoringClusteringCoefFig7ab.ipynb` for Fig 7a,b, and `OzoneMonitoringSites_fig7f.ipynb` for Fig 7f) can be run to generate sub-figures.

4. **Explore Network Properties:** You can interactively explore the ozone network using the provided code. For example, use `networkx` functions on the loaded graphs to calculate metrics not explicitly in the paper, or filter the network by threshold. The data structures (pickles) typically include adjacency matrices or edge lists that you can manipulate.

5. **Custom Analysis:** The repository can be adapted to analyze other aspects or updated data (e.g., extending beyond 2017 or focusing on a specific region). The parsing and correlation scripts are generalizable – by pointing to different input data, you can rebuild networks for different pollutants or time ranges. Use the `commonFunctions.py` for guidance on expected data formats.

**Reproducing Key Results:** All primary results in the manuscript (network metrics trends, CARB vs non-CARB comparisons, etc.) can be reproduced by running the relevant notebooks with the provided dataset. For instance, to reproduce the policy impact analysis figure (Figure 4 in the paper), ensure you have run the clustering coefficient calculations for all states, then run `Hypothesis_Fig45.ipynb` which will likely generate the comparison plot of clustering coefficient over time for CARB and non-CARB groups. This will illustrate the finding that CARB states maintain higher network clustering through the years compared to non-CARB states.

## Results Overview

The outputs of this project include both quantitative results and visualizations that align with the findings reported in the paper. Below is an overview of what the analysis produces and the insights gained:

* **Annual Ozone Networks:** For each year 1980–2017, a network graph is constructed where nodes are ozone monitoring locations (typically one per county) and weighted edges represent the strength of correlation in ozone levels between nodes. The network is usually thresholded by significance (only connections above a 99.9% significance level are kept). These networks show how interlinked ozone pollution is across different regions. Users can visualize these networks on the U.S. map (as in the Graphical Abstract map, or via `plotBasemap.py`), observing, for example, dense connectivity in industrial regions or urban corridors.

* **Network Metrics and Trends:** The repository computes various graph metrics for the ozone networks:

  * **Degree Distribution:** The distribution of connections per site tends to deviate from random, indicating that some sites (regions) consistently share ozone dynamics with many others. For example, the degree distribution plots (Graphical Abstract b) show the observed vs expected degree frequencies, highlighting more high-degree nodes than a random network would predict (suggesting key influencer regions).
  * **Clustering Coefficient:** A central focus is on how the **average clustering coefficient** of the network evolves over time, and how it differs between groups of states. Clustering coefficient measures the extent to which monitoring sites that are connected to the same site are also connected to each other (forming triads). The analysis finds that:

    * **CARB states** (with stricter emissions policies) exhibit **higher and more stable clustering coefficients** over time, indicating a robust, well-integrated ozone network among those states’ monitoring sites. In other words, ozone levels in CARB states tend to rise and fall in a more interconnected manner across sites, possibly reflecting effective region-wide pollution control and consistent environmental management.
    * **Non-CARB states** show a **declining clustering trend** over the decades, especially in the later years, suggesting that their ozone networks became less cohesive. This fragmentation could imply disparate ozone behavior and potentially less effective control strategies or more localized influences dominating by the end of the study period.
    * These patterns are visualized in plots (e.g., Figure 4 in the paper) comparing average clustering coefficient year-by-year for CARB vs. non-CARB groups, as well as maps highlighting states with increasing vs. decreasing trends.
  * **Correlation Strength Distribution:** The project also examines how the distribution of correlation coefficients between sites changes. The **cross-correlation distribution** (Graphical Abstract c) indicates the proportion of site-pairs with weak, moderate, or strong correlations. A shift toward weaker correlations over time in some regions might suggest more localized ozone behavior, whereas consistently strong correlations indicate widespread regional phenomena (possibly driven by large-scale meteorological patterns or uniform policy impacts).
  * **Network Connectivity & Components:** Metrics like the size of the largest connected component, network diameter, and average path length are calculated (and summarized in the Graphical Abstract table (e)). These offer a sense of how easily information (or pollution influence) percolates through the network. For instance, a decreasing diameter over time could imply that the ozone fluctuations became more synchronized nationally.
  * **Degree-Clustering Relationship:** The scatter plot of node degree vs. clustering (Graphical Abstract d) is generated to show whether highly connected sites also tend to have higher clustering. In many years, a positive correlation is observed: sites that interact with many others also form tight-knit clusters, reinforcing the idea of regional hubs of ozone co-variation.

* **Energy-Policy Analysis:** By incorporating energy consumption/production data, the project maps **energy sector trends to network changes**. In Figure 2 of the paper, for example, states are classified based on whether their energy usage was increasing and whether their ozone network clustering was increasing. The results categorize states as:

  * *Well-integrated networks:* states with rising energy activity that still managed to increase or maintain high ozone network clustering (suggesting policy measures kept pollution networks tight-knit despite economic growth).
  * *Poorly integrated networks:* states with rising energy activity but declining ozone network clustering, indicating that increased emissions might be outpacing policy controls, leading to more disparate ozone patterns.
  * *Borderline:* states with no clear trend or mixed signals.

  These findings help illustrate how policy stringency (like CARB adoption) and energy developments (industrial growth, changes in fuel use) jointly influence air quality networks. Visuals include U.S. maps color-coded by these categories and time-series plots.

* **Figures and Plots:** The repository reproduces all key figures of the manuscript:

  * **Time-series plots** of network metrics (e.g., clustering coefficient, number of edges) from 1980–2017.
  * **Comparative bar/line charts** contrasting CARB vs. non-CARB statistics (such as average degree or clustering in specific years of interest, e.g., before vs after major regulatory milestones).
  * **Maps** highlighting spatial patterns, like the density of ozone monitoring sites per state and how it changed (Figure 2a shows growth in sites in certain states in green vs decreases in purple), or network connectivity visuals overlaying geography.
  * **Statistical tables** summarizing metrics (as seen in Graphical Abstract e), possibly also provided in the notebooks for each year or overall.
  * **Hypothesis testing results:** The analysis might include statistical tests (z-tests, etc.) to confirm differences in network metrics between groups (mentioned in some notebook names). While the repository primarily focuses on descriptive analysis, any confirmatory tests or *p*-values would be noted in the notebooks if performed.

In summary, the results demonstrate that **network analysis offers a powerful lens to evaluate air quality management outcomes**. Ozone networks became more coherent in states with proactive policies, whereas other regions saw a breakdown in network structure over time. These insights support the conclusion that strong, consistent environmental regulations (like those in CARB states) can lead to more uniformly improved air quality, as reflected in the network connectivity of pollution data. Policy-makers can use such network-based evidence to identify regions where ozone management is lagging (fragmented networks) and investigate underlying causes.

## Citation

If you use this repository, code, or data in your research or policy analysis, please cite the following paper and data archive:

**Paper:**
Gujral, H., Jain, S., & Sinha, A. (2025). *Network Analysis of Ground-Level Ozone: Implications for Environmental Policy and Air Quality Management*. **Environmental Modelling & Software**, 157, 106502. DOI: 10.1016/j.envsoft.2025.106502

In BibTeX format:

```bibtex
@article{Gujral2025ozoneNetwork,
  title = {Network Analysis of Ground-Level Ozone: Implications for Environmental Policy and Air Quality Management},
  author = {Gujral, Harshit and Jain, Somya and Sinha, Adwitiya},
  journal = {Environmental Modelling \& Software},
  volume = {157},
  pages = {106502},
  year = {2025},
  doi = {10.1016/j.envsoft.2025.106502}
}
```

**Data & Code Archive:**
Gujral, H. (2024). *US Ozone Network (1980–2017) \[Data set]*. Zenodo. DOI: 10.5281/zenodo.13274569

In BibTeX format:

```bibtex
@dataset{Gujral2024ozoneData,
  author       = {Harshit Gujral},
  title        = {{US Ozone Network (1980-2017)}},
  year         = 2024,
  doi          = {10.5281/zenodo.13274569},
  note         = {Version 1.0, Preprocessed ozone network data supporting Gujral et al. (2025)}
}
```

*(If using this repository, you may also cite the GitHub repository or the specific commit for reproducibility. A DOI via Zenodo is provided above for the versioned archive of the data.)*

## License

This project is licensed under the **MIT License**. You are free to use, modify, and distribute the code and data in accordance with the MIT License terms. (See the `LICENSE` file for details.)

## Acknowledgments

This research was conducted by **Harshit Gujral**, **Somya Jain**, and **Adwitiya Sinha**. The development of the ozone network modeling approach and the analyses were carried out at the University of Toronto (Department of Computer Science) and collaborating institutions. The authors would like to thank **Prof. Steve Easterbrook** (University of Toronto) for his valuable insights and discussions, which significantly enriched this work. We also acknowledge the U.S. EPA and EIA for providing open access to air quality and energy data, without which this study would not have been possible.

Contributions: H. Gujral led the data analysis and code development (writing the original draft of the manuscript and software), S. Jain contributed to method development and result interpretation, and A. Sinha provided guidance on network science techniques and edited the manuscript.

Finally, we appreciate the open-source community and the developers of the Python libraries used in this project. Their tools enabled complex environmental data analysis and visualization in this work.
