# Spectral Decomposition of Identity-By-Descent Networks (SPC)

This repository includes scripts to calculate SPCs using IBD data.

## Dependencies

To run the main script `calculate_spc.py`, you need the following packages on Python (version 3.5 and above required):

- [Numpy](https://numpy.org/install/) (tested on 1.11 and later)
- [Networkit](https://networkit.github.io) (tested on 8.0 and later)
- [Scipy](https://scipy.org) (tested on 1.5.4 and later)

All packages can be installed using Python's package manager `pip`. We suggest setting up a new environment. This process is made convenient through Conda:

```
conda create -n spc_env python=3.9
```

Packages can either be installed through environment initiation command:

```
conda create -n spc_env python=3.9 scipy=1.8.1 numpy=1.22.3 networkit=10.0
```

or after the initiation and activation:

```
conda activate spc_env
pip install numpy==1.22.3 scipy==1.8.1 networkit==10.0
```

## Generating Global IBD network

The script called `generate_global_network.py` accepts a path to a directory that includes IBD segment information for all chromosomes divides in files. The IBD segment files should end in `.match` format. We currently only support iLASH output. The script can be modified to support other software. You can also contact us.The second argument for the script is the address for the resulting global network.

## Calculating SPCs

The main script `calculate_spc.py` can be run using the following command:

```
$ python calculate_spc.py
> usage: [-h] [-i INPUT] [-o OUTPUT] [-c COUNT] [-d DELIMITER]
```

The script has a 4 arguments:

- `--input` / `-i` the address of the global network file. It should be in a linked list format `<A> <B> <IBD>`, where A and B are participant IDs and IBD is the total length of shared IBD in centiMorgans.
- `--output` / `-o` the address for the output file.
- `--count` / `-c` the number of SPC dimentions to calculate. Default is 25.
- `--delimiter` / `-d` the delimiter in the global network file. Default is space.

