import os
import json
from ftplib import FTP

class FtpSession(object):

    _ftp = None

    def __init__(self, host, user, passwd):

        self._host = host
        self._user = user
        self._passwd = passwd

    def _connect_ftp(self):
        """initiate the ftp sesion"""
        self._ftp = FTP(self._host, user=self._user, passwd=self._passwd)

    def _populate_lists(self, file_list, folder_list):
        """Populate the file_list and folder_list
        It assumes that _ftp.dir() will return a UNIX formated string
        """

        complete_list = []
        self._ftp.dir(complete_list.append)

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


    def _get_folder(self, ignore_list=""):
        """retrieve the content of a folder via FTP
        It ignores links
        """

        file_list = []
        folder_list = []

        self._populate_lists(file_list, folder_list)

        if ignore_list is not "":
            for item in file_list:
                if item in ignore_list:
                    file_list.remove(item)

            for item in folder_list:
                if item in ignore_list:
                    folder_list.remove(item)


        for name in file_list:
            with open(name, "wb") as file:
                self._ftp.retrbinary('RETR %s' % name, file.write)

        for name in folder_list:
            try:
                self._ftp.cwd(name)
                os.mkdir(name)
                os.chdir(name)
                self._get_folder(name)
            except:
                pass #if retrieving a folder is not possible just go to the next

            self._ftp.cwd("..")
            os.chdir("..")


    def sync_folder(self, local_folder, distant_folder, ignore_list):
        """Recursivly sync a FTP folder
        It ignores links
        """

        self._connect_ftp()
        os.chdir(local_folder)

        self._ftp.cwd(distant_folder)
        self._get_folder(ignore_list)
        ignore_list = self._ftp.nlst()

        self._ftp.quit()
        return ignore_list
