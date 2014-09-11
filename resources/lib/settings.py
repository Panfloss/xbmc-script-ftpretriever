import json
import re
import xbmcaddon

__addon__ = xbmcaddon.Addon()

def getIncludeList(index):
    """
    Return a re compile expression for files to include
    """
    if __addon__.getSetting("useInclude" + str(index)) == "false":
        return None
    else:
        includeList = []
        if __addon__.getSetting("includeVids" + str(index)) == "true":
            includeList.append("\.avi$")
            includeList.append("\.mkv$")
            includeList.append("\.mp4$")
            includeList.append("\.webm$")
            includeList.append("\.mov$")
            includeList.append("\.m4v$")
            includeList.append("\.srt$")
            includeList.append("\.sub$")
        if __addon__.getSetting("includeAudio" + str(index)) == "true":
            includeList.append("\.mp3$")
            includeList.append("\.aac$")
            includeList.append("\.ogg$")
            includeList.append("\.oga$")
            includeList.append("\.wma$")
            includeList.append("\.wav$")
            includeList.append("\.flac$")
            includeList.append("\.alac$")
        if __addon__.getSetting("includeImg" + str(index)) == "true":
            includeList.append("\.jpg$")
            includeList.append("\.jpeg$")
            includeList.append("\.png$")
            includeList.append("\.bpm$")
            includeList.append("\.gif$")
            includeList.append("\.webp$")

        return re.compile("|".join(includeList), re.I)

def getIgnoreList(index):
    """
    Return a re compile expression for files to ignore
    """
    if __addon__.getSetting("useIgnore" + str(index)) == "false":
        return None
    else:
        ignoreList = []
        if __addon__.getSetting("ignoreNfo" + str(index)) == "true":
            ignoreList.append("\.nfo$")
            ignoreList.append("\.info$")
            ignoreList.append("\.txt$")
            ignoreList.append("\.meta$")
        if __addon__.getSetting("ignoreSample" + str(index)) == "true":
            ignoreList.append("/sample/")

    return re.compile("|".join(ignoreList), re.I)

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
                if profiles[i]["ftp_folders"][j] == "":
                    continue
                while profiles[i]["ftp_folders"][j][0] == " ":
                    profiles[i]["ftp_folders"][j] = profiles[i]["ftp_folders"][j][1:]

            profiles[i]["ignore_list"] = getIgnoreList(i)

            profiles[i]["include_list"] = getIncludeList(i)

            profiles[i]["deeds_list"] = __addon__.getSetting("deeds_list" + str(i))
            try:
                profiles[i]["deeds_list"] = json.loads(profiles[i]["deeds_list"])
            except ValueError:
                profiles[i]["deeds_list"] = []
                
            profiles[i]["inprogress"] = __addon__.getSetting("inprogress" + str(i))

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

def saveInprogress(inprogress, profile_index):
    """
    save the inprogress string in the addon config
    """
    
    __addon__.setSetting("inprogress" + str(profile_index), inprogress)

def saveIgnoreList(ignore_list, profile_index):
    """
    save the ignore_list in the addon config
    """
    json_list = json.dumps(ignore_list, separators=(',',':'))
    __addon__.setSetting("ignore_list" + str(profile_index), json_list)
