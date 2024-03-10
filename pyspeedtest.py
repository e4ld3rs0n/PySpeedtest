#!/usr/bin/env python3

from datetime import datetime
import argparse
import speedtest
import os.path

sysLogFilePath = "/var/log/pyspeedtest.log"

# TODO:
# - Handle exceptions (in case internet connection is absent or impossible)
# - Handle other output formats

def logAction(message, level='info'):
    global sysLogFilePath

    with open(sysLogFilePath, "a") as log:
        if level == 'info':
            log.write("[+] ")
        elif level == 'warning':
            log.write("[-] ")
        elif level == 'error':
            log.write("[!] ")
        else:
            log.write("[i] ")

        log.write(datetime.now().strftime("%H:%M:%S %d/%m/%Y"))
        log.write(" " + message + "\n")


def manageArgs():
    parser = argparse.ArgumentParser(
        usage='%(prog)s [options] -o <output file>',
        description="Internet speed tester using speedtest.net API.",
        epilog='Install the speedtest-cli package before use.'
    )

    parser.add_argument(
        '-o', '--output',
        help='File where to record the readings',
        required=True
    )

    parser.add_argument(
        '-f', '--format',
        choices={"csv", "xls", "md", "txt"},
        default='csv',
        help='Specify an output format (default is CSV)'
    )

    parser.add_argument(
        '-s', '--separator',
        default=';',
        help='Specify an alternative separator character'
    )

    return parser.parse_args()

def main():
    print_header = False
    args = manageArgs()

    if not os.path.isfile(args.output):
        print_header = True

    with open(args.output, '+a') as logfile:
        if print_header:
            # Date, Time, ISP, Download, Upload, Ping, Server
            if args.format == 'csv':
                header = f'Date{args.separator}Time{args.separator}Result{args.separator}ISP{args.separator}Download{args.separator}Upload{args.separator}Ping{args.separator}Server{args.separator}\n'
                logfile.write(header)
            elif args.format == 'xls':
                pass
            elif args.format == 'md':
                pass
            elif args.format == 'txt':
                pass

        # Test the speed
        servers = []
        threads = None
        now = datetime.now()

        logAction("Initiating speedtest...")
        try:
            s = speedtest.Speedtest()
        except speedtest.ConfigRetrievalError as e:
            logAction("Cannot connect to the network: " + str(e), 'error')

            now.strftime("%d/%m/%Y %H:%M:%S")
            resultStr = f'{now.strftime("%d/%m/%Y")}' + args.separator
            resultStr += f'{now.strftime("%H:%M:%S")}' + args.separator
            resultStr += f'FAIL' + args.separator
            resultStr += f'None' + args.separator
            resultStr += f'None' + args.separator
            resultStr += f'None' + args.separator
            resultStr += f'None' + args.separator
            resultStr += f'None' + args.separator

            logfile.write(resultStr + '\n')

            exit(1)

        logAction("Searching for the closest server...")
        s.get_servers(servers)
        s.get_best_server()

        logAction("Testing download speed...")
        s.download(threads=threads)

        logAction("Testing upload speed...")
        s.upload(threads=threads)
        results = s.results.dict()

        downloadf = float(results['download']) / 1000000
        uploadf = float(results['upload']) / 1000000
        pingf = float(results['ping'])

        # Date, Time, ISP, Download, Upload, Ping, Server
        now.strftime("%d/%m/%Y %H:%M:%S")
        resultStr = f'{now.strftime("%d/%m/%Y")}' + args.separator
        resultStr += f'{now.strftime("%H:%M:%S")}' + args.separator
        resultStr += f'SUCCESS' + args.separator
        resultStr += f'{results["client"]["isp"]}' + args.separator
        resultStr += f'{downloadf:.2f} Mbps' + args.separator
        resultStr += f'{uploadf:.2f} Mbps' + args.separator
        resultStr += f'{pingf:.2f} ms' + args.separator
        resultStr += f'{results["server"]["host"]}' + args.separator

        logfile.write(resultStr + '\n')

if __name__ == '__main__':
    main()
