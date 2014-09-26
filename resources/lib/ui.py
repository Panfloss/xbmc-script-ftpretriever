import xbmcgui
import sys


class SyncProgressBarBG(object):
    "class to handle the background progressbar"

    _pDialog = None
    _addon_name = None

    def __init__(self, heading):
        "create the DialogProgressBG "

        self.language = sys.modules["__main__"].language
        self._addon_name = heading
        
        self._pDialog = xbmcgui.DialogProgressBG()
        self._pDialog.create(heading, self.language(32000))

    def update(self, percent, msg):
        "wrap the update function"

        self._pDialog.update(percent, message=msg)

    def update_file_dl(self, file, tot_files, file_number):
        "specialized update fn for when downloading file"
        
        text = self.language(32001).format(file_number, tot_files, file)
        
        #resize "name" if it does not fit in the progress bar (50 chars wide)
        excess = len(text) - 50
        if excess > 0:
            file = file[:len(file)*2/3 - (excess/2)] + file[len(file)*2/3 + (excess/2)+1:]
            text = self.language(32001).format(file_number, tot_files, file)
        
        self._pDialog.update(file_number*100 / tot_files, message=text)

    def update_profile(self, tot_profile, profile_number):
        "specialized update fn for when changing profile"

        self._pDialog.update(profile_number*100 / tot_profile , heading=self._addon_name + " " + self.language(32002).format(profile_number, tot_profile), message=self.language(32000))

    def close(self):
        """
        close the progress bar
        """

        self._pDialog.close()
