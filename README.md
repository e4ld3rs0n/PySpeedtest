# PySpeedtest
 
A very simple internet speed logger written in Python. Uses speedtest-cli API. It is intended
to be used as a cron job on Linux machines.

## Usage

This script is intended to be used on a Nethesis device with crontab to periodically log internet speeds in a file. The idea is to make it work 

The basic usage is as follows:

```bash
$ pyspeedtest.py -o <output file>
```

## Requirements

It relies on the `speedtest-cli` package. Either install the package with your Linux package manager:

```bash
$ sudo yum install speedtest-cli
```

```bash
$ sudo apt install speedtest-cli
```

...or install the Python package, either system-wide or in a virtual environment:

```bash
$ pip3 install speedtest-cli
```

## Available options

- `-o FILENAME`, `--output FILENAME`: Mandatory, the output log file
- `-f FORMAT`, `--format FORMAT`: The format of the log file. Available formats: `csv` (CSV, default), `txt` (plaintext), `md` (markdown)
- `-s SEPARATOR`, `--separator SEPARATOR`: The separator character to use (default is ;)