import os
import json
from ftplib import FTP

__FTP_SES__ = None

def init_ftp(host, user, passwd):
    """Initiate the __FTP_SES__ global variable"""

    global __FTP_SES__
    if __FTP_SES__ is None:
        __FTP_SES__ = FTP(host, user=user, passwd=passwd)
    else:
        raise RuntimeError("a FTP session has already been activated.")


def populate_lists(file_list, folder_list):
    """Populate the file_list and folder_list
    It assumes that __FTP_SES__.dir() will return a UNIX formated string
    """

    global __FTP_SES__

    complete_list = []
    __FTP_SES__.dir(complete_list.append)

    for item in complete_list:
        if item[0] == "d":
            folder_list.append(" ".join(item.split()[8:]))
        elif item.split()[0][0] == "-":
            file_list.append(" ".join(item.split()[8:]))
        #add the handling of symlinks?

    try:
        folder_list.remove(".")
        folder_list.remove("..")
    except:
        pass


def get_folder(ignore_list=""):
    """retrieve the content of a folder via FTP
    It ignores links
    """

    global __FTP_SES__

    file_list = []
    folder_list = []

    populate_lists(file_list, folder_list)

    if ignore_list is not "":
        for item in file_list:
            if item in ignore_list:
                file_list.remove(item)

        for item in folder_list:
            if item in ignore_list:
                folder_list.remove(item)


    for name in file_list:
        with open(name, "wb") as file:
            __FTP_SES__.retrbinary('RETR %s' % name, file.write)

    for name in folder_list:
        try:
            __FTP_SES__.cwd(name)
            os.mkdir(name)
            os.chdir(name)
            get_folder(name)
        except:
            pass #if retrieving a folder is not possible just go to the next

        __FTP_SES__.cwd("..")
        os.chdir("..")


def sync_folder(host, user, passwd, local_folder, distant_folder, ignore_list):
    """Recursivly sync a FTP folder
    It ignores links
    """

    global __FTP_SES__

    init_ftp(host, user, passwd)
    os.chdir(local_folder)

    __FTP_SES__.cwd(distant_folder)
    get_folder(ignore_list)
    ignore_list = __FTP_SES__.nlst()

    __FTP_SES__.quit()
    return ignore_list
