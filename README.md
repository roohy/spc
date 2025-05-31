# Spectral Decomposition of Identity-By-Descent Networks (SPC)

This repository includes scripts to calculate SPCs using IBD data.

## Dependencies

To run the main script `calculate_spc.py`, the following Python packages are needed (Python 3.5 and above required):

- [Numpy](https://numpy.org/install/) (tested on 1.11 and later)
- [Networkit](https://networkit.github.io) (tested on 8.0 and later)
- [Scipy](https://scipy.org) (tested on 1.5.4 and later)

All packages can be installed using Python's package manager `pip`. Setting up a new environment is preferred. If Conda is available, new environments can be set using the following commands:

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

The script called `generate_global_network.py` can generate the similarity network file required for SPC calculation. It can be run using the following command:

```
$ python generate_global_network.py
```
The script has the following arguments:

- `--ibd-file-address`/`-i`: the address of the IBD file(s). If there are multiple IBD files (e.g. separated by chromosome),replace the chromosome number, or any other numerical index, with '@' in the address. E.g. /path/to/files/ibd_output_chr@.match
- `id1-column`,`id2-column`, `--ibd-column`: column index for the sample IDs of the individuals, along with that of the IBD length column, within the IBD file.
- `haploid-mode`: Use this flag if haplotypes codes have their own column, instead of a haplotype prefix within the same columns.
- `minimum-segment-length`: minimum length of IBD segments to be counted in the aggregation (default:3).
- `-minimum-agg-length`: minimum total length of IBD shared between a pair of individuals to be considered as an entry in the output file (defualt:6).
- `--sep`: separator in the IBD file. Use 't' for tab and 's' for space (default:'s').
- `--removal-file`:address of a file the includes sample IDs of the participants that should be excluded from the final file. e.g. closely related individuals
- `--output`: address for the output file.

<!-- accepts a path to a directory that includes IBD segment information for all chromosomes in separate files. The IBD segment files should end in `.match` format. We currently only support iLASH output. The script can be modified to support other software. You can also contact us.The second argument for the script is the address for the resulting global network. -->

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

