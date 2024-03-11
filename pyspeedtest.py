#!/usr/bin/env python3

from datetime import datetime
import argparse
import speedtest
import os.path

SYS_LOG_FILE_PATH = "test.log" #"/var/log/pyspeedtest.log"

def log_action(message, level='info'):
    with open(SYS_LOG_FILE_PATH, "a") as log:
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


def manage_args():
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
        choices={"csv", "md", "txt"},
        default='csv',
        help='Specify an output format (default is CSV)'
    )

    parser.add_argument(
        '-s', '--separator',
        default=';',
        help='Specify an alternative separator character'
    )

    return parser.parse_args()


def write_header(logfile, args, format='csv'):
    if args.format == 'csv':
        header = f'Date{args.separator}Time{args.separator}Result{args.separator}ISP{args.separator}Download (Mbps){args.separator}Upload (Mbps){args.separator}Ping (ms){args.separator}Server{args.separator}\n'
        logfile.write(header)
    elif args.format == 'md':
        header = '| Date | Time | Result | ISP | Download | Upload | Ping | Server |\n'
        header += '| --- | --- | --- | --- | --- | --- | --- | --- |\n'
        logfile.write(header)
    elif args.format == 'txt':
        header = 'Date\t\tTime\t\tResult\t\tISP\tDownload\tUpload\tPing\tServer\n'
        logfile.write(header)
        pass


def write_result(logfile, args, result, format='csv', success=True):
    now = datetime.now()
    
    if format == 'csv':
        result_str = f'{now.strftime("%d/%m/%Y")}' + args.separator
        result_str += f'{now.strftime("%H:%M:%S")}' + args.separator

        if success:
            result_str += f'Completed' + args.separator
            result_str += f'{result["client"]["isp"]}' + args.separator
            result_str += f'{float(result["download"]) / 10**6:.2f}'.replace('.', ',') + args.separator
            result_str += f'{float(result["upload"]) / 10**6:.2f}'.replace('.', ',') + args.separator
            result_str += f'{float(result["ping"]):.2f}'.replace('.', ',') + args.separator
            result_str += f'{result["server"]["host"]}' + args.separator
        else:
            result_str += f'Failed' + args.separator
            result_str += f'None' + args.separator * 6
    elif args.format == 'md':
        result_str = f'| {now.strftime("%d/%m/%Y")} | '
        result_str += f'{now.strftime("%H:%M:%S")} | '

        if success:
            result_str += f'Completed | '
            result_str += f'{result["client"]["isp"]} | '
            result_str += f'{float(result["download"]) / 10**6:.2f} Mbps | '
            result_str += f'{float(result["upload"]) / 10**6:.2f} Mbps | '
            result_str += f'{float(result["ping"]):.2f} ms | '
            result_str += f'{result["server"]["host"]} |'
        else:
            result_str += f'Failed | ' + 'None | ' * 5
    elif args.format == 'txt':
        result_str = f'{now.strftime("%d/%m/%Y")}' + '\t'
        result_str += f'{now.strftime("%H:%M:%S")}' + '\t'

        if success:
            result_str += f'Completed\t'
            result_str += f'{result["client"]["isp"]}\t'
            result_str += f'{float(result["download"]) / 10**6:.2f} Mbps\t'
            result_str += f'{float(result["upload"]) / 10**6:.2f} Mbps\t'
            result_str += f'{float(result["ping"]):.2f} ms\t'
            result_str += f'{result["server"]["host"]}'
        else:
            result_str += f'Failed\t' + 'None\t' * 5
    
    logfile.write(result_str + '\n')


def main():
    args = manage_args()
    print_header = not os.path.isfile(args.output)

    with open(args.output, '+a') as logfile:
        if print_header:
            write_header(logfile, args, format=args.format)

        log_action("Initiating speedtest...")
        try:
            s = speedtest.Speedtest()
        except speedtest.ConfigRetrievalError as e:
            log_action("Cannot connect to the network: " + str(e), 'error')
            write_result(logfile, args, {}, format=args.format, success=False)
            exit(1)

        log_action("Searching for the closest server...")
        try:
            s.get_servers([])
            s.get_best_server()
        except speedtest.NoMatchedServers as e:
            log_action("No servers found: " + str(e), 'error')
            write_result(logfile, args, {}, format=args.format, success=False)
            exit(1)
        except speedtest.SpeedtestBestServerFailure as e:
            log_action("Request limit exceeded: " + str(e), 'error')
            write_result(logfile, args, {}, format=args.format, success=False)
            exit(1)

        log_action("Testing download speed...")
        try:
            s.download()
        except speedtest.SpeedtestDownloadTestError as e:
            log_action("Download test failed: " + str(e), 'error')
            write_result(logfile, args, {}, format=args.format, success=False)
            exit(1)

        log_action("Testing upload speed...")
        try:
            s.upload()
        except speedtest.SpeedtestUploadTestError as e:
            log_action("Upload test failed: " + str(e), 'error')
            write_result(logfile, args, {}, format=args.format, success=False)
            exit(1)
        
        results = s.results.dict()
        write_result(logfile, args, results, format=args.format, success=True)


if __name__ == '__main__':
    main()
