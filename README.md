
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
# Starlink-on-the-Autobahn Data Set
This repository contains the data used in our paper 
[Measuring Mobile Starlink Performance: A Comprehensive Look](https://ieeexplore.ieee.org/document/10877858). All measurements were conducted on a Autobahn ride from Osnabrück to Bunde, Germany. The number of samples varies depending on the type of measurement. Details of the measurement setup are presented in our paper. Aditionally, we provide stationary measurements conducted in Osnabrück, Germany, providing data to compate different dish types and data plans.

**Readme is work in progress, more information will be extended in the next days!**

**Due to size limitations, the data is only compressed available, we will transfer the repo soon to make it available in raw files.** 

## Dataset Structure
Dataset Structure

The collected data is located in the Data directory, which contains three subfolders:

* **Autobahn/**: Contains RTT measurements (via ping) and throughput measurements (via iperf3) recorded during the highway ride. Speed annotations are included.
* **Stationary/**: Provides RTT and throughput data collected under stationary conditions in Osnabrück. This includes comparisons between different Starlink dish types and data plans.
* **Emulation/**: Includes traces extracted from the Autobahn dataset to reproduce loss and non-loss states, facilitating controlled network experiments.



## Files
```
.
├── Analysis_Fig10_Fig11.ipynb # Notebook to reproduce plots from the paper
├── Analysis_Fig12_Fig13.ipynb # Notebook to reproduce plots from the paper
├── Analysis_Fig15.ipynb # Notebook to reproduce plots from the paper
├── Analysis_Fig16.ipynb # Notebook to reproduce plots from the paper
├── Analysis_Fig3_Fig5.ipynb # Notebook to reproduce plots from the paper
├── Analysis_Fig4_Fig6cd.ipynb # Notebook to reproduce plots from the paper
├── Analysis_Fig6ab.ipynb # Notebook to reproduce plots from the paper
├── Analysis_Fig7_Fig8.ipynb # Notebook to reproduce plots from the paper
├── create_testbed.sh # Script to setup the emulation environment
├── Data
│   ├── Autobahn # Data measured on the autobahn
│   │   ├── Bridges.csv # Bridges with coordinates along the route
│   │   ├── RTT_Bridges.csv # RTT mapped to bridges
│   │   ├── RTT_Loss_Bridges.csv # RTT and Loss mapped to bridges
│   │   ├── RTT_Loss.csv # RTT and Loss measurements
│   │   ├── RTT_trace_with_bridges.csv
│   │   ├── Throughput_Bridges.csv # Throughput with mapped bridges
│   │   └── throughput.csv # Throughput measurements
│   ├── Emulation # Date to reproduce the emulation
│   │   ├── loss_time_bridge_trace.csv # Loss trace for emulation with bridge information
│   │   ├── loss_time_trace.csv # Loss trace for emulation
│   │   ├── output_47G_00.csv # Throughput data of file transfer experiment with loss
│   │   └── output_47G_01.csv # Thorughput data of file transfer experiment without loss
│   └── Stationary # Contains Stationary measurement data
│       ├── RTT_FHP.csv # RTT data measured with FHP dish
│       ├── RTT_Loss_FHP.csv # RTT and Loss data measured with FHP dish
│       ├── RTT_Roam.csv # RTT data measured in the Roam data plan
│       ├── RTT_Standard.csv # RTT data measured in the Standard data plan
│       ├── throughput_FHP.csv # Throughput measurements with FHP
│       ├── throughput_Roam.csv # Throughput measured using the Roam data plan
│       └── throughput_Standard.csv # Throughput measured using the Standard data plan
├── loss_emulation.py # Script to run the loss emulation
└── README.md
``` 

## Emulation Howto
0. Install pandas using pip (pip install pandas)
1. Run create\_testbed.sh to create the network namespaces etc.
2. Create a random file to transfer (dd if=/dev/urandom of=random\_47GB\_file.bin bs=1M count=47104)
3. Start a minimal python webserver inside the server side namespace (ip netns exec ns2 python3 -m http.server)
4. Run the emulation script (python loss\_emulation.py)


## Citation 
D. Laniewski, E. Lanfer and N. Aschenbruck, "Measuring Mobile Starlink Performance: A Comprehensive Look," in IEEE Open Journal of the Communications Society, doi: 10.1109/OJCOMS.2025.3539836.

```
@ARTICLE{10877858,
  author={Laniewski, Dominic and Lanfer, Eric and Aschenbruck, Nils},
  journal={IEEE Open Journal of the Communications Society}, 
  title={Measuring Mobile Starlink Performance: A Comprehensive Look}, 
  year={2025},
  volume={},
  number={},
  pages={1-1},
  keywords={Satellite constellations;Extraterrestrial measurements;Satellites;Automobiles;Sea measurements;Road transportation;Orbits;Velocity measurement;Urban areas;Standards;Dataset;Flat High Performance;LEO;LEO Measurement;Measurement;Mobility;Satellite Communication;Starlink;Starlink Dataset;Starlink Measurement;Starlink Mobility},
  doi={10.1109/OJCOMS.2025.3539836}}

```
## License
This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/).


