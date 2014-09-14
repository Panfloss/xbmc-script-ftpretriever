import resources.lib.ftp as ftp
import resources.lib.ui as ui
import resources.lib.settings as settings
import xbmc
import xbmcaddon

__addon__ = xbmcaddon.Addon(id="service.ftpretriever")
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')
language = __addon__.getLocalizedString

profilePB = ui.SyncProgressBarBG(__addonname__ + language(32010)) #PB wich will show the "profile progression"
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
