# -*- coding: utf-8 -*-

""" Sapo Videos
    2014 fightnight
"""

import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys

####################################################### CONSTANTES #####################################################

versao = '0.1.00'
addon_id = 'plugin.video.sapo'
MainURL = 'http://videos.sapo.pt/'
vazio= []
art = '/resources/art/'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1'
selfAddon = xbmcaddon.Addon(id=addon_id)
sapopath = selfAddon.getAddonInfo('path')
mensagemok = xbmcgui.Dialog().ok
pastaperfil = xbmc.translatePath(selfAddon.getAddonInfo('profile')).decode('utf-8')
cookie_sapo = os.path.join(pastaperfil, "cookie_sapo.lwp")
from t0mm0.common.net import Net
net=Net()



def menu_principal():
      addDir("Top 10",MainURL,1,'',1)
      addDir("Destaques",MainURL,7,'',1)
      addDir("Directos",MainURL + 'directos.html',8,'',1)
      addDir("Categorias",MainURL + 'categorias.html',3,'',1)
      addDir("Pesquisar",MainURL,4,'',1)
      #addLink("",'','')
      #disponivel=versao_disponivel()
      #if disponivel==versao: addLink('Última versao instalada (' + versao+ ')','','')
      #else: addDir('Instalada v' + versao + ' | Actualização v' + disponivel,MainURL,4,'',1)

def pesquisa():
      keyb = xbmc.Keyboard('', 'Sapo Vídeos')
      keyb.doModal()
      if (keyb.isConfirmed()):
            search = keyb.getText()
            if search=='': sys.exit(0)
            encode=urllib.quote(search)
            urlfinal='http://videos.sapo.pt/ajax/search?q='+encode+'&type=videos&token='+file_token()+'&nocache='+get_random()+'&page=1'
            #urlfinal='http://videos.sapo.pt/ajax/search.php?word=' + encode + '&order=releve&version=2&epages=60'
            request(urlfinal)

def destaques():
      url=MainURL + 'ajax/destaques?token=' + file_token() + '&nocache=' + get_random() + '&page=1'
      request(url)

def directos():
      url=MainURL + 'ajax/lives?token=' + file_token() + '&nocache=' + get_random() + '&page=1'
      request(url)

def tops():
      get_token=file_token()
      addDir("Hoje",MainURL + 'ajax/top?token=' + get_token + '&nocache=' + get_random() + '&page=1&order=day',6,'',1)
      addDir("Última Semana",MainURL + 'ajax/top?token=' + get_token + '&nocache=' + get_random() + '&page=1&order=week',6,'',1)
      addDir("Último Mês",MainURL + 'ajax/top?token=' + get_token + '&nocache=' + get_random() + '&page=1&order=month',6,'',1)
      addDir("Desde Sempre",MainURL + 'ajax/top?token=' + get_token + '&nocache=' + get_random() + '&page=1&order=all',6,'',1)

def categorias():
      link=abrir_url(url)
      categorias=re.compile('small-40" href=".+?id=(.+?)"><img alt="(.+?)" src="(.+?)" />.+?<span class="vid-count">(.+?)</span>').findall(link)
      for end,nome,thumb,nrvideos in categorias:
            addDir('[B]%s[/B] (%s vídeos)' % (nome,nrvideos),MainURL + 'ajax/category/'+end+'?token=' + file_token() + '&nocache=' + get_random() + '&page=1&order=releve',6,thumb,1)
            
def file_token():
      cookies=openfile("cookie_sapo.lwp",pastaperfil)
      token=re.compile('sv_token=(.+?);').findall(cookies)[0]
      return token

def get_random():
      from random import randint
      random=str(randint(0, 10000))
      return random
             
def request(url):
      ref_data = {'Accept':'text/javascript,text/xml,application/xml,application/xhtml+xml,text/html,application/json;q=0.9,text/plain;q=0.8,video/x-mng,image/png,image/jpeg,image/gif;q=0.2,*/*;q=0.1','User-Agent':user_agent,'X-Ink-Version':'1','X-Requested-With':'XMLHttpRequest'}
      link= clean(abrir_url_cookie(url,ref_data))

      videos=re.compile('"title":"(.+?)".+?"randname":"(.+?)",.+?"views":(.+?),.+?"thumb_url":"(.+?)"').findall(link)
      for titulo,idend,views,thumb in videos:
            thumb=thumb.replace('\\','')
            #titulo=titulo.decode('latin-1','ignore').encode('utf-8')
            pastastream('[B]%s[/B] (%s visualizações)' % (titulo,views),MainURL + idend,5,thumb,len(videos))

def openfile(filename,pastafinal=pastaperfil):
    try:
        destination = os.path.join(pastafinal, filename)
        fh = open(destination, 'rb')
        contents=fh.read()
        fh.close()
        return contents
    except:
        print "Nao abriu os temporarios de: %s" % filename
        return None


def abrir_url_cookie(url,referencia):
      net.set_cookies(cookie_sapo)
      try:
            link=net.http_GET(url,referencia).content.encode('latin-1','ignore')
            return link
      except urllib2.HTTPError, e:
            mensagemok('wareztuga.tv',str(urllib2.HTTPError(e.url, e.code, "Erro na página", e.hdrs, e.fp)),"Volte a tentar.")
            sys.exit(0)
      except urllib2.URLError, e:
            mensagemok('wareztuga.tv',"Erro na pagina")
            sys.exit(0)

            
def captura(name,url):
      link=abrir_url(url)
      thumb=re.compile('<meta property="og:image" content="(.+?)"/>').findall(link)[0]
      username=re.compile("var usermrec='(.+?)'").findall(link)[0]
      if re.search('rtmp://',link):
            chname=url.replace('http://videos.sapo.pt/','')
            filepath=re.compile('/live/(.+?)&').findall(link)[0]
            host=abrir_url('http://videos.sapo.pt/hosts_stream.html')
            hostip=re.compile('<host>(.+?)</host>').findall(host)[0]
            if re.search('playersrc="',link):
                  jslink=re.compile('playersrc="(.+?)"').findall(link)[0]
                  jslink=jslink.split('.js')
                  swf=jslink[0]
                  swf=swf.replace('Video','flash/videojs.swf')
            else: swf='http://imgs.sapo.pt/sapovideo/swf/flvplayer-sapo.swf?v11'
            finalurl='rtmp://' + hostip + '/live' + ' playPath=' + filepath  + ' swfUrl='+swf+' live=true pageUrl=http://videos.sapo.pt/'+chname
      else:
            try:
                  endereco=re.compile('file=(.+?)&').findall(link)[0]
            except:
                  link=abrir_url(url + '/rss2')
                  video=re.compile('<media:content url="(.+?)/pic/').findall(link)[0]
                  endereco = video + '/mov'
            finalurl=redirect(endereco)
      comecarvideo(name,finalurl,username,thumb)


def comecarvideo(titulo,url,username,thumb):
      playlist = xbmc.PlayList(1)
      playlist.clear()
      listitem = xbmcgui.ListItem(titulo, iconImage="DefaultVideo.png", thumbnailImage=thumb)            
      listitem.setInfo("Video", {"Title":titulo, "TVShowTitle": username[0]})
      listitem.setProperty('mimetype', 'video/x-msvideo')
      listitem.setProperty('IsPlayable', 'true')
      dialogWait = xbmcgui.DialogProgress()
      #dialogWait.create('Sapo Videos', 'A carregar')
      playlist.add(url, listitem)
      xbmcplugin.setResolvedUrl(int(sys.argv[1]),True,listitem)
      #dialogWait.close()
      #del dialogWait
      xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
      xbmcPlayer.play(playlist)

################################################## PASTAS ################################################################

def addLink(name,url,iconimage):
      ok=True; liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name } )
      ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
      return ok

def pastastream(name,url,mode,iconimage,total):
      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
      ok=True; liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name } )
      ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=total)
      cm = []
      cm.append(('',''))
      liz.addContextMenuItems(cm, replaceItems=True)                      
      return ok

def addDir(name,url,mode,iconimage,total):
      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
      ok=True; liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name } )
      ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=total)
      return ok

def abrir_url(url):
      req = urllib2.Request(url)
      req.add_header('User-Agent', user_agent)
      response = urllib2.urlopen(req)
      link=response.read()
      response.close()
      return link

def versao_disponivel():
      try:
            link=abrir_url('http://fightnight-xbmc.googlecode.com/svn/addons/fightnight/plugin.video.sapo/addon.xml')
            match=re.compile('name="Sapo Videos"\r\n       version="(.+?)"\r\n       provider-name="fightnight">').findall(link)[0]
      except:
            ok = mensagemok('Sapo Videos','Addon não conseguiu conectar ao servidor','de actualização. Verifique a situação.','')
            match='Erro. Verificar origem do erro.'      
      return match


def redirect(url):
      req = urllib2.Request(url)
      req.add_header('User-Agent', user_agent)
      response = urllib2.urlopen(req)
      gurl=response.geturl()
      return gurl

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
      command={'&nbsp;':' ','&laquo;':'','&raquo;':'','&eacute;':'é','&iacute;':'í','&aacute;':'á','&oacute;':'ó','&uacute;':'ú','&ccedil;':'ç','&otilde;':'õ','&atilde;':'ã','&agrave;':'à','&acirc;':'â'}
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
      selfAddon.setSetting('nada',value='false') #ugly empty addon_data folder creator
      net.http_GET(MainURL)
      net.save_cookies(cookie_sapo)
      menu_principal()
        
elif mode==1: tops()
elif mode==2: canais()
elif mode==3: categorias()
elif mode==4: pesquisa()
elif mode==5: captura(name,url)
elif mode==6: request(url)
elif mode==7: destaques()
elif mode==8: directos()

#plugin://plugin.video.sapo/?mode=5&url=http://videos.sapo.pt/qAUkoLFQegUKv0jDDs33&name=Nomedovideo
  
xbmcplugin.endOfDirectory(int(sys.argv[1]))
