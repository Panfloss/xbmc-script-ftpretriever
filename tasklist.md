Task List
=========

- [ ] create a filter for tasklist (like .gitignore)
- [ ] prevent script from crashing if a file or a folder is not accessible
- [ ] prevent script from crashing if a folder is already synced (and check if everything in it is rightly synced : after crash recovery)
- [ ] allow to sync to a smb:// or other special mount point with xbmc.cvfs
- [ ] use multi-threading for multiple ftp syncs??
- [x] add a notification when the download start and when it's over
- [x] make ignore_list an argument of sync folder and store it with xbmc addon_data
- [x] reorganise ftp_sync : it should allow the creation of an object that represent the ftp session and have method to sync folder
- [X] use a progress bar to show when the addon is working (dialogProgressBG)
