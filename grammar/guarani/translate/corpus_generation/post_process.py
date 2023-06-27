import re

def post_process(p):
    
    p[0].replace('de el','del')
    p[0].replace('a el','al')
    p[0] = ' '.join(p[0].split())
    p[1].replace(' _', '')
    p[1].replace('_ ', '')
    p[1] =  re.sub(r'\s+', ' ', p[1]) # remove extra spaces
    return([p[0], p[1]])
    