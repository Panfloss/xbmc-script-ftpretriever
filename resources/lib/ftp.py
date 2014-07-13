import settings
import os
import ui
from ftplib import FTP

class FtpSession(object):

    def __init__(self, profile, index):

        self._host = profile["host"]
        self._user = profile["user"]
        self._passwd = profile["passwd"]
        self._local_folder = profile["local_folder"]
        self._ftp_folders = profile["ftp_folders"]
        self._ignore_list = profile["ignore_list"]
        self._deeds_list = profile["deeds_list"]

        self._tasklist = []

        self._profile_index = index

        self._progressBar = ui.SyncProgressBarBG(self._host + " : Progress")


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

    def _create_tasklist(self):
        """Generate the list of file to get
        wrapper for recursive function
        """

        for item in self._ftp_folders:
            content = self._ftp.nlst(item)
            ignored = []
            for elt in content:
                if elt in self._ignore_list:
                    ignored.append(elt)

            for elt in ignored:
                content.remove(elt)

            self._populate_tasklist(content)

        for elt in self._deeds_list:
            if elt in self._tasklist:
                self._tasklist.remove(elt)

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
                except OSError:
                    pass

        return "/".join(file_path)

    def _execute_tasks(self):
        """Sequentialy execute download tasks"""

        tot_files = len(self._tasklist)
        file_number = 0

        while len(self._tasklist) > 0:
            file_path = self._tasklist[0]

            file_name = file_path.split("/")[-1]
            file_number += 1
            self._progressBar.update_file_dl(file_name, tot_files, file_number)

            local_path = self._create_hierarchy(file_path)
            with open(local_path, "wb") as file:
                self._ftp.retrbinary('RETR %s' % file_path, file.write)
            self._tasklist.pop(0)
            settings.saveDeedsList(self._deeds_list, self._profile_index)

    def sync_folder(self):
        """Recursivly sync a FTP folder
        """

        self._connect_ftp()
        os.chdir(self._local_folder)

        self._create_tasklist()
        self._execute_tasks()

        self._ignore_list = []
        for folder in self._ftp_folders:
            self._ignore_list += self._ftp.nlst(folder)
        settings.saveIgnoreList(self._ignore_list, self._profile_index)

        settings.saveDeedsList([], self._profile_index)

        self._ftp.quit()
        self._progressBar.close()
