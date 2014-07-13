import ftp
import ui
import settings
import xbmc
import xbmcaddon
import os
import json

__addon__ = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')
__profile__ = xbmc.translatePath(__addon__.getAddonInfo('profile')).decode("utf-8")

profilePB = ui.SyncProgressBarBG(__addonname__ + " : Total progress") #PB wich will show the "profile progression"
profiles, profile_qtt = settings.getSettings()
profile_ongoing = 0

for index in range(len(profiles)):
    if profiles[index]["activated"] == False:
        continue
    profile_ongoing += 1
    profilePB.update_profile(profile_qtt, profile_ongoing, profiles[index]["host"])
    ftpInstance = ftp.FtpSession(profiles[index], index)
    ftpInstance.sync_folder()

profilePB.close()
