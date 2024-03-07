#!/usr/bin/env python3

from datetime import datetime
import argparse, speedtest, os.path

# TODO:
# - Handle exceptions (in case internet connection is absent or impossible)
# - Handle other output formats

def manageArgs():
    parser=argparse.ArgumentParser(
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

    if(not os.path.isfile(args.output)):
        print_header = True

    with open(args.output, '+a') as logfile:
        if(print_header):
            # Date, Time, ISP, Download, Upload, Ping, Server
            match args.format:
                case 'csv':
                    header = f'Date{args.separator}Time{args.separator}ISP{args.separator}Download{args.separator}Upload{args.separator}Ping{args.separator}Server{args.separator}\n'
                    logfile.write(header)
                case 'xls':
                    pass
                case 'md':
                    pass
                case 'txt':
                    pass
        
        # Test the speed
        servers = []
        threads = None
        s = speedtest.Speedtest()

        print("[+] Searching for the closest server...")
        s.get_servers(servers)
        s.get_best_server()

        print("[+] Testing download speed...")
        s.download(threads=threads)

        print("[+] Testing upload speed...")
        s.upload(threads=threads)
        results = s.results.dict()

        now = datetime.now()

        downloadf = float(results['download']) / 1000000
        uploadf = float(results['upload']) / 1000000
        pingf = float(results['ping'])

        # Date, Time, ISP, Download, Upload, Ping, Server
        now.strftime("%d/%m/%Y %H:%M:%S")
        resultStr =  f'{now.strftime("%d/%m/%Y")}' + args.separator
        resultStr += f'{now.strftime("%H:%M:%S")}' + args.separator
        resultStr += f'{results['client']['isp']}' + args.separator
        resultStr += f'{downloadf:.2f} Mbps' + args.separator
        resultStr += f'{uploadf:.2f} Mbps' + args.separator
        resultStr += f'{pingf:.2f} ms' + args.separator
        resultStr += f'{results['server']['host']}' + args.separator

        logfile.write(resultStr + '\n')

if __name__ == '__main__':
    main()