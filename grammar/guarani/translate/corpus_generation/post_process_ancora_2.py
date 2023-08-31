import re

def post_process(p):
    
    p[0] = p[0].replace(' de el ',' del ')
    p[0] = p[0].replace(' a el ',' al ')
    p[0] = ' '.join(p[0].split())

    p[1] = p[1].replace(' _', '')
    p[1] = p[1].replace('_ ', '')
    p[1] =  re.sub(r'_# .', '', p[1])
    p[1] =  re.sub(r'\s+', ' ', p[1]) # remove extra spaces
    p[1] = p[1].strip()

    # Capitalize first character and add period
    p[0] = p[0][0].upper() # + p[0][1:] + '.'
    p[1] = p[1][0].upper() # + p[1][1:] + '.'

    return([p[0], p[1]])
    