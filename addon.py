import resources.lib.sync_ftp as sync_ftp
import xbmc
import xbmcaddon as xa

PLUGIN_ID = "service.ftpretriever"
addon = xa.Addon(PLUGIN_ID)

settings = {}
settings["host"] = addon.getSetting("host")
settings["user"] = addon.getSetting("username")
settings["passwd"] = addon.getSetting("password")
settings["local_folder"] = "addon.getSetting("local_folder")
settings["distant_folder"] = addon.getSetting("distant_folder")



sync_ftp.sync_folder(settings['host'], settings['user'], settings['passwd'], settings['local_folder'], settings['distant_folder'])
