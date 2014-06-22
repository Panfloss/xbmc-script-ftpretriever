import resources.lib.sync_ftp as sync_ftp
import xbmc
import xbmcaddon
import xbmcgui
import os
import json

__addon__ = xbmcaddon.Addon()
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')
__profile__ = xbmc.translatePath(__addon__.getAddonInfo('profile') ).decode("utf-8")


pDialog = xbmcgui.DialogProgressBG()
pDialog.create(__addonname__, 'Accessing credentials')

host = __addon__.getSetting("host")
user = __addon__.getSetting("username")
passwd = __addon__.getSetting("password")
local_folder = __addon__.getSetting("local_folder")
distant_folder = __addon__.getSetting("distant_folder")

pDialog.update(5, message='Recovering list of up to date files')

try:
    os.chdir(__profile__)
    with open("ignore_list.json", "r") as file:
        ignore_list = json.load(file)
except:
    ignore_list = ""


pDialog.update(10, message='File retrieving in progress...')

ftpInstance = sync_ftp.FtpSession(host, user, passwd)

ignore_list = ftpInstance.sync_folder(local_folder, distant_folder, ignore_list)

pDialog.update(95, message='Updating list of up to date files')

os.chdir(__profile__)
with open("ignore_list.json", "w") as file:
    json.dump(ignore_list, file, sort_keys=True, indent=4, separators=(',', ': '))

pDialog.update(100, message=' ')
pDialog.close()
