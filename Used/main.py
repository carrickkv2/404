import mediafire_dl
from go_daddy_dl import download_from_godaddy
from zip_extraction import extract_files
import time

try:
    url = 'https://www.mediafire.com'
    output = 'PerfectStorm.7z'
    mediafire_dl.download(url, output, quiet=False)
    print(' Attempting to extract the files')
    time.sleep(2)
    extract_files(output)
    input(' Files have been successfully extracted. Please press enter to quit')
except Exception as e:
    time.sleep(3)
    try:
        print('\n The Link included in the program does not work.')
        url = input(' Please enter a media fire link that downloads the mod files \n :')
        output = 'PerfectStorm.7z'
        mediafire_dl.download(url, output, quiet=False)
        print(' Attempting to extract the files')
        time.sleep(2)
        extract_files(output)
        input(' Files have been successfully extracted. Please press enter to quit')
    except Exception as e:
        time.sleep(3)
        try:
            print('\n The link given does not work, attempting to download from the slower server. \n')
            url = '  http://perfectstormmod.com/update/PerfectStorm.7z'
            output = 'PerfectStorm.7z'
            download_from_godaddy(url)  # Change this to the go daddy program
            print(' Attempting to extract the files')
            time.sleep(2)
            extract_files(output)
            input(' Files have been successfully extracted. Please press enter to quit')
        except Exception as e:
            time.sleep(3)
            print('\n The program encountered an issue. Please contact the Administrators of the perfect Storm Mod to'
                  ' Resolve this. Thank you.')
