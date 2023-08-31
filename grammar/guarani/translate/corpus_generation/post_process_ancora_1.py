import re

def post_process(p):

    if (p[1].count('*') == 1):
        p[1] = p[1].replace(' *', '')
    elif (p[1].count('*') == 2):
        split_p = p[1].split()
        last_word = split_p[len(split_p)-1].replace('*','')
        p[1] = p[1].split()[:-1]
        p[1] = ' '.join(p[1])
        p[1] = p[1].replace('*',last_word)

    return([p[0], p[1]])
    