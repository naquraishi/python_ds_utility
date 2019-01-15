import os
import sys

####################################################################################################
# Example execution steps:
#For results in bytes
#c:\>python C:\Users\nafeez.quraishi\PycharmProjects\IV\disk_space_utility.py
#For results in human readable format
#c:\>python C:\Users\nafeez.quraishi\PycharmProjects\IV\disk_space_utility.py h
#For results with human readable format and directory path
#c:\>python C:\Users\nafeez.quraishi\PycharmProjects\IV\disk_space_utility.py h U:
#Results should look like following:
#c:\>python C:\Users\nafeez.quraishi.PN-HR-NB17\PycharmProjects\IV\disk_space_utility.py h U:\a
#file name: 1102OS_Codes.zip; size: 37MB
#file name: 9781783280698_code.zip; size: 4MB
#directory name: b; size: 362MB
#file name: jsf-jdbc-source-code-v2.zip; size: 19MB
#****************************************************************************************************
#Total disc space occupied by accessible/enlisted directories/files is: 422MB
#****************************************************************************************************
##Note: The utility is tested on Windows 10 and Ubuntu VM
######################################################################################################


def folder_size(path='.'):
    """folder_size function recursively calculate size of the folder and returns total size for the target folder"""
    total = 0
    for entry in os.scandir(path):
        if entry.is_file():
            total += entry.stat().st_size
        if entry.is_dir():
            total += folder_size(entry.path)
    return total


def disk_usage(fr='', p='.'):
    """disk_usage function takes two optional parameters : FIRST valid parameter is "h" without quotes for human
     readable format, SECOND parameter should be a valid directory path for which disk_usage has to be calculated.
     Without any parameters the utility shows files and directory for current directory in bytes. It uses os.scandir
    which is a relatively newer PEP addition, this increases speed of directory iteration by 2-20 times wrt earlier
    function os.walk. https://www.python.org/dev/peps/pep-0471/ for more details"""

    dir_total = 0
    with os.scandir(p) as itr:
        for e in itr:
            try:
                if e.is_dir():
                    if fr == 'h':
                        print("directory name: %s; size: %s" % (e.name, str(human_readable_bytes(folder_size(e.path)))))
                    else:
                        print("directory name: %s; size: %s" % (e.name, str(folder_size(e.path))))
                    dir_total += (folder_size(e.path))
                elif e.is_file():
                    file_total = e.stat().st_size
                    dir_total += file_total
                    if fr == 'h':
                        print("file name: %s; size: %s" % (e.name, str(human_readable_bytes(file_total))))
                    else:
                        print("file name: %s; size: %s" % (e.name, str(file_total)))
            except FileNotFoundError and PermissionError:
                continue

    if fr == 'h':
        print("*"*100 + "\nTotal disc space occupied by accessible/enlisted directories/files is: %s\n" %
              str(human_readable_bytes(dir_total)) + "*"*100 + "\n")
    else:
        print("*" * 100 + "\nTotal disc space occupied by accessible/enlisted directories/files is: %s\n" %
              str(dir_total) + "*" * 100 + "\n")


def human_readable_bytes(number_of_bytes):
    """ This function coverts number of bytes to approximate human readable format"""
    unit = ''
    if number_of_bytes < 0:
        raise ValueError("Number of bytes can not be smaller than 0")

    number_of_bytes = float(number_of_bytes)

    if 0 <= number_of_bytes < 1024:
        unit = 'B'
    if 1024 <= number_of_bytes < 10**6:
        number_of_bytes = round(number_of_bytes/1024)
        unit = 'KB'
    if 10**6 <= number_of_bytes < 10**9:
        number_of_bytes = round(number_of_bytes/10**6)
        unit = 'MB'
    if 10**9 <= number_of_bytes < 10**12:
        number_of_bytes = round(number_of_bytes / 10 ** 9)
        unit = 'GB'
    if 10**12 <= number_of_bytes < 10**15:
        number_of_bytes = round(number_of_bytes / 10 ** 12)
        unit = 'TB'

    return str(int(number_of_bytes)) + '' + unit


if __name__ == '__main__':

    if len(sys.argv) >= 3:
        fmt = str(sys.argv[1])
        pth = str(sys.argv[2])
        disk_usage(fmt, pth)

    elif len(sys.argv) == 2:
        fmt = str(sys.argv[1])
        disk_usage(fmt)

    else:
        disk_usage()
