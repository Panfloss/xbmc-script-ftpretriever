import settings
import xbmcvfs
import ui
import json
from ftplib import FTP

import xbmcgui #put it in ui.py after

class FtpSession(object):

    def __init__(self, profile, index, progress):

        self._host = profile["host"]
        self._user = profile["user"]
        self._passwd = profile["passwd"]
        self._local_folder = profile["local_folder"]
        self._ftp_folders = profile["ftp_folders"]
        self._include = profile["include_list"]
        self._ignore = profile["ignore_list"]
        self._deeds_list = profile["deeds_list"]
        self._inprogress = profile["inprogress"]
        self._tasklist = []

        self._profile_index = index

        self._progressBar = progress


    def _connect_ftp(self):
        """initiate the ftp sesion"""
        try:
            self._ftp = FTP(self._host, user=self._user, passwd=self._passwd)
        except error_perm:
            xbmcgui.Dialog().ok("an error occured", "Username or password incorect")
            return False
        
        return True

    def _is_folder(self, item):
        """Check if item is a file (False) or a folder (return nlst(folder))"""

        content = self._ftp.nlst(item)
        if len(content) == 1 and content[0] == item:
            return False
        else:
            return content

    def _create_tasklist(self, folders):
        """Generate the tasklist recursively
        """

        for item in folders:
            content = self._is_folder(item)
            if content is False:
                self._tasklist.append(item)
            else:
                self._create_tasklist(content)

    def _filter_tasklist(self):
        """
        Remove element already on deeds_list
        and element matching with ignore_list
        Allow only element matching include_list if it is populated
        make sure that if there is an inprogress item it is put first on the list
        """

        filtered = []
        stopedinprogress = self._inprogress in self._tasklist

        if self._inprogress is not "" and stopedinprogress:
            filtered.append(self._inprogress)

        #make sure no element already downloaded is in tasklist
        for elt in self._tasklist:
            if elt in self._deeds_list:
                filtered.append(elt)

        if self._include != None:
            #make sure each element in tasklist match include list
            for elt in self._tasklist:
                if self._include.search(elt) is None:
                    if elt not in filtered:
                        filtered.append(elt)

        if self._ignore != None:
            #make sure no element in tasklist match ignore list
            for elt in self._tasklist:
                if self._ignore.search(elt) is not None:
                    if elt not in filtered:
                        filtered.append(elt)

        for elt in filtered:
            self._tasklist.remove(elt)

        if self._inprogress is not "" and stopedinprogress:
            self._tasklist.insert(0, self._inprogress)

    def _filter_deeds_list(self):
        """
        Remove element no more on the distant folder (not in tasklist this time)
        """

        filtered = []

        for elt in self._deeds_list:
            if elt not in self._tasklist:
                filtered.append(elt)

        for elt in filtered:
            self._deeds_list.remove(elt)
            
    
    def _get_relative_path(self, file_path):
        """
        get the relative path of a file
        the path without the server 'ftp_folder' or the 'local_folder' prefix
        """
        
        #isolate the hierachy from ftp_folder
        for folder in self._ftp_folders:
            if file_path[:len(folder)] == folder:
                file_path = file_path[len(folder):]
                
            if file_path[0] == '/':
                file_path = file_path[1:]

        return file_path
        
    def _make_local_path(self, relative_path):
        """
        get the local path from the relative path
        """
        
        if self._local_folder[-1] == "/":
            local_path = self._local_folder + relative_path
        else:
            local_path = self._local_folder + "/" + relative_path
            
        return local_path
            
            
    def _create_hierarchy(self, file_path):
        """create the folder hierarchy for the file"""

        file_path = file_path.split("/")
        folder_path = "/".join(file_path[:-1])

        try:
            xbmcvfs.mkdirs(folder_path)
        except:
            pass

    def _execute_tasks(self):
        """Sequentialy execute download tasks"""

        tot_files = len(self._tasklist)
        file_number = 0

        while len(self._tasklist) > 0:
            file_path = self._tasklist[0]

            file_name = file_path.split("/")[-1]
            file_number += 1

            local_path = self._make_local_path(self._get_relative_path(file_path))
            self._create_hierarchy(local_path)
            
            if file_path is self._inprogress or not xbmcvfs.exists(local_path):
                self._progressBar.update_file_dl(file_name, tot_files, file_number)
                settings.saveInprogress(file_path, self._profile_index)
                file = xbmcvfs.File(local_path, "wb")
                self._ftp.retrbinary('RETR %s' % file_path, file.write)
                file.close()

            settings.saveInprogress("", self._profile_index)
            self._deeds_list.append(self._tasklist.pop(0))
            settings.saveDeedsList(self._deeds_list, self._profile_index)

    def sync_folder(self):
        """Recursivly sync a FTP folder
        """

        if self._connect_ftp() :
            self._create_tasklist(self._ftp_folders)
            self._filter_deeds_list()
            self._filter_tasklist()
    
            self._execute_tasks()
    
            self._ftp.quit()
        else :
            pass
            # add a notification explaining the situation here or in _connect_ftp
