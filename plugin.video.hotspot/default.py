# -*- coding: utf-8 -*-

""" Hotspot Connector
    2014 fightnight"""

import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys

####################################################### CONSTANTES #####################################################

versao = '0.0.06'
addon_id = 'plugin.video.hotspot'
art = '/resources/art/'
user_agent = 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.102 Safari/537.36'
selfAddon = xbmcaddon.Addon(id=addon_id)
ptwifiURL= 'https://wifi.meo.pt/HttpHandlers/HotspotConnection.asmx/'
ptwifiUsername = selfAddon.getSetting('ptwifi-username')
ptwifiPassword = selfAddon.getSetting('ptwifi-password')
noswifiUsername = selfAddon.getSetting('noswifi-username')
noswifiPassword = selfAddon.getSetting('noswifi-password')
wtpath = selfAddon.getAddonInfo('path').decode('utf-8')
iconpequeno=wtpath + art + 'logo32.png'
mensagemok = xbmcgui.Dialog().ok
mensagemprogresso = xbmcgui.DialogProgress()
pastaperfil = xbmc.translatePath(selfAddon.getAddonInfo('profile')).decode('utf-8')
cookie_nos = os.path.join(pastaperfil, "cookienos.lwp")
traducao= selfAddon.getLocalizedString #apagar
               
################################################### MENUS PLUGIN ######################################################

def menu_principal():
      if selfAddon.getSetting('ptwifiactivo') == 'true':
            addDir('MEO WiFi',ptwifiURL,1,wtpath + art + 'meowifi.png',1,True)
      if selfAddon.getSetting('noswifiactivo') == 'true':
            addDir('NOS Wifi by Fon',ptwifiURL,5,wtpath + art + 'noswifi.png',1,True)
      addDir("Definições | [COLOR blue][B]Hotspot Connector[/B][/COLOR]",'nada',4,wtpath + art + 'defs.png',6,False)
      xbmc.executebuiltin("Container.SetViewMode(500)")

def ptwifi():
      try:
            ptwifi=abrir_url(ptwifiURL + 'GetStateResponse') #info inicial
            if re.search('<IsLogged>true</IsLogged>',ptwifi):
                  try: addLink('[B][COLOR blue]Login: [/COLOR][/B]'+re.compile('<Login>(.+?)</Login>').findall(ptwifi)[0],'',wtpath + art + 'meowifi.png')
                  except: pass
                  try: addLink('[B][COLOR blue]Tráfego Transferido na Sessão: [/COLOR][/B]'+re.compile('<DownstreamMB>(.+?)</DownstreamMB>').findall(ptwifi)[0] + ' MB','',wtpath + art + 'meowifi.png')
                  except: pass
                  try: addLink('[B][COLOR blue]Tráfego Enviado na Sessão: [/COLOR][/B]'+re.compile('<UpstreamMB>(.+?)</UpstreamMB>').findall(ptwifi)[0] + ' MB','',wtpath + art + 'meowifi.png')
                  except: pass
                  try: addLink('[B][COLOR blue]Tempo de Sessão: [/COLOR][/B]'+re.compile('<Time>(.+?)</Time>').findall(ptwifi)[0]+'h','',wtpath + art + 'meowifi.png')
                  except: pass
                  addDir('',ptwifiURL,10,wtpath + art + 'meowifi.png',1,False)
                  addDir('[B][COLOR white]Fazer Logoff[/COLOR][/B]',ptwifiURL,2,wtpath + art + 'meowifi.png',1,False)
            else:
                  addDir('[B][COLOR white]Iniciar Sessão[/COLOR][/B] com [B][COLOR blue]' + ptwifiUsername + '[/COLOR][/B]',ptwifiURL + 'Login?usr=' + ptwifiUsername,3,wtpath + art + 'meowifi.png',1,False)
                  addDir('',ptwifiURL,10,wtpath + art + 'meowifi.png',1,False)
                  addDir('[B][COLOR blue]Sem sessão iniciada[/COLOR][/B]',ptwifiURL,10,wtpath + art + 'meowifi.png',1,False)
                  
      except urllib2.HTTPError, e:
            mensagemok('Hotspot Connector',str(urllib2.HTTPError(e.url, e.code, "Erro na página.", e.hdrs, e.fp)))
            sys.exit(0)
      except urllib2.URLError, e:
            mensagemok('Hotspot Connector',"Está ligado à rede MEO WiFi?", "Se sim, aguarde 1/2 minutos e tente novamente.",'Volte a reconnectar a rede caso o erro continue.')
            sys.exit(0)            

def ptwifi_iniciasessao():
      post='{username:"'+ptwifiUsername+'", password:"'+ptwifiPassword+'"}'
      req=urllib2.Request(url, post)
      req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
      req.add_header("Content-type", "application/json")
      req.add_header('Accept', 'application/json, text/javascript, */*; q=0.01')
      req.add_header('Host','wifi.meo.pt')
      req.add_header('Origin','https://wifi.meo.pt')
      req.add_header('Referer','https://wifi.meo.pt/pt/Pages/Homepage.aspx')
      req.add_header('X-Requested-With','XMLHttpRequest')
      try:
            page=urllib2.urlopen(req).read()
            if re.search('"ERROR-FAULT"',page): mensagemok('Hotspot Connector',"Conta inválida.")
            elif re.search('"ERRO-2"',page): mensagemok('Hotspot Connector',"Estás num hotspot ptwifi?")
            else:
                  xbmc.executebuiltin("XBMC.Notification(Hotspot Connector,Login efectuado,'10000',"+iconpequeno.encode('utf-8')+")")
                  xbmc.executebuiltin("XBMC.Container.Refresh")            
      except urllib2.HTTPError, e:
            mensagemok('Hotspot Connector',str(urllib2.HTTPError(e.url, e.code, "Erro na página.", e.hdrs, e.fp)))
            sys.exit(0)
      except urllib2.URLError, e:
            mensagemok('Hotspot Connector',"Está ligado à rede MEO WiFi?", "Se sim, aguarde 1/2 minutos e tente novamente.",'Volte a reconnectar a rede caso o erro continue.')
            sys.exit(0)            

def ptwifi_terminasessao():
      abrir_url(ptwifiURL + 'Logoff')
      xbmc.executebuiltin("XBMC.Notification(Hotspot Connector,Logoff efectuado,'10000'," + iconpequeno.encode('utf-8')+")")
      xbmc.executebuiltin("XBMC.Container.Refresh")  

def addLink(name,url,iconimage):
      liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name } )
      liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)

def noswifi():
        #obrigado darkstar pelos tiros a escura
        checkurl = "http://example.com"
        html=abrir_url_cookie(checkurl)
        
        if html.find('action="https://nos.portal.fon.com') >= 0:
            print "Info inicial: " + str(html)
            m = re.search('action="(https://nos.[^"]+)"',html)
            if(m == None):
                  mensagemok('Hotspot Connector',"Actionurl não encontrado.","Volte a tentar mais tarde.")
                  return
            
            actionUrl = m.group(1)

            from t0mm0.common.net import Net
            net=Net()
            net.set_cookies(cookie_nos)
            data = {'USERNAME' : noswifiUsername, 'PASSWORD' : noswifiPassword,'remember':'on'}
            ref_data = {'User-Agent':user_agent}
            html= net.http_POST(actionUrl,form_data=data,headers=ref_data).content.encode('latin-1','ignore')

            print "Teste Login: " + str(html)

            m = re.search('<div class="error"><span>([^<]+)<br /></span></div>', html)
            if(m == None):                
                
                try: addLink('[B]Login efectuado ou não necessário[/B]','',wtpath + art + 'noswifi.png')
                except: pass
            else:
                try: addLink(m.group(1),'',wtpath + art + 'noswifi.png')
                except: pass
        else:
            try: addLink('[B]Login efectuado ou não necessário[/B]','',wtpath + art + 'noswifi.png')
            except: pass
            
def addDir(name,url,mode,iconimage,total,pasta):
      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
      liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name} )
      liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)

def abrir_url(url):
      req = urllib2.Request(url)
      req.add_header('User-Agent', user_agent)
      response = urllib2.urlopen(req)
      link=response.read()
      response.close()
      return link

def abrir_url_cookie(url):
      from t0mm0.common.net import Net
      net=Net()
      net.set_cookies(cookie_nos)
      try:
            link=net.http_GET(url).content.encode('latin-1','ignore')
            return link
      except urllib2.HTTPError, e:
            mensagemok('Hotspot Connector',str(urllib2.HTTPError(e.url, e.code, 'Erro a abrir página', e.hdrs, e.fp)),traducao(40200))
            sys.exit(0)
      except urllib2.URLError, e:
            mensagemok('Hotspot Connector',traducao(40199) + ' ' + 'Erro a abrir página')
            sys.exit(0)
            
def entrarnovamente(opcoes):
      if opcoes==1: selfAddon.openSettings()
      addDir('Entrar novamente',MainURL,28,wtpath + art + 'refresh.png',1,True)
      addDir('Alterar definições',MainURL,20,wtpath + art + 'defs.png',1,True)
      
def versao_disponivel():
      try:
            link=abrir_url('http://fightnight-xbmc.googlecode.com/svn/addons/wareztuga/plugin.video.wt/addon.xml')
            match=re.compile('name="wareztuga.tv"\r\n       version="(.+?)"\r\n       provider-name="wareztuga">').findall(link)[0]
      except:
            ok = mensagemok('wareztuga.tv',traducao(40184),traducao(40185),'')
            match=traducao(40186)
      return match

def get_params():
      param=[]
      paramstring=sys.argv[2]
      if len(paramstring)>=2:
            params=sys.argv[2]
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'):
                  params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                  splitparams={}
                  splitparams=pairsofparams[i].split('=')
                  if (len(splitparams))==2:
                        param[splitparams[0]]=splitparams[1]                 
      return param

def clean(text):
      command={'\r':'','\n':'','\t':'','\xC0':'À','\xC1':'Á','\xC2':'Â','\xC3':'Ã','\xC7':'Ç','\xC8':'È','\xC9':'É','\xCA':'Ê','\xCC':'Ì','\xCD':'Í','\xCE':'Î','\xD2':'Ò','\xD3':'Ó','\xD4':'Ô','\xDA':'Ú','\xDB':'Û','\xE0':'à','\xE1':'á','\xE2':'â','\xE3':'ã','\xE7':'ç','\xE8':'è','\xE9':'é','\xEA':'ê','\xEC':'ì','\xED':'í','\xEE':'î','\xF3':'ó','\xF5':'õ','\xFA':'ú'}
      regex = re.compile("|".join(map(re.escape, command.keys())))
      return regex.sub(lambda mo: command[mo.group(0)], text)
            
params=get_params()
url=None
name=None
mode=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass


print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
      print "Versao Instalada: v" + versao
      if ptwifiUsername=='' and noswifiUsername=='': selfAddon.openSettings()
      menu_principal()
elif mode==1: ptwifi()
elif mode==2: ptwifi_terminasessao()  
elif mode==3: ptwifi_iniciasessao()
elif mode==4: selfAddon.openSettings()
elif mode==5: noswifi()
                       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
