from razdel import sentenize, tokenize
from navec import Navec
from slovnet import Syntax

def actions_character(text, name):

    chunk = []
    slovar = []

    navec = Navec.load('navec_news_v1_1B_250K_300d_100q.tar')
    syntax = Syntax.load('slovnet_syntax_news_v1.tar')
    syntax.navec(navec)

    for sent in sentenize(text):
        slovar.append(sent)
        tokens = [_.text for _ in tokenize(sent.text)]
        chunk.append(tokens)
        chunk[:1]


    words, deps = [], []
    prov = 0
    print("Character actions:")
    for markup in syntax.map(chunk):
        for token in markup.tokens:
            words.append(token.text)
            source = int(token.head_id) - 1
            target = int(token.id) - 1
            if source > 0 and source != target:  # skip root, loops
                deps.append([source, target, token.rel])
    # show_markup(words, deps)
    # print(deps)
        for i in range(len(deps)):
            if words[deps[i][1]] ==name: # если, это имя
                prov = words[deps[i][0]] # сохраняем слово, от которого построилась связь
                print(words[deps[i][1]], words[deps[i][0]], end = ', ') # выводим имя и слово от которого идет связь
            if i+1 < len(words):
                if words[i] +" "+ words[i+1] ==name: # если не нашли имя, то смотрим соседнее слов и добавляем к первому
                    name = words[i] +" "+ words[i+1]
                    prov = words[deps[i][0]]
                    print(name, words[deps[i][0]], end = ', ')        
            if i+2 < len(words):        
                if words[i] +" "+ words[i+1] +" "+ words[i+2] ==name: # если не нашли имя, то смотрим соседнее слов и добавляем к первому и еще добавляем следущее ФИО
                    name = words[i] +" "+ words[i+1] +" "+ words[i+2]
                    prov = words[deps[i][0]]
                    print(name, words[deps[i][0]], end = ', ')
            
            
            if words[deps[i][0]] == prov and deps[i][2] == 'conj' or deps[i][2] == 'xcomp': # если стрелка от связующего слова и связь 'conj' или 'xcomp' 
                print(words[deps[i][1]] + "\n")
        
        words.clear()
        deps.clear()
        
    #print(otvet)


    # otvet содержит найденные имена
    # deps хранит связи между словами и наименование связи
    # words хранит разделенный на токены текст