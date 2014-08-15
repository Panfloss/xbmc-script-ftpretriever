import xbmcgui
import sys


class SyncProgressBarBG(object):
    "class to handle the background progressbar"

    _pDialog = None

    def __init__(self, heading):
        "create the DialogProgressBG "

        self._pDialog = xbmcgui.DialogProgressBG()
        self._pDialog.create(heading, self.language(32000))
        
        self.language = sys.modules["__main__"].language

    def update(self, percent, msg):
        "wrap the update function"

        self._pDialog.update(percent, message=msg)

    def update_file_dl(self, file_name, tot_files, file_number):
        "specialized update fn for when downloading file"

        self._pDialog.update(file_number*100 / tot_files, message=self.language(32001).format(file_number, tot_files, file_name))

    def update_profile(self, tot_profile, profile_number, profile_host):
        "specialized update fn for when changing profile"

        self._pDialog.update(profile_number*100 / tot_profile , message=self.language(32002).format(profile_number, tot_profile, profile_host))

    def close(self):
        """
        close the progress bar
        """

        self._pDialog.close()
