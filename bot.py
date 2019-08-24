import praw
import os
from datetime import datetime
import time
from dateutil.relativedelta import relativedelta
import sys

def __init__():
    r = praw.Reddit("bot")
    print ("Conectado.")

    return r
    
def run_bot(r, subreddits_list, replies_list, posts_list):
    print ("1/3: comentando as postagens recentes e salvando subs, postagens e comentários...")
    for submission in r.subreddit('EmPortugues').new(limit=1000):
        if submission.is_self is False:
            #subreddit
            submission_url = submission.url
            if submission_url.endswith("/"): sub_url = submission.url[:-1]
            else: sub_url = submission_url
            subreddit_name = sub_url
            if subreddit_name.startswith("https://www.reddit.com/r/"): sub_name = sub_url.replace("https://www.reddit.com/r/", "")
            if subreddit_name.startswith("https://reddit.com/r/"): sub_name = sub_url.replace("https://reddit.com/r/", "")
            sub = r.subreddit(sub_name).display_name
            if sub not in subreddits_list:
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
                if mod_list == 0: mods = "nenhum moderador"
                if mod_list == 1: mods = "apenas um moderador"
                if mod_list > 1: mods = str(mod_list) + " moderadores"
                #quantidade de membros
                subscribers = r.subreddit(sub).subscribers
                members = str(format(r.subreddit(sub).subscribers, ",d").replace(",","."))
                if subscribers == 0: subs = "nenhum membro na comunidade"
                if subscribers == 1: subs = "só um membro na comunidade"
                else: subs = members + " membros na comunidade"
                #wiki disponível
                wiki_enabled = r.subreddit(sub).wiki_enabled
                if wiki_enabled == True:  wiki = "[sim](" + sub_url + "/wiki/index)" 
                else: wiki = "não"           
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
                if lfla == True and ufla == True: pflair = "para usários e postagens" 
                if lfla == True and ufla == False: pflair = "somente para postagens" 
                if lfla == False and ufla == True: pflair = "somente para usuários"    
                if lfla == False and ufla == False: pflair = "indisponível"           
                #conteúdo adulto
                over18 = r.subreddit(sub).over18
                if over18 == False: nsfw = "não" 
                else: nsfw = "sim"
                #versão antiga
                oldr = "[link](https://old.reddit.com/r/" + r.subreddit(sub).display_name + ")"
                #novo comentário
                comment = submission.reply(
                    "#" + subr + "\n\n" +
                    "___ \n\n" +
                    "**Descrição oficial:** " + desc + "\n\n" +
                    "**Data de criação:** " + crea + "\n\n" +
                    "**Quantidade de moderadores:** " + mods + "\n\n" +
                    "**Quantidade de membros:** " + subs + "\n\n" +
                    "**Disponibiliza wiki:** " + wiki  + "\n\n" +
                    "**Tipo de postagem:** " + subm  + "\n\n" +          
                    "**Mídias permitidas:** " + mult + "\n\n" + 
                    "**Disponibilidade de flairs:** " + pflair + "\n\n" + 
                    "**NSFW:** " + nsfw + "\n\n" +             
                    "**Versão antiga:** " + oldr + "\n\n" +
                    "___ \n\n" +
                    "^(Eu sou um bô, blipe, blupe. | [sub](https://www.reddit.com/r/EmPortugues) | [site](https://emportugues.org/) | [aplicativo](https://play.google.com/store/apps/details?id=org.emportugues.aplicativo) | [organização](https://github.com/subreddit-emportugues) | [mensagem](https://reddit.com/message/compose/?to=BoEmPortugues&subject=Eu não sou um bô.))")
                #comentário fixado
                comment.mod.distinguish(how='yes', sticky=True)
                #registros salvos
                with open ("subreddits_list.txt", "a") as f:
                    f.write(sub + "\n")
                with open ("posts_list.txt", "a") as f:
                    f.write(submission.id + "\n")
                with open ("replies_list.txt", "a") as f:
                    f.write(comment.id + "\n")
    print ("2/3: editando cada um dos comentários antigos salvos com informações recentes...")
    for reply in replies_list:
        comment = r.comment(reply)
        #subreddit
        submission_url = comment.submission.url
        if submission_url.endswith("/"): sub_url = comment.submission.url[:-1]
        else: sub_url = submission_url
        subreddit_name = sub_url
        if subreddit_name.startswith("https://www.reddit.com/r/"): sub_name = sub_url.replace("https://www.reddit.com/r/", "")
        if subreddit_name.startswith("https://reddit.com/r/"): sub_name = sub_url.replace("https://reddit.com/r/", "")
        sub = r.subreddit(sub_name).display_name                           
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
        if mod_list == 0: mods = "nenhum moderador"
        if mod_list == 1: mods = "apenas um moderador"
        if mod_list > 1: mods = str(mod_list) + " moderadores"
        #quantidade de membros
        subscribers = r.subreddit(sub).subscribers
        members = str(format(r.subreddit(sub).subscribers, ",d").replace(",","."))
        if subscribers == 0: subs = "nenhum membro na comunidade"
        if subscribers == 1: subs = "só um membro na comunidade"
        else: subs = members + " membros na comunidade"
        #wiki disponível
        wiki_enabled = r.subreddit(sub).wiki_enabled
        if wiki_enabled == True:  wiki = "[sim](" + sub_url + "/wiki/index)" 
        else: wiki = "não"           
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
        if lfla == True and ufla == True: pflair = "para usários e postagens" 
        if lfla == True and ufla == False: pflair = "somente para postagens" 
        if lfla == False and ufla == True: pflair = "somente para usuários"    
        if lfla == False and ufla == False: pflair = "indisponível"           
        #conteúdo adulto
        over18 = r.subreddit(sub).over18
        if over18 == False: nsfw = "não" 
        else: nsfw = "sim"
        #versão antiga
        oldr = "[link](https://old.reddit.com/r/" + r.subreddit(sub).display_name + ")"  
        #comentário editado
        comment.edit(
            "#" + subr + "\n\n" +
            "___ \n\n" +
            "**Descrição oficial:** " + desc + "\n\n" +
            "**Data de criação:** " + crea + "\n\n" +
            "**Quantidade de moderadores:** " + mods + "\n\n" +
            "**Quantidade de membros:** " + subs + "\n\n" +
            "**Disponibiliza wiki:** " + wiki  + "\n\n" +
            "**Tipo de postagem:** " + subm  + "\n\n" +          
            "**Mídias permitidas:** " + mult + "\n\n" + 
            "**Disponibilidade de flairs:** " + pflair + "\n\n" + 
            "**NSFW:** " + nsfw + "\n\n" +             
            "**Versão antiga:** " + oldr + "\n\n" +
            "___ \n\n" +
            "^(Eu sou um bô, blipe, blupe. | [Sub](https://www.reddit.com/r/EmPortugues) | [Site](https://emportugues.org/) | [Aplicativo](https://play.google.com/store/apps/details?id=org.emportugues.aplicativo) | [Organização](https://github.com/subreddit-emportugues) | [Mensagem](https://reddit.com/message/compose/?to=BoEmPortugues&subject=Eu não sou um bô.))")
    print ("3/3: atualizando flairs de todas as postagens publicadas salvas com dados novos...")
    for post in posts_list:
        submission = r.submission(post)
        #subreddit
        submission_url = submission.url
        if submission_url.endswith("/"): sub_url = submission.url[:-1]
        else: sub_url = submission_url
        subreddit_name = sub_url
        if subreddit_name.startswith("https://www.reddit.com/r/"): sub_name = sub_url.replace("https://www.reddit.com/r/", "")
        if subreddit_name.startswith("https://reddit.com/r/"): sub_name = sub_url.replace("https://reddit.com/r/", "")
        sub = r.subreddit(sub_name).display_name
        #data de crialção
        created_utc = int(r.subreddit(sub).created_utc)
        crea = "criado em " + datetime.utcfromtimestamp(created_utc).strftime("%d/%m/%Y às %H:%M:%S")
        #quantidade de moderadores
        moderators = [moderators for moderators in r.subreddit(sub).moderator()]
        mod_list = len(moderators)
        #idade do subreddit
        today = datetime.utcfromtimestamp(int(time.time())).strftime("%Y-%m-%d %H:%M:%S")
        tdate = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
        creation = datetime.utcfromtimestamp(created_utc).strftime("%Y-%m-%d %H:%M:%S")
        cdate = datetime.strptime(creation, '%Y-%m-%d %H:%M:%S')
        lapse_creation = relativedelta(tdate, cdate)
        #flair
        flair = ""
        #data da última postagem
        for post in r.subreddit(sub).new(limit=1):
            date_now = datetime.utcfromtimestamp(int(time.time())).strftime("%Y-%m-%d %H:%M:%S")
            ndate = datetime.strptime(date_now, '%Y-%m-%d %H:%M:%S')
            publication_date = datetime.utcfromtimestamp(int(post.created)).strftime("%Y-%m-%d %H:%M:%S")
            pdate = datetime.strptime(publication_date, '%Y-%m-%d %H:%M:%S')
            lapse_publication = relativedelta(ndate, pdate)
            #novo
            if lapse_creation.years == 0 and lapse_creation.months<6: flair = submission.flair.select('32d8425e-2f49-11e9-ab2c-0e1d29001264')
            #sem moderação
            elif mod_list == 0: flair = submission.flair.select('04969b72-2f47-11e9-b0a9-0e8bb92aff24')
            #ativo
            elif lapse_publication.years == 0 and lapse_publication.months<6: flair = submission.flair.select('4496fb72-2f47-11e9-9f81-0eab5e01b79a')
            #inativo
            else: flair = submission.flair.select('fd76536e-2f46-11e9-8434-0e74c00272c4')
        #sub vazio
        if flair is "":
            #novo
            if lapse_creation.years == 0 and lapse_creation.months<6: flair = submission.flair.select('32d8425e-2f49-11e9-ab2c-0e1d29001264')
            #sem moderação
            elif mod_list == 0: flair = submission.flair.select('04969b72-2f47-11e9-b0a9-0e8bb92aff24')
            #inativo
            else: flair = submission.flair.select('fd76536e-2f46-11e9-8434-0e74c00272c4')
    print ("Procedimento terminado com sucesso!")
    sys.exit(0)

def get_subreddits_list():
    if not os.path.isfile("subreddits_list.txt"):
        subreddits_list = []
    else:
        with open("subreddits_list.txt", "r") as f:
            subreddits_list = f.read()
            subreddits_list = subreddits_list.split("\n")
            subreddits_list = list(filter(None, subreddits_list))

    return subreddits_list
    
def get_replies_list():
    if not os.path.isfile("replies_list.txt"):
        replies_list = []
    else:
        with open("replies_list.txt", "r") as f:
            replies_list = f.read()
            replies_list = replies_list.split("\n")
            replies_list = list(filter(None, replies_list))

    return replies_list
    
def get_posts_list():
    if not os.path.isfile("posts_list.txt"):
        posts_list = []
    else:
        with open("posts_list.txt", "r") as f:
            posts_list = f.read()
            posts_list = posts_list.split("\n")
            posts_list = list(filter(None, posts_list))

    return posts_list

r = __init__()
subreddits_list = get_subreddits_list()
replies_list = get_replies_list()
posts_list = get_posts_list()

while True:
    run_bot(r, subreddits_list, replies_list, posts_list)
