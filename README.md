# Topological_Analysis
Analyze material structures using Voronoi analysis

## Introduction

Topological_Analysis is a Python library to analyze interstitial sites in oxides and sulfides, based on Voronoi analysis. It identifies potential interstitial sites for a given species, including original sites in the structure. The library provides several Python filters for site selection and a command-line executable script. The script produces CIF and CSV files showing the Voronoi radius of interstitial sites, their positions, bond valence, and other information. Topological_Analysis now supports Python 3.6+ environment.

## Features

- Analyze potential interstitial sites in crystal structures
- Calculate percolation paths for ion diffusion
- Compute bond valence and geometric constraints
- Visualize results with VMD command generation
- Support for CIF file analysis with YAML parameter configuration

## Dependencies

**The following software and Python libraries are required to use Topological_Analysis:**

- [Zeo++](http://www.zeoplusplus.org/) - **Must be installed separately** (see installation instructions)
- [Pymatgen](http://pymatgen.org/) (2022.0.0+)
- [NumPy](http://www.numpy.org/) (1.19.0+)
- [Pandas](https://pandas.pydata.org/) (1.2.0+)
- [Monty](https://materialsvirtuallab.github.io/monty/) (2021.0.0+)
- [PrettyTable](https://pypi.python.org/pypi/PrettyTable) (2.0.0+)
- [ruamel.yaml](https://pypi.org/project/ruamel.yaml/) (0.17.0+)
- [pyzeo](https://pypi.org/project/pyzeo/) (0.1+)
- [Cython](https://cython.org/) (0.29.0+)

## Important Note

As of March 6, 2025, this code requires a patch to pymatgen that is currently under review at https://github.com/materialsproject/pymatgen/pull/4315. Until this patch is merged, you may need to apply the patch manually or use a forked version of pymatgen.

## Installation

1. Create and activate a Python virtual environment (required):
   ```
   python -m venv topo_env
   source topo_env/bin/activate  # On Linux/macOS
   topo_env\Scripts\activate     # On Windows
   ```

2. Install Zeo++ (required):

   **Option 1: Manual Installation (Recommended)**
   
   Install Zeo++ following the instructions at http://www.zeoplusplus.org/

   **Option 2: Automatic Installation (Linux preferred)**
   
   You can use a convenience function to automatically install Zeo++ by adding the `--install-zeopp` flag:
   ```
   pip install .[install-zeopp]
   ```
   
   This will attempt to download, compile, and install Zeo++ in your virtual environment. While primarily tested on Linux, it may work on other platforms with appropriate development tools installed.


3. Alternatively, you can clone the repository and install:
   ```
   git clone https://github.com/materialsvirtuallab/Topological_Analysis.git
   cd Topological_Analysis
   pip install -e .  # For regular installation
   pip install .[install-zeopp]  # To also install Zeo++ (cannot use -e for zeo++ install!)
   ```

## Using the Command-Line Tool

The `analyze_voronoi_nodes` script requires 2 input files: a CIF file for the input structure and a YAML file for analysis parameters. The YAML file specifies percolation radius and other necessary information.

To run the script:
```
analyze_voronoi_nodes <cif_file> -i <yaml_file>
```

Run with `-h` flag to see documentation for other options:
```
analyze_voronoi_nodes -h
```

Example YAML parameter files are included in the repository:
- `examples/example.yaml` - Lists all usable parameters
- `examples/inputs.yaml` - Executable input file for oxides

## Examples

**Analysis of LGPS and Li2S structures**

To analyze LGPS (188887.cif), execute:
```
cd /your/directory/Topological_Analysis/examples/
analyze_voronoi_nodes 188887.cif -i inputs.yaml
```

Note: the input CIF file may contain disordered cation sites. The analysis code will replace disordered cation sites with lowest radius cation ions. However, the output structure will preserve the original disordered sites.

To use the VMD command lines, copy and paste the command line file contents to the VMD terminal.

## Filter Options

The analysis supports several filters that can be specified with the `-f` flag:
- `Ordered`: OrderFrameworkFilter - Handle disordered structures
- `PropOxi`: OxidationStateFilter - Check oxidation states
- `VoroPerco`: TAPercolateFilter - Check percolation radius
- `Coulomb`: TACoulombReplusionFilter - Apply Coulomb repulsion constraints
- `VoroBV`: TABvFilter - Apply bond valence constraints
- `VoroLong`: TALongFilter - Analyze node lengths
- `MergeSite`: OptimumSiteFilter - Optimize site prediction
- `VoroInfo`: Output center coordinates and length of each node

## Troubleshooting

If you encounter issues with Zeo++ or the pymatgen interface:

1. Ensure you're using a supported version of pymatgen with the necessary patch
2. Confirm Zeo++ is properly installed and accessible in your PATH
3. Check that your virtual environment is active
4. For compilation issues, ensure you have the appropriate development tools installed

## Citing Topological_Analysis

If you use Topological_Analysis in your research, please cite the original publication:

Xingfeng He, Qiang Bai, Yunsheng Liu, Adelaide M. Nolan, Chen Ling, Yifei Mo, "Crystal Structural Framework of Lithium Super-Ionic Conductors", Advanced Energy Materials 9, 1902078 (2019)  https://doi.org/10.1002/aenm.201902078
