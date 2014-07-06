import xbmcgui


class SyncProgressBarBG(object):
    "class to handle the background progressbar"

    _pDialog = None

    def __init__(self, __addonname__):
        "create the DialogProgressBG "

        self._pDialog = xbmcgui.DialogProgressBG()
        self._pDialog.create(__addonname__, 'Accessing credentials')

    def update(self, percent, msg):
        "wrap the update function"

        self._pDialog.update(percent, message=msg)

    def update_file_dl(self, file_name, tot_files, file_number):
        "specialized update fn for when downloading file"

        self._pDialog.update(file_number/tot_files, message="downloading file {}/{} : {}" .format(file_number, tot_files, file_name))
