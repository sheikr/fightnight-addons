# -*- coding: utf-8 -*-
import xbmc, xbmcaddon, xbmcgui, xbmcplugin, cookielib,urllib, urllib2,re,sys,socket

MainURL = 'http://www.wareztuga.tv/'
addon_id = 'plugin.video.wt'
user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'
art = '/resources/art/'
mensagemok = xbmcgui.Dialog().ok
mensagemprogresso = xbmcgui.DialogProgress()
selfAddon = xbmcaddon.Addon(id=addon_id)
wtpath = selfAddon.getAddonInfo('path').decode('utf-8')
iconpequeno=wtpath + art + 'logo32.png'
pastaperfil = xbmc.translatePath(selfAddon.getAddonInfo('profile')).decode('utf-8')
cookie_wt = os.path.join(pastaperfil, "cookiewt.lwp")
traducaoma= selfAddon.getLocalizedString
vazio=[]
accao =re.compile("'(.+?)'").findall(sys.argv[1])[0]
tipo=re.compile("'(.+?)'").findall(sys.argv[1])[1]
warezid=re.compile("'(.+?)'").findall(sys.argv[1])[2]
try:urlficheiro=re.compile("'(.+?)'").findall(sys.argv[1])[3]
except:urlficheiro=''

#def splitCount(s, count):
#     return [''.join(x) for x in zip(*[list(s[z::count]) for z in range(count)])]

def splitCount(seq, length):
    return [seq[i:i+length] for i in range(0, len(seq), length)]

def abrir_url_cookie(url,parametros=None):
      from t0mm0.common.net import Net
      net=Net()
      net.set_cookies(cookie_wt)
      try:
            if parametros:link=net.http_POST(url,parametros).content.encode('latin-1','ignore')
            link=net.http_GET(url).content.encode('latin-1','ignore')
            return link
      except urllib2.HTTPError, e:
            mensagemok('wareztuga.tv',str(urllib2.HTTPError(e.url, e.code, traducao(40199), e.hdrs, e.fp)),traducao(40200))
            sys.exit(0)
      except urllib2.URLError, e:
            mensagemok('wareztuga.tv',traducao(40199) + ' ' + traducao(40200))
            sys.exit(0)
      except socket.timeout as e:
            mensagemok('wareztuga.tv','Timeout da página.','Tente novamente.')
            sys.exit(0)


def lersinopse():
    mensagemprogresso.create('wareztuga.tv','A carregar...')
    link=clean(abrir_url_cookie(urlficheiro,False))
    #try:
    text=re.compile('<span id="movie-synopsis-aux" class="movie-synopsis-aux">(.+?)</span>').findall(link)[0]
    text=text.decode('string-escape')
    trechos=[]
    i=0
    partido=splitCount(text,99)
    #print partido
    for pedacos in partido:
          #print pedacos
          i=i+1
          nomeficheiro='temp%s.mp3'%(str(i))
          temp=os.path.join(pastaperfil,nomeficheiro)
          trechos.append(temp)
          #limit = min(100, len(text))#100 characters is the current limit.
          #text = text[0:limit]
          url = "http://translate.google.com/translate_tts?tl=pt&q=%s" % (urllib.quote(pedacos))
          #values = urllib.urlencode({"q": pedacos, "textlen": len(pedacos), "tl": 'pt'})
          hrs = {"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7"}
          #req = urllib2.Request(url, data=values, headers=hrs)
          req = urllib2.Request(url,headers=hrs)
          p = urllib2.urlopen(req)
          f = open(temp, 'wb')
          f.write(p.read())
          f.close()
          xbmc.sleep(250)

    #import wave
    outfile=os.path.join(pastaperfil,'final.mp3')
    try:os.remove(outfile)
    except: pass
    import shutil
    destination = open(outfile, 'wb')
    for filename in trechos:
          shutil.copyfileobj(open(filename, 'rb'), destination)
          try:os.remove(filename)
          except: pass
    destination.close()

    playlist = xbmc.PlayList(1)
    playlist.clear()
    listitem = xbmcgui.ListItem(traducao(40347), iconImage="DefaultVideo.png", thumbnailImage='')
    listitem.setInfo("Video", {"Title":traducao(40347)})
    playlist.add(outfile, listitem)
    
    #listitem.setProperty('mimetype', 'video/x-msvideo')
    #listitem.setProperty('IsPlayable', 'true')
    mensagemprogresso.close()
    xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(playlist)  


def abrir_url(url):
      #print "A fazer request de: " + url
      try:
            req = urllib2.Request(url)
            req.add_header('User-Agent', user_agent)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            return link
      except urllib2.HTTPError, e:
            mensagemok('wareztuga.tv',str(urllib2.HTTPError(e.url, e.code, traducao(40199), e.hdrs, e.fp)),traducao(40200))
            sys.exit(0)
      except urllib2.URLError, e:
            mensagemok('wareztuga.tv',traducao(40199) + ' ' + traducao(40200))
            sys.exit(0)
      except socket.timeout as e:
            mensagemok('wareztuga.tv','Timeout da página.','Tente novamente.')
            #sys.exit(0)

def traducao(texto):
      return traducaoma(texto).encode('utf-8')

def apagarinterrompido(tipo):
    try: os.remove(os.path.join(pastaperfil, tipo))
    except: pass
    try: os.remove(os.path.join(pastaperfil, tipo + '_info'))
    except: pass
    xbmc.executebuiltin("XBMC.Notification(wareztuga.tv," + traducao(40201) + ",'10000',"+iconpequeno.encode('utf-8')+")")
    xbmc.executebuiltin("XBMC.Container.Refresh")

def accaonosite(tipo,warezid,metodo):
    url=MainURL + 'fave.ajax.php?mediaType=' + tipo + '&mediaID=' + warezid + '&action=' + metodo
    abrir_url_cookie(url,False)
    xbmc.executebuiltin("XBMC.Notification(wareztuga.tv," + traducao(40116) + ",'10000',"+iconpequeno.encode('utf-8')+")")
    xbmc.executebuiltin("XBMC.Container.Refresh")

def comentarios():
    link=clean(abrir_url_cookie(urlficheiro,False))
    comentarios=re.compile('<div class="comment-user"><div class="username"><span>(.+?)</span>.+?<div class="comment-date"><span>(.+?)</span></div></div><div class="comment-number">.+?</div></div></div><div class="clear"></div><div class="comment-body">(.+?)<div class="comment-separator"></div>').findall(link)
    texto=[]
    if comentarios==vazio: texto.append('\n[B]' + str(traducao(40117)) + '[/B]')
    else: texto.append('\n[B]' + str(traducao(40118)) + ':[/B]')
    xbmc.executebuiltin("ActivateWindow(10147)")
    window = xbmcgui.Window(10147)
    xbmc.sleep(100)
    window.getControl(1).setLabel( "%s - %s" % (traducao(40119),'wareztuga.tv',))
    import htmlentitydefs
    for nick,tempo,comment in comentarios:
        comment=comment.replace('<div class="quote">','[B]').replace('</div><br />','[/I] - ').replace('</span></div>','').replace('<span>[B]<span>','[I]').replace('</span>','').replace('<span>','').replace('<br />','')
        comment = re.sub('&([^;]+);', lambda m: unichr(htmlentitydefs.name2codepoint[m.group(1)]), comment)
        comment= comment.encode('utf-8')
        texto.append('[B][COLOR blue]' + nick + '[/COLOR][/B] (' + tempo + '): ' + comment)
    texto='\n\n'.join(texto)
    window.getControl(5).setText(texto)

def votar(tipo,warezid):
    voto = xbmcgui.Dialog().numeric(0,traducao(40120))
    voto=int(voto)
    if voto > 10 or voto<1:
        votar(tipo,warezid)
    else:
        voto=str(voto)
        urlfinal= MainURL + 'mediaRater.ajax.php?mediaType=' + tipo + '&mediaID=' + warezid + '&rate=' + voto
        abrir_url_cookie(urlfinal,False)
        xbmc.executebuiltin("XBMC.Notification(wareztuga.tv," + traducao(40121) + ",'10000',"+iconpequeno.encode('utf-8')+")")

def trailer(warezid):

    request= 'http://api.themoviedb.org/3/movie/' + warezid + '/trailers?api_key=6ee3768ba155b41252384a1148398b34'
    txheaders= {'User-Agent':user_agent,'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    req = urllib2.Request(request,None,txheaders)
    response=urllib2.urlopen(req).read()
    if re.search('"size":"HD"',response): codigo=re.compile('"size":"HD","source":"(.+?)"').findall(response)[0]
    elif re.search('"size":"HQ"',response): codigo=re.compile('"size":"HQ","source":"(.+?)"').findall(response)[0]
    elif re.search('"size":"Standard"',response): codigo=re.compile('"size":"Standard","source":"(.+?)"').findall(response)[0]
    else:
        mensagemok("wareztuga.tv",traducao(40202))
        return
    sources = []
    youtube='plugin://plugin.video.youtube/?action=play_video&videoid=' + codigo
    xbmc.Player().play(youtube)

def reportarerro(tipo,warezid):
    mensagemok('wareztuga.tv',traducao(40203), traducao(40204), traducao(40205))
    mensagens=[traducao(40341),traducao(40342),traducao(40343),traducao(40344),traducao(40345),traducao(40346)]
    mensagid=['2','7','8','9','10','11']
    index = xbmcgui.Dialog().select('Report', mensagens)
    if index > -1:
          linkreport = MainURL + 'report.ajax.php?reason=opt' + mensagid[index] + '&mediaType=' + tipo + '&mediaID=' + warezid
          mensagem=abrir_url_cookie(linkreport)
          if re.search('Obrigado por reportar o problema',mensagem):
                mensagemok('wareztuga.tv',traducao(40336), traducao(40337),traducao(40338))
          elif re.search('efectuar mais do que um report por conte',mensagem):
                mensagemok('wareztuga.tv',traducao(40339), traducao(40340))

          
    #keyb = xbmc.Keyboard('', traducao(40206))
    #keyb.doModal()
    #if (keyb.isConfirmed()):
    #    search = keyb.getText()
    #    encode=[]
    #    encode.append(search)
    #    if encode != '' and len(encode[0])>=3:
    #        encode.append('Erro reportado através de wareztuga.tv mobile (XBMC).')
    #        comentario='\n\n'.join(encode)
    #        linkreport = MainURL + 'report.ajax.php?mediaType=' + tipo + '&mediaID=' + warezid
    #        parametros = {'problem': comentario}
    #        abrir_url_cookie(linkreport,parametros)
    #        xbmc.executebuiltin("XBMC.Notification(wareztuga.tv,"+traducao(40207)+",'10000',"+iconpequeno.encode('utf-8')+")")
    #    else: xbmc.executebuiltin("XBMC.Notification(wareztuga.tv,"+traducao(40213)+",'10000',"+iconpequeno.encode('utf-8')+")")

def comentar(tipo,warezid):
    keyb = xbmc.Keyboard('', traducao(40122))
    keyb.doModal()
    if (keyb.isConfirmed()):
        search = keyb.getText()
        encode=[]
        encode.append(search)
        if encode != '' and len(encode[0])>=3:
            encode.append('Comentário efectuado através de wareztuga.tv mobile.')
            comentario='\n\n'.join(encode)
            linkcomment = MainURL + 'comment.ajax.php?mediaType=' + tipo + '&mediaID=' + warezid
            parametros = {'comment': comentario}
            estado=abrir_url_cookie(linkcomment,parametros=parametros)
            xbmc.executebuiltin("XBMC.Notification(wareztuga.tv,"+traducao(40208)+",'10000',"+iconpequeno.encode('utf-8')+")")
        else: xbmc.executebuiltin("XBMC.Notification(wareztuga.tv,"+traducao(40213)+",'10000',"+iconpequeno.encode('utf-8')+")")

def clean(text):
      command={'\r':'','\n':'','\t':'','\xC0':'À','\xC1':'Á','\xC2':'Â','\xC3':'Ã','\xC7':'Ç','\xC8':'È','\xC9':'É','\xCA':'Ê','\xCC':'Ì','\xCD':'Í','\xCE':'Î','\xD2':'Ò','\xD3':'Ó','\xD4':'Ô','\xDA':'Ú','\xDB':'Û','\xE0':'à','\xE1':'á','\xE2':'â','\xE3':'ã','\xE7':'ç','\xE8':'è','\xE9':'é','\xEA':'ê','\xEC':'ì','\xED':'í','\xEE':'î','\xF3':'ó','\xF5':'õ','\xFA':'ú'}
      regex = re.compile("|".join(map(re.escape, command.keys())))
      return regex.sub(lambda mo: command[mo.group(0)], text)


def principal():
    if accao== 'visto': accaonosite(tipo,warezid,'watched')
    if accao== 'faved': accaonosite(tipo,warezid,'faved')
    if accao== 'cliped': accaonosite(tipo,warezid,'cliped')
    if accao== 'subscribed': accaonosite(tipo,warezid,'subscribed')
    if accao== 'comentarios': comentarios()
    if accao== 'lersinopse': lersinopse()
    if accao== 'comentar': comentar(tipo,warezid)
    if accao== 'votar': votar(tipo,warezid)
    if accao== 'trailer': trailer(warezid)
    if accao== 'interrompido':apagarinterrompido(tipo)
    if accao== 'reportar': reportarerro(tipo,warezid)

principal()
