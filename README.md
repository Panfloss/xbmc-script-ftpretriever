xbmc-ftp-sync-addon
===================

An XBMC addon to retrieve ftp content

It download the content of selected FTP folders using a matching and an ignore list.
Each file is only downloaded once even if you delete it localy so you can use a temporary folder to download to

### Roadmap
* 0 .1.0 :
 * ability to sync one folder with an ignore list out of the receiver folder
* 0.2.0:
 * Multiple sync profiles
 * Better notification(actually progressing progress bar)
 * can handle shutdown during process
* 0.3.0:
 * implemente xbmc.cvfs to manage different protocols for local_folder
