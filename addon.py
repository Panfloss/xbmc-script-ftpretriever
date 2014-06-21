import resources.lib.sync_ftp as sync_ftp
import xbmc
import xbmcaddon as xa
import os
import json

__addon__ = xa.Addon()
__profile__ = xbmc.translatePath(__addon__.getAddonInfo('profile') ).decode("utf-8")


host = __addon__.getSetting("host")
user = __addon__.getSetting("username")
passwd = __addon__.getSetting("password")
local_folder = __addon__.getSetting("local_folder")
distant_folder = __addon__.getSetting("distant_folder")

try:
    os.chdir(__profile__)
    with open("ignore_list.json", "r") as file:
        ignore_list = json.load(file)
except:
    ignore_list = ""

ignore_list = sync_ftp.sync_folder(host, user, passwd, local_folder, distant_folder, ignore_list)

os.chdir(__profile__)
with open("ignore_list.json", "w") as file:
    json.dump(ignore_list, file, sort_keys=True, indent=4, separators=(',', ': '))
