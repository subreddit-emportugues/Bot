# Robô

## Descrição
Robô do Reddit que realiza diversas atividades diferentes no subreddit [r/EmPortugues](https://www.reddit.com/r/EmPortugues/) em nome de [u/BoEmPortugues](https://www.reddit.com/user/BoEmPortugues/).

O robô usa [PRAW](https://praw.readthedocs.io/en/latest/#) para se autenticar e obter dados dos subreddits linkados em postagens publicadas no subreddit utilizando [Reddit JSON API](https://github.com/reddit-archive/reddit/wiki/json) para fazer comentários novos e editar comentários antigos formatados em [Markdown](https://www.reddit.com/wiki/markdown), manter rótulos atualizados e indicar repostagens enquanto salva subreddits, postagens e comentários em arquivos TXT.

As tarefas executadas pelo robô possibilitam responder a cada postagem e fixar um comentário novo com dados do subreddit linkado com `reply()` e `distinguish()`, editar comentários antigos atualizando os dados com `edit()`, atualizar flairs e marcações NSFW automaticamente com `select()` e `nsfw()` e remover repostagens com `remove()`.

As informações comentadas pelo robô são: `display_name_prefixed`, `public_description`, `created_utc`, `moderator()`, `subscribers` e `wiki_enabled`, `submission_type`, `allow_images` e/ou `allow_videogifs` e/ou `allow_videos`, `can_assign_user_flair` e/ou `can_assign_link_flair`, `over18`, o link para a versão antiga do subreddit e links para o [subreddit](https://www.reddit.com/r/EmPortugues/), o [site](https://emportugues.org/), o [aplicativo](https://play.google.com/store/apps/details?id=org.emportugues.aplicativo) e este repositório.

## Sumário
* [Instalação](#Instalação)
* [Instruções](#Instruções)
* [Dependências](#Dependências)
* [Colaboração](#Colaboração)
* [Demonstração](#Demonstração)
* [Referências](#Referências)

## Instalação
1. Baixe o repositório;
2. descomprima o arquivo;
3. execute um interpretador de comandos;
4. navegue até a pasta;
5. e rode "py bot.py".

## Instruções
Para alterar o subreddit, em [bot.py](https://github.com/subreddit-emportugues/robo/blob/master/bot.py), edite:
```
for submission in r.subreddit('EmPortugues').new(limit=1000):
```
```
for submission in r.subreddit('EmPortugues').new(limit=1000):
```

Para alterar o comentário novo, em [bot.py](https://github.com/subreddit-emportugues/robo/blob/master/bot.py), edite:
```
comment = submission.reply(
    '#' + subr + '\n\n' +
    '___ \n\n' +
    '**Descrição oficial:** ' + desc + '\n\n' +
    '**Data de criação:** ' + crea + '\n\n' +
    '**Quantidade de moderadores:** ' + mods + '\n\n' +
    '**Quantidade de membros:** ' + subs + '\n\n' +
    '**Disponibiliza wiki:** ' + wiki  + '\n\n' +
    '**Tipo de postagem:** ' + subm  + '\n\n' +          
    '**Mídias permitidas:** ' + mult + '\n\n' + 
    '**Disponibilidade de flairs:** ' + pflair + '\n\n' + 
    '**NSFW:** ' + nsfw + '\n\n' +             
    '**Versão antiga:** ' + oldr + '\n\n' +
    '___ \n\n' +
    '^(Eu sou um bô, blipe, blupe. | [sub](https://www.reddit.com/r/EmPortugues) | [site](https://emportugues.org/) | [aplicativo](https://play.google.com/store/apps/details?id=org.emportugues.aplicativo) | [organização](https://github.com/subreddit-emportugues) | [mensagem](https://reddit.com/message/compose/?to=BoEmPortugues&subject=Eu não sou um bô.))')
```

Para alterar o comentário editado, em [bot.py](https://github.com/subreddit-emportugues/robo/blob/master/bot.py), edite:
```
comment.edit(
    '#' + subr + '\n\n' +
    '___ \n\n' +
    '**Descrição oficial:** ' + desc + '\n\n' +
    '**Data de criação:** ' + crea + '\n\n' +
    '**Quantidade de moderadores:** ' + mods + '\n\n' +
    '**Quantidade de membros:** ' + subs + '\n\n' +
    '**Disponibiliza wiki:** ' + wiki  + '\n\n' +
    '**Tipo de postagem:** ' + subm  + '\n\n' +          
    '**Mídias permitidas:** ' + mult + '\n\n' + 
    '**Disponibilidade de flairs:** ' + pflair + '\n\n' + 
    '**NSFW:** ' + nsfw + '\n\n' +             
    '**Versão antiga:** ' + oldr + '\n\n' +
    '___ \n\n' +
    '^(Eu sou um bô, blipe, blupe. | [Sub](https://www.reddit.com/r/EmPortugues) | [Site](https://emportugues.org/) | [Aplicativo](https://play.google.com/store/apps/details?id=org.emportugues.aplicativo) | [Organização](https://github.com/subreddit-emportugues) | [Mensagem](https://reddit.com/message/compose/?to=BoEmPortugues&subject=Eu não sou um bô.))')
```

Para alterar flairs, em [bot.py](https://github.com/subreddit-emportugues/robo/blob/master/bot.py), edite:
```
if lapse_creation.years == 0 and lapse_creation.months<6: flair = submission.flair.select('32d8425e-2f49-11e9-ab2c-0e1d29001264')
```
```
elif mod_list == 0: flair = submission.flair.select('04969b72-2f47-11e9-b0a9-0e8bb92aff24')
```
```
elif lapse_publication.years == 0 and lapse_publication.months<6: flair = submission.flair.select('4496fb72-2f47-11e9-9f81-0eab5e01b79a')
```
```
else: flair = submission.flair.select('fd76536e-2f46-11e9-8434-0e74c00272c4')
```
```
if lapse_creation.years == 0 and lapse_creation.months<6: flair = submission.flair.select('32d8425e-2f49-11e9-ab2c-0e1d29001264')
```
```
elif mod_list == 0: flair = submission.flair.select('04969b72-2f47-11e9-b0a9-0e8bb92aff24')
```
```
else: flair = submission.flair.select('fd76536e-2f46-11e9-8434-0e74c00272c4')
```
```
submission.flair.select('b9003d0a-3999-11e9-9008-0eabe0609938')
```

## Dependências
> PRAW
```
import praw
```
> OS
```
import os
```
> datetime
```
from datetime import datetime
```
> time
```
import time
```
> relativedelta
```
from dateutil.relativedelta import relativedelta
```
> sys
```
import sys
```

## Colaboração

Você pode colaborar com este repositório!

[Confira os kanbans deste projeto](https://github.com/orgs/subreddit-emportugues/projects/6), [entre em contato com a equipe de moderação](https://reddit.com/message/compose?to=/r/EmPortugues) e [participe da equipe de desenvolvimento](https://github.com/orgs/subreddit-emportugues/teams/desenvolvedores) para saber a respeito do progresso deste repositório caso queira colaborar antes de [reportar um novo problema](https://github.com/subreddit-emportugues/robo/issues) ou [solicitar o recebimento de uma modificação](https://github.com/subreddit-emportugues/robo/pulls).

## Demonstração

[Conheça o robô para entender como o código deste repositório funciona.](https://www.reddit.com/user/BoEmPortugues/) ![](/robo.gif)

## Referências

* Robô: https://www.reddit.com/user/BoEmPortugues
* Comunidade: https://www.reddit.com/r/EmPortugues
* Organização: https://github.com/subreddit-emportugues
* Repositório: https://github.com/subreddit-emportugues/robo
* Projeto: https://github.com/orgs/subreddit-emportugues/projects/6
* Equipe: https://github.com/orgs/subreddit-emportugues/teams/desenvolvedores
* Licença:
