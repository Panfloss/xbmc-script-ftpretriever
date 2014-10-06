import xbmcgui
import sys

errors = []
language = None

class SyncProgressBarBG(object):
    "class to handle the background progressbar"

    _pDialog = None
    _addon_name = None

    def __init__(self, heading):
        "create the DialogProgressBG "

        language = sys.modules["__main__"].language
        self._addon_name = heading

        self._pDialog = xbmcgui.DialogProgressBG()
        self._pDialog.create(heading, language(32000))

    def update(self, percent, msg):
        "wrap the update function"

        self._pDialog.update(percent, message=msg)

    def update_file_dl(self, file, tot_files, file_number):
        "specialized update fn for when downloading file"

        text = language(32001).format(file_number, tot_files, file)

        self._pDialog.update(file_number*100 / tot_files, message=text)

    def update_profile(self, tot_profile, profile_number):
        "specialized update fn for when changing profile"

        self._pDialog.update(profile_number*100 / tot_profile , heading=self._addon_name + " " + language(32002).format(profile_number, tot_profile), message=language(32000))

    def close(self):
        """
        close the progress bar
        """

        self._pDialog.close()


def ftpConnectionError(profile_number, error):
    """
    Function adding connection errors to the list of errors
    """
    errors.append(language(33001).format(profile_number, error))

def notifyErrors():
    """
    Pop an ok dialog box if some errors occured
    """

    if errors != []:
        message = "\n".join(errors)
        xbmcgui.Dialog().ok("XBMC FTP Retriever", language(33000) + message)
