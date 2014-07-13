import json
import xbmcaddon

__addon__ = __addon__ = xbmcaddon.Addon()

def getSettings():
    """
    Return the addon settings as a list of dict, each representing a ftp profile
    and the number of activated profiles as an int
    """
    profiles = []
    activated_profiles = 5

    for i in range(5):
        profiles.append({})
        if __addon__.getSetting("activate" + str(i)) == "true":
            profiles[i]["activated"] = True
            profiles[i]["host"] = __addon__.getSetting("host" + str(i))
            profiles[i]["user"] = __addon__.getSetting("username" + str(i))
            profiles[i]["passwd"] = __addon__.getSetting("password" + str(i))
            profiles[i]["local_folder"] = __addon__.getSetting("local_folder" + str(i))

            profiles[i]["ftp_folders"] = __addon__.getSetting("distant_folders" + str(i))
            profiles[i]["ftp_folders"] = profiles[i]["ftp_folders"].split(",")
            for j in range(len(profiles[i]["ftp_folders"])): #remove whitespace at the begining of folderpath
                while profiles[i]["ftp_folders"][j][0] == " ":
                    profiles[i]["ftp_folders"][j] = profiles[i]["ftp_folders"][j][1:]

            profiles[i]["ignore_list"] = __addon__.getSetting("ignore_list" + str(i))
            try:
                profiles[i]["ignore_list"]= json.loads(profiles[i]["ignore_list"])
            except ValueError:
                profiles[i]["ignore_list"] = []

            profiles[i]["deeds_list"] = __addon__.getSetting("deeds_list" + str(i))
            try:
                profiles[i]["deeds_list"] = json.loads(profiles[i]["deeds_list"])
            except ValueError:
                profiles[i]["deeds_list"] = []
        else:
            profiles[i]["activated"] = False
            activated_profiles -= 1

    return profiles, activated_profiles

def saveDeedsList(deeds_list, profile_index):
    """
    save the tasklist in the addon config
    """
    json_list = json.dumps(deeds_list, separators=(',',':'))
    __addon__.setSetting("deeds_list" + str(profile_index), json_list)

def saveIgnoreList(ignore_list, profile_index):
    """
    save the ignore_list in the addon config
    """
    json_list = json.dumps(ignore_list, separators=(',',':'))
    __addon__.setSetting("ignore_list" + str(profile_index), json_list)
