import praw
import config
import time
import os
import collections, praw
from datetime import datetime

def bot_login():
    print ("Conectando...")
    r = praw.Reddit(username = config.username,
                password = config.password,
                client_id = config.client_id,
                client_secret = config.client_secret,
                user_agent = "reddit:r/EmPortugues:vAlpha (by u/BoEmPortugues)")
    print ("Conectado.")

    return r

def run_bot(r, submissions_replied_to):
    print ("Verificiando as 1000 postagens mais recentes em busca de links...")

    for submission in r.subreddit('emportugues').new(limit=1000):
        if submission.is_self is False and submission.url not in submissions_replied_to:
            submission_url = submission.url
            if submission_url.endswith("/"): sub_url = submission.url[:-1]
            else: sub_url = submission_url
            subreddit_name = sub_url
            if subreddit_name.startswith("https://www.reddit.com/r/"): sub_name = sub_url.replace("https://www.reddit.com/r/", "")
            if subreddit_name.startswith("https://reddit.com/r/"): sub_name = sub_url.replace("https://reddit.com/r/", "")
            sub = r.subreddit(sub_name).display_name
            
            print ("Encontrada postagem com o seguinte link para subreddit: " + sub_url + ".")
            
            submissions_replied_to.append(sub_url)
            
            print ("Coletando dados sobre o subreddit " + r.subreddit(sub).display_name_prefixed + "...")
       
            #nome do subreddit
            subr = r.subreddit(sub).display_name_prefixed
            #descrição completa
            public_description = r.subreddit(sub).public_description
            if public_description == "": desc = "?"
            if public_description != "": desc = "\"" + r.subreddit(sub).public_description.replace("\n", " ") + "\""            
            #data de crialção
            created_utc = int(r.subreddit(sub).created_utc)
            crea = "criado em " + datetime.utcfromtimestamp(created_utc).strftime("%d/%m/%Y às %H:%M:%S")
            #quantidade de subscrições
            subscribers = str(r.subreddit(sub).subscribers)
            if subscribers == 0: subs = "nenhum usuário subscrito"
            if subscribers == 1: subs = "só um usuário subscrito"
            else: subs = subscribers + " usuários subscritos"
            #wiki disponível
            wiki_enabled = r.subreddit(sub).wiki_enabled
            if wiki_enabled == True:  wiki = "[wiki disponível](" + sub_url + "/wiki/index)" 
            else: wiki = "wiki indisponível"
            #tipo de acesso
            subreddit_type = r.subreddit(sub).subreddit_type
            if subreddit_type == "public": type = "conteúdo público" 
            if subreddit_type == "restricted": type = "conteúdo restrito"
            if subreddit_type == "private": type = "conteúdo privado"
            if subreddit_type == "gold_restricted": type = "conteúdo premium"
            if subreddit_type == "archived": type = "conteúdo arquivado"            
            #tipo de postagem
            submission_type = r.subreddit(sub).submission_type
            if submission_type == "any": subm = "permite textos e links"
            if submission_type == "link": subm = "permite apenas links"
            if submission_type == "text": subm = "permite apenas textos"
            #permissão de imagens, allow_videogifs e vídeos
            allow_images = r.subreddit(sub).allow_images
            allow_videogifs = r.subreddit(sub).allow_videogifs
            allow_videos = r.subreddit(sub).allow_videos
            if allow_images == True and allow_videogifs == True and allow_videos == True: mult = "aceita imagens, GIFs e vídeos" 
            if allow_images == True and allow_videogifs == True and allow_videos == False: mult = "aceita somente imagens e GIFs" 
            if allow_images == True and allow_videogifs == False and allow_videos == True: mult = "aceita somente imagens e vídeos" 
            if allow_images == True and allow_videogifs == False and allow_videos == False: mult = "aceita exclusivamente imagens" 
            if allow_images == False and allow_videogifs == True and allow_videos == True: mult = "aceita somente GIFs e vídeos" 
            if allow_images == False and allow_videogifs == True and allow_videos == False: mult = "aceita exclusivamente GIFs" 
            if allow_images == False and allow_videogifs == False and allow_videos == True: mult = "aceita exclusivamente vídeos" 
            if allow_images == False and allow_videogifs == False and allow_videos == False: mult = "não aceita imagens, GIFs nem vídeos" 
            #flair para postagens para usuários
            ufla = r.subreddit(sub).can_assign_user_flair
            lfla = r.subreddit(sub).can_assign_link_flair
            if lfla == True and ufla == True: flair = "disponibiliza flairs para usários e postagens" 
            if lfla == True and ufla == False: flair = "disponibiliza flairs somente para postagens" 
            if lfla == False and ufla == True: flair = "disponibiliza flairs somente para usuários"    
            if lfla == False and ufla == False: flair = "não disponibilzia flairs para postagens nem usuários"           
            #conteúdo adulto
            over18 = r.subreddit(sub).over18
            if over18 == False: nsfw = "seguro para o trabalho" 
            else: nsfw = "não seguro para o trabalho "
            #em quarentena
            quarantine = r.subreddit(sub).quarantine
            if quarantine == False: quar = "em estado normal"
            else: quar = "em estado de quarentena"
            
            print ("Preparando a tabela para comentar na postagem...")
                        
            submission.reply(
            subr + "\n" +
            ":-: | \n" +
            desc + " | \n" +
            crea + " | \n" +
            subs + " | \n" +
            wiki  + " | \n" +
            type  + " | \n" +
            subm  + " | \n" +          
            mult + " | \n" + 
            flair + " | \n" + 
            nsfw + " | \n" +             
            quar + " | \n \n" +
            "^(Eu sou um bô, blipe, blupe. | [Sub](https://www.reddit.com/r/EmPortugues) | [Site](https://emportugues.org/) | [Aplicativo](https://play.google.com/store/apps/details?id=org.emportugues.aplicativo) | [Organização](https://github.com/subreddit-emportugues) | [Mensagem](http://reddit.com/message/compose/?to=BoEmPortugues&subject=Eu não sou um bô.))")
            
            print ("Comentário postado com sucesso!")
            
            with open ("submissions_replied_to.txt", "a") as f:
                f.write(sub_url + "\n")
                print ("Endereço adicionado à listagem.")
    
    print (submissions_replied_to)

    print ("Aguardando 10 minutos para recomeçar...")
    time.sleep(600)

def get_saved_comments():
    if not os.path.isfile("submissions_replied_to.txt"):
        submissions_replied_to = []
    else:
        with open("submissions_replied_to.txt", "r") as f:
            submissions_replied_to = f.read()
            submissions_replied_to = submissions_replied_to.split("\n")
            submissions_replied_to = list(filter(None, submissions_replied_to))

    return submissions_replied_to

r = bot_login()
submissions_replied_to = get_saved_comments()
print (submissions_replied_to)

while True:
    run_bot(r, submissions_replied_to)
    
def is_summon_chain(post):
  if not post.is_root:
    parent_comment_id = post.parent_id
    parent_comment = r.get_info(thing_id=parent_comment_id)
    if parent_comment.author != None and str(parent_comment.author.name) == config.username:
      return True
    else:
      return False
  else:
    return False
  
def comment_limit_reached(post):
  global submissioncount
  count_of_this = int(float(submissioncount[str(post.submission.id)]))
  if count_of_this > 1:
    print ("A tarefa já foi realizada nesta postagem anteriormente.")
    return True
  else:
    return False
  
def is_already_done(post):
  done = False
  numofr = 0
  try:
    repliesarray = post.replies
    numofr = len(list(repliesarray))
  except:
    pass
  if numofr != 0:
    for repl in post.replies:
      if repl.author != None and repl.author.name == config.username:
        done = True
        continue
  if done:
    return True
  else:
    return False

def post_reply(reply,post):
  global submissioncount
  try:
    a = post.reply(reply)
    submissioncount[str(post.submission.id)]+=1
    return True
  except Exception as e:
    warn("A fesposta falhou: %s @ %s"%(e,post.subreddit))
    if str(e) == "Erro 403: Proibido":
      print ("Fui banido em " + "r/" + post.subreddit + ".")
      save_changing_variables()
    return False

submissioncount = collections.Counter()
