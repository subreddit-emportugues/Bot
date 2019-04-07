import praw
import os
from datetime import datetime
import sys  

def __init__():
    print ("Conectando...")
    r = praw.Reddit("bot")
    print ("Conectado.")

    return r

def run_bot(r, submissions_replied_to):
    print ("Verificiando as 1000 postagens mais recentes em busca de links...")

    for submission in r.subreddit('EmPortugues').new(limit=1000):
        if submission.is_self is False and submission.url not in submissions_replied_to:
            submission_url = submission.url
            if submission_url.endswith("/"): sub_url = submission.url[:-1]
            else: sub_url = submission_url
            subreddit_name = sub_url
            if subreddit_name.startswith("https://www.reddit.com/r/"): sub_name = sub_url.replace("https://www.reddit.com/r/", "")
            if subreddit_name.startswith("https://reddit.com/r/"): sub_name = sub_url.replace("https://reddit.com/r/", "")
            sub = r.subreddit(sub_name).display_name
            
            print ("Encontrada postagem com o seguinte link para subreddit: " + submission.url + ".")
            
            submissions_replied_to.append(submission.url)
            
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
            #quantidade de moderadores
            moderators = [moderators for moderators in r.subreddit(sub).moderator()]
            mod_list = len(moderators)
            if mod_list == 0: mods = "nenhum(a) moderador(a)"
            if mod_list == 1: mods = "apenas um(a) moderador(a)"
            if mod_list > 1: mods = str(mod_list) + " moderadores"
            #quantidade de subscrições
            subscribers = str(r.subreddit(sub).subscribers)
            if subscribers == 0: subs = "nenhum membro na comunidade"
            if subscribers == 1: subs = "só um membro na comunidade"
            else: subs = subscribers + " membros na comunidade"
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
            if submission_type == "self": subm = "permite apenas textos"
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
            else: nsfw = "não seguro para o trabalho"
            #em quarentena
            quarantine = r.subreddit(sub).quarantine
            if quarantine == False: quar = "em estado normal"
            else: quar = "em estado de quarentena"
            #versão antiga
            oldr = "[versão antiga](https://old.reddit.com/r/" + r.subreddit(sub).display_name + ")"
            
            print ("Preparando a tabela para comentar na postagem...")
                        
            comment = submission.reply(
            subr + "\n" +
            ":-: | \n" +
            desc + " | \n" +
            crea + " | \n" +
            mods + " | \n" +
            subs + " | \n" +
            wiki  + " | \n" +
            type  + " | \n" +
            subm  + " | \n" +          
            mult + " | \n" + 
            flair + " | \n" + 
            nsfw + " | \n" +             
            quar + " | \n" +
            oldr + " | \n \n" +
            "^(Eu sou um bô, blipe, blupe. | [Sub](https://www.reddit.com/r/EmPortugues) | [Site](https://emportugues.org/) | [Aplicativo](https://play.google.com/store/apps/details?id=org.emportugues.aplicativo) | [Organização](https://github.com/subreddit-emportugues) | [Mensagem](http://reddit.com/message/compose/?to=BoEmPortugues&subject=Eu não sou um bô.))")
            
            comment.mod.distinguish(how='yes', sticky=True)
            
            print ("Comentário postado e fixado!")
            
            with open ("submissions_replied_to.txt", "a") as f:
                f.write(submission.url + "\n")
                print ("Endereço adicionado à listagem.")
    
    print (submissions_replied_to)

    print ("Procedimento terminado com sucesso!")
    sys.exit(0)

def get_saved_comments():
    if not os.path.isfile("submissions_replied_to.txt"):
        submissions_replied_to = []
    else:
        with open("submissions_replied_to.txt", "r") as f:
            submissions_replied_to = f.read()
            submissions_replied_to = submissions_replied_to.split("\n")
            submissions_replied_to = list(filter(None, submissions_replied_to))

    return submissions_replied_to

r = __init__()
submissions_replied_to = get_saved_comments()
print (submissions_replied_to)

while True:
    run_bot(r, submissions_replied_to)
