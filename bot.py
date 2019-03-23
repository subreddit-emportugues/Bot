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
                user_agent = config.user_agent)
    print ("Conectado.")

    return r

def run_bot(r, submissions_replied_to):
    print ("Varrendo as 25 postagens mais recentes...")

    for submission in r.subreddit('test').new(limit=25):
        if submission.is_self is False and submission.url not in submissions_replied_to:
            sub_url = submission.url
            sub = sub_url.replace("https://www.reddit.com/r/", "")
        
            print ("Encontrada postagem com o seguinte link para subreddit: " + submission.url)
            print ("Comentando na postagem sobre o subreddit " + "r/" + sub + "...")
            
            submissions_replied_to.append(submission.url)
            
            #nome do subreddit
            subr = r.subreddit(sub).display_name_prefixed
            #data de crialção
            crea = int(r.subreddit(sub).created_utc)
            #descrição completa
            desc = ""
            if desc != "": "\"" + r.subreddit(sub).public_description + "\""
            elif desc == "": desc = "?"
            #quantidade de subscrições
            subs = r.subreddit(sub).subscribers
            #tipo de postagem
            subm = r.subreddit(sub).submission_type
            if subm == "any": subm = "links e textos"
            if subm == "link": subm = "apenas links"
            if subm == "text": subm = "apenas textos"
            #flair para postagens
            lfla = r.subreddit(sub).can_assign_link_flair
            if lfla == True: lfla = "sim" 
            elif lfla == False: lfla = "não"             
            #flair para usuários
            ufla = r.subreddit(sub).can_assign_user_flair
            if ufla == True: ufla = "sim" 
            elif ufla == False: ufla = "não"            
            #permite imagens
            imag = r.subreddit(sub).allow_images
            if imag == True: imag = "sim" 
            elif imag == False: imag = "não"            
            #permite gifs
            gifs = r.subreddit(sub).allow_videogifs
            if gifs == True: gifs = "sim" 
            elif gifs == False: gifs = "não"
            #permite vídeos
            vids = r.subreddit(sub).allow_videos
            if vids == True: vids = "sim" 
            elif vids == False: vids = "não"
            #conteúdo adulto
            nsfw = r.subreddit(sub).over18
            if nsfw == False: nsfw = "não" 
            elif nsfw == True: nsfw = "sim"
            #em quarentena
            quar = r.subreddit(sub).quarantine
            if quar == False: quar = "não" 
            elif quar == True: quar = "sim"
            #wiki disponível
            wiki = r.subreddit(sub).wiki_enabled
            if wiki == True:  wiki = "<a href=" + submission.url + "/wiki/index>sim</a>" 
            elif wiki != True: wiki = "não"  
            #tipo de acesso
            type = r.subreddit(sub).subreddit_type
            if type == "public": type = "público" 
            if type == "restricted": type = "restrito"
            if type == "private": type = "privado"
            if type == "gold_restricted": type = "premium"
            if type == "archived": type = "arquivado"

            submission.reply(
                "#" + subr + "\n" +
                "---" + "\n \n" +
                "**Descrição completa:** " +  desc + "\n \n" +
                "**Data de criação:** " + (datetime.utcfromtimestamp(crea).strftime("%d/%m/%Y às %H:%M:%S")) + "\n \n" +
                "**Quantidade de subcrições:** " + str(subs) + "\n \n" +
                "**Tipo de postagem:** " + subm  + "\n \n" +
                "**Permite imagens: " + imag + "\n \n" +
                "**Permite vídeos: " + vids + "\n \n" +                
                "**Em quarentena:** " + quar + "\n \n" +
                "---" + "\n \n" +
                "^Eu ^sou ^um ^bô, ^blipe, ^blupe. ^| ^r/EmPortugues ^| ^[Mensagem](http://reddit.com/message/compose/?to=RoboEmPortugues&subject=Robô%%20Report) ^| ^Código")
            
            with open ("submissions_replied_to.txt", "a") as f:
                f.write(submission.url + "\n")

    print ("Varredura completa!")

    print (submissions_replied_to)

    print ("Aguardando 60 segundos para recomeçar...")
    time.sleep(60)

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
    if parent_comment.author != None and str(parent_comment.author.name) == 'config.username':
      return True
    else:
      return False
  else:
    return False
  
def comment_limit_reached(post):
  global submissioncount
  count_of_this = int(float(submissioncount[str(post.submission.id)]))
  if count_of_this > 10:
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
      if repl.author != None and repl.author.name == 'config.username':
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
