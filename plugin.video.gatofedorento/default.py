# -*- coding: utf-8 -*-

""" Gato Fedorento
    2014 fightnight"""

import xbmc, xbmcgui, xbmcaddon, xbmcplugin,re,sys, urllib, urllib2,time,datetime

versao = '0.0.04'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1'
addon_id = 'plugin.video.gatofedorento'
art = '/resources/art/'
selfAddon = xbmcaddon.Addon(id=addon_id)
tvporpath = selfAddon.getAddonInfo('path')
mensagemok = xbmcgui.Dialog().ok
menuescolha = xbmcgui.Dialog().select
pastaperfil = xbmc.translatePath(selfAddon.getAddonInfo('profile'))

def menu_principal():
    #if selfAddon.getSetting("mensagemfb") == "true":
    #        ok = mensagemok('wareztuga.tv','Faz like na pagina do facebook para','obteres todas as novidades.','http://fb.com/xxxxxxxxxxxx')
    #        selfAddon.setSetting('mensagemfb',value='false')
    addDir("Séries Completas",'nada',2,tvporpath + art + '',1,True)
    addDir("Sketchs Soltos",'nada',4,tvporpath + art + '',1,False)
    addDir("Procurar Vídeos",'nada',4,tvporpath + art + '',1,False)
    addDir("Quem são os Gato Fedorento?",'nada',4,tvporpath + art + '',1,False)
    addDir("",'',22,tvporpath + art + 'defs.png',1,False)
    disponivel=versao_disponivel()
    if disponivel==versao: addLink('Última versao (' + versao+ ')','',tvporpath + art + 'versao.png')
    else: addDir('Instalada v' + versao + ' | Actualização v' + disponivel,'nada',15,tvporpath + art + 'versao.png',1,False)
    addDir("Definições do addon",'',22,tvporpath + art + 'defs.png',1,False)

def abrir_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', user_agent)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

def versao_disponivel():
    try:
        link=abrir_url('http://fightnight-xbmc.googlecode.com/svn/addons/fightnight/plugin.video.gatofedorento/addon.xml')
        match=re.compile('name="Gato Fedorento"\r\n       version="(.+?)"\r\n       provider-name="fightnight">').findall(link)[0]
    except:
        ok = mensagemok('Gato Fedorento','Addon não conseguiu conectar ao servidor','de actualização. Verifique a situação.','')
        match='Erro. Verificar origem do erro.'
    return match

def seriescompletas():
    nrcanais=30
    addDir("Gato Fedorento: Série Fonseca (2003)",'http://fightnight-xbmc.googlecode.com/svn/gatofedorento/completas_fonseca.txt',3,tvporpath + art + '',1,False)
    addDir("Gato Fedorento: Série Meireles (2004)",'http://fightnight-xbmc.googlecode.com/svn/gatofedorento/completas_meireles.txt',3,tvporpath + art + '',1,False)
    addDir("Gato Fedorento: Série Barbosa (2005)",'http://fightnight-xbmc.googlecode.com/svn/gatofedorento/completas_barbosa.txt',3,tvporpath + art + '',1,False)    
    addDir("Gato Fedorento: Série Lopes da Silva (2006)",'http://fightnight-xbmc.googlecode.com/svn/gatofedorento/completas_lopesdasilva.txt',3,tvporpath + art + '',1,False)    
    addDir("Gato Fedorento: Diz que é uma Espécie de Magazine (2006)",'http://fightnight-xbmc.googlecode.com/svn/gatofedorento/completas_magazine.txt',3,tvporpath + art + '',1,False)
    addDir("Gato Fedorento: Zé Carlos (2008)",'http://fightnight-xbmc.googlecode.com/svn/gatofedorento/completas_zecarlos.txt',3,tvporpath + art + '',1,False)
    addDir("Gato Fedorento: Esmiúça os Sufrágios (2009)",'http://fightnight-xbmc.googlecode.com/svn/gatofedorento/completas_sufragios.txt',3,tvporpath + art + '',1,False)
    addDir("Gato Fedorento: MEO - Fora da Box (2011)",'http://fightnight-xbmc.googlecode.com/svn/gatofedorento/completas_foradabox.txt',3,tvporpath + art + '',1,False)
    
def request_servidores(url,name):
    titles=[]; ligacao=[]
    link=abrir_url(url)
    recolha=re.compile('----- (.+?) ---- (.+?) ---').findall(link)
    for titulo, endereco in recolha:
        titles.append(titulo)
        ligacao.append(endereco)
    if len(ligacao)==1: index=0
    elif len(ligacao)==0: ok=mensagemok('Gato Fedorento', 'Nenhum stream disponivel.'); return     
    else: index = menuescolha('Escolha a parte', titles)
    if index > -1:
        linkescolha=ligacao[index]
        if linkescolha:
            import urlresolver
            sources=[]
            hosted_media = urlresolver.HostedMediaFile(url=linkescolha)
            sources.append(hosted_media)
            source = urlresolver.choose_source(sources)
            if source:
                linkescolha=source.resolve()
                if linkescolha==False:
                    okcheck = xbmcgui.Dialog().ok
                    okcheck(traducao(40000),traducao(40019))
                    return
                comecarvideo(linkescolha,name)


def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'): params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2: param[splitparams[0]]=splitparams[1]                         
    return param

def comecarvideo(finalurl,name):
    playlist = xbmc.PlayList(1)
    playlist.clear()
    listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage='')
    listitem.setInfo("Video", {"Title":name})
    listitem.setProperty('IsPlayable', 'true')
    dialogWait = xbmcgui.DialogProgress()
    dialogWait.create('Gato Fedorento', 'A carregar')
    playlist.add(finalurl, listitem)
    dialogWait.close()
    del dialogWait
    if selfAddon.getSetting("playertype") == "0": player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
    elif selfAddon.getSetting("playertype") == "1": player = xbmc.Player(xbmc.PLAYER_CORE_MPLAYER)
    elif selfAddon.getSetting("playertype") == "2": player = xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER)
    elif selfAddon.getSetting("playertype") == "3": player = xbmc.Player(xbmc.PLAYER_CORE_PAPLAYER)
    else: player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
    #GA("player",name)
    player.play(playlist)

def addLink(name,url,iconimage):
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)

def addDir(name,url,mode,iconimage,total,pasta):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name, "overlay":6 } )
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)

def clean(text):
    command={'\r':'','\n':'','\t':'','&nbsp;':''}
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
    menu_principal()
elif mode==1: menu_principal()
elif mode==2: seriescompletas()
elif mode==3: request_servidores(url,name)
elif mode==4: ok = mensagemok('Gato Fedorento','Em actualização.')
elif mode==15: ok = mensagemok('Gato Fedorento','A actualizacao é automática. Caso nao actualize va ao','repositorio fightnight e prima c ou durante 2seg','e force a actualizacao. De seguida, reinicie o XBMC.')
elif mode==22: selfAddon.openSettings()
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
