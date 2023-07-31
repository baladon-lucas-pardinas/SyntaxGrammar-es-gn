import re

def post_process(p):
    
    p[0] = p[0].replace(' de el ',' del ')
    p[0] = p[0].replace(' a el ',' al ')
    p[0] = ' '.join(p[0].split())

    p[1] = p[1].replace(' _', '')
    p[1] = p[1].replace('_ ', '')
    p[1] =  re.sub(r'\s+', ' ', p[1]) # remove extra spaces
    p[1] = p[1].strip()

    if (p[1].count('*') == 1):
        p[1] = p[1].replace(' *', '')
    elif (p[1].count('*') == 2):
        split_p = p[1].split()
        last_word = split_p[len(split_p)-1].replace('*','')
        p[1] = p[1].split()[:-1]
        p[1] = ' '.join(p[1])
        p[1] = p[1].replace('*',last_word)

    return([p[0], p[1]])
    