import os
import json
from ftplib import FTP

class FtpSession(object):

    _ftp = None
    _tasklist = []
    _ftp_folders = []

    def __init__(self, host, user, passwd, tasklist = []):

        self._host = host
        self._user = user
        self._passwd = passwd

    def _connect_ftp(self):
        """initiate the ftp sesion"""
        self._ftp = FTP(self._host, user=self._user, passwd=self._passwd)

    def _is_folder(self, item):
        """Check if item is a file (False) or a folder (return nlst(folder))"""

        content = self._ftp.nlst(item)
        if len(content) == 1 and content[0] == item:
            return False
        else:
            return content

    def _populate_tasklist(self, folders):
        """make the recursion for creating a tasklist"""
        for item in folders:
            content = self._is_folder(item)
            if content is False:
                self._tasklist.append(item)
            else:
                self._populate_tasklist(content)

    def _create_tasklist(self, ignore_list = []):
        """Generate the list of file to get
        wrapper for recursive function
        """

        for item in _ftp_folders:
            content = self._ftp.nlst(item)
            ignored = []
            for elt in content:
                if elt in ignore_list:
                    ignored.append(elt)

            for elt in ignored:
                content.remove(elt)

            self._populate_tasklist(content)

    def _save_tasklist(self):
        """save the tasklist as a json file"""

        #save tasklist as a json in __profile__
        pass

    def _create_hierarchy(self, file_path):
        """create the folder hierarchy for the file"""

        for folder in self._ftp_folders:
            if file_path[:len(folder)] == folder:
                file_path = file_path[len(folder):]
            if file_path[0] == '/':
                file_path = file_path[1:]

        file_path = file_path.split("/")

        if len(file_path) > 1:
            path = ""
            for folder in file_path[:-1]:
                path += folder + "/"
                try:
                    os.mkdir(path)
                except:
                    pass


    def _execute_tasks(self):
        """Sequentialy execute download tasks"""

        while self._tasklist != "":
            file_path = self._tasklist[0]
            self._create_hierarchy(file_path)
            with open(file_path, "wb") as file:
                self._ftp.retrbinary('RETR %s' % name, file.write)
            self._tasklist.pop(0)
            self._save_tasklist()
            #update progressbar


    def sync_folder(self, local_folder, ftp_folders, ignore_list):
        """Recursivly sync a FTP folder
        """

        self._ftp_folders = ftp_folders

        self._connect_ftp()
        os.chdir(local_folder)


        ignore_list = []
        for folder in fpt_folders:
            ignore_list += self._ftp.nlst(folder)

        self._ftp.quit()
        return ignore_list
