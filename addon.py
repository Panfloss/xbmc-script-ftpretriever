import resources.lib.sync_ftp as sync_ftp
import xbmc
import xbmcaddon as xa

#PLUGIN_ID = "service.ftpretriever"
__addon__ = xa.Addon()#PLUGIN_ID)
__profile__ = xbmc.translatePath(__addon__.getAddonInfo('profile') ).decode("utf-8")


host = __addon__.getSetting("host")
user = __addon__.getSetting("username")
passwd = __addon__.getSetting("password")
local_folder = __addon__.getSetting("local_folder")
distant_folder = __addon__.getSetting("distant_folder")



sync_ftp.sync_folder(host, user, passwd, local_folder, distant_folder)
