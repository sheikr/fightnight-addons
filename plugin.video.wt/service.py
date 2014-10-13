# -*- coding: utf-8 -*-

import os,datetime,xbmc,xbmcplugin,xbmcgui,xbmcaddon
dataPath = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo("profile")).decode("utf-8")

class main:
    def __init__(self):
        while (not xbmc.abortRequested):

            if xbmcaddon.Addon().getSetting("lib-updateauto") == 'true' and xbmcaddon.Addon().getSetting("lib-serieson") == 'true':
                try:
                    t1 = datetime.datetime.strptime(xbmcaddon.Addon().getSetting("service_run"), "%Y-%m-%d %H:%M:%S.%f")
                    t2 = datetime.datetime.now()
                    hoursList = [2, 5, 10, 15, 24]
                    interval = int(xbmcaddon.Addon().getSetting("service_interval"))
                    update = abs(t2 - t1) > datetime.timedelta(hours=hoursList[interval])
                    if update == False: raise Exception()
                    if not (xbmc.Player().isPlaying() or xbmc.getCondVisibility('Library.IsScanningVideo')):
                        xbmc.executebuiltin('RunPlugin(plugin://plugin.video.wt/?mode=38&name=subs&url=nada)')
                        xbmcaddon.Addon().setSetting('service_run', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
                except:
                    pass
            xbmc.sleep(1000)

main()
