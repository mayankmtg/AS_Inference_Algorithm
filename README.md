# [Knownpath]/[AS Inference] Algorithm

An implementation of [Knownpath Algorithm](https://ieeexplore.ieee.org/abstract/document/4150657?section=abstract)

## Installation

### Create Virtual environment and insall requirements
```bash
python3 -m venv knownpathenv
```
```bash
source knownpathenv/bin/activate
```
```bash
pip install -r requirements.txt
```

### Create Postgres database
- Install postgres
- Create postgres database instance
- Edit database configurations in ```config/config.yml```

### Download raw BGP collections

Download BGP raw data files from [routeviews archive](http://archive.routeviews.org/).

The file format is ```.bz2```. Extract the file and use [zebra-dump-parser](https://github.com/rfc1036/zebra-dump-parser) to obtain the routeview ribs. (Change the value of $format variable in zebra-dump-parser.pl file to 2):

```sh
$ bzip2 -d <filename>.bz2
$ cat <filename> | perl <path>/zebra-dump-parser.pl > '<filename>.rib' 2> dump-error
```

This gives the corresponding rib file that contains the IP prefix and AS path like:

```sh
$ head <filename>.rib
0.0.0.0/0 53767 3257
1.0.0.0/24 57463 13335
1.0.0.0/24 701 2914 13335
...
```

Similarly extract all the files from multiple vantage points and save the .rib files to data/ directory.

### Creating Tables

For the first run create tables in database

```sh
$ cd app/
$ python app.py -c True
$ cd ../
```

### Populating Tables

If the tables are empty that means we need to process raw BGP data and store them in usable indexed format. Make sure that the data is present in data/ directory.

```sh
$ cd app/
$ python app.py -p True
$ cd ../
```
