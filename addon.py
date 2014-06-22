import resources.lib.sync_ftp as sync_ftp
import xbmc
import xbmcaddon
import os
import json

__addon__ = xbmcaddon.Addon()
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')
__profile__ = xbmc.translatePath(__addon__.getAddonInfo('profile') ).decode("utf-8")


host = __addon__.getSetting("host")
user = __addon__.getSetting("username")
passwd = __addon__.getSetting("password")
local_folder = __addon__.getSetting("local_folder")
distant_folder = __addon__.getSetting("distant_folder")

xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,"FTP retrieving is starting", 5000, __icon__))

try:
    os.chdir(__profile__)
    with open("ignore_list.json", "r") as file:
        ignore_list = json.load(file)
except:
    ignore_list = ""

ftpInstance = sync_ftp.FtpSession(host, user, passwd)

ignore_list = ftpInstance.sync_folder(local_folder, distant_folder, ignore_list)

os.chdir(__profile__)
with open("ignore_list.json", "w") as file:
    json.dump(ignore_list, file, sort_keys=True, indent=4, separators=(',', ': '))


xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,"FTP retrieving is finished", 5000, __icon__))
