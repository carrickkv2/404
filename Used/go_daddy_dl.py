import os
import subprocess
import sys
import time
import urllib.request


def download_from_godaddy(url_given):
    # Create the URL and filename
    url = url_given

    file_name = url.split('/')[-1]

    # Get the current directory
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)

    # Get the path for 7zip
    zip_path = str(application_path) + str(r'\7za.exe')

    # Dictionary for raw string function
    _dRawMap = {8: r'\b', 7: r'\a', 12: r'\f', 10: r'\n', 13: r'\r', 9: r'\t', 11: r'\v'}

    def get_raw_string(s: str) -> str:
        """Takes a filepath string and turns it into a raw string"""
        return r''.join(_dRawMap.get(ord(c), c) for c in s)

    def extract_files(zip_name):
        """Extracts the files using the 7zip exe"""
        system = subprocess.Popen([get_raw_string(zip_path), "e", zip_name])
        return system.communicate()

    # Start the download
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        print('File is downloading')
        file_size = response.getheader('content-length')
        file_size_dl = 0
        block_sz = 1296

        # For timing the download
        start_time = time.time()

        if file_size:
            file_size = int(file_size)
            block_sz = max(4096, file_size // 20)

        # Write the file to the system
        while True:
            buffer = response.read(block_sz)
            if not buffer:
                break

            if file_size:
                file_size_dl += len(buffer)
                out_file.write(buffer)
                done = int(30 * file_size_dl / int(file_size))
                sys.stdout.write(
                    "\r[%s%s] Speed is %s Mbps" % (
                        '=' * done, ' ' * (30 - done), file_size_dl // (time.time() - start_time) / 100000))
                percent = int((file_size_dl / file_size) * 100)
                print(f"\nDownload percentage is : {percent}% ")

    # Print to console when the download is done
    print(f'\nFile has finished downloading in {(time.time() - start_time) / 60} minutes')

    # Extract the downloaded file to the current folder
    # extract_files(file_name)

    input('\nPlease press enter to quit')
