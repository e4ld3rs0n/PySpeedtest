# PySpeedtest
 
A very simple internet speed logger written in Python. Uses speedtest-cli API. It is intended
to be used as a cron job on NethServer machines.

## Usage

This script is intended to be used on a Nethesis device with crontab to periodically log internet speeds in a file. The basic usage is as follows:

```bash
$ pyspeedtest.py -o <output file>
```

## Requirements

It relies on the `speedtest-cli` package (present by default on NethServer). If it's missing, either install the package with your Linux package manager:

```bash
$ sudo yum install speedtest-cli
```

...or install the Python package directly with `pip`:

```bash
$ pip3 install speedtest-cli
```

## Installation and use

The idea is to run this script using crontab. For example run `crontab -e` in a terminal and add:

```
0 * * * * /usr/bin/python3 /root/pyspeedtest.py -o /root/netspeedlog.csv
```

The script writes logs into `/var/log/pyspeedtest.log` to simplify troubleshooting. This path is hard-coded and you can change it by editing the script directly.

## Available options

- `-h`, `--help`: Display available options and exit
- `-o FILENAME`, `--output FILENAME`: Mandatory, the file where to save the test results
- `-f FORMAT`, `--format FORMAT`: The format of the results file. Available formats are: `csv` (CSV, default), `txt` (plaintext), `md` (markdown)
- `-s SEPARATOR`, `--separator SEPARATOR`: The separator character to use for CSV (the default is ';')

