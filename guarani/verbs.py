import csv

def irregular(verb):
    irregulares = ["'a", "'u", "y'u", "'yta", "'yguy"]
    return (verb in irregulares)

def aireal(verb):
    aireales = ["ai-pe'a", "ai-kytĩ","aikutu", "aikarãi", "aikotevẽ", "aikundaha", "aikũmby", "aikytĩ", "aipe'a", "aipeka", "aipete", "aipiro", "aipovã", "aipyaha", "aipokyty", "aiporu", "aipyhy", "aipapa","aipeju", "aipe'o", "aipepi", "aipepy", "aipichy", "aipo'o", "aiporavo", "aipota", "aipyte","aipeha'ã", "aipohano", "aipichãi", "aiporayhureko", "aime", "aimo'ã", "ainupã","aitykua", "aitypei", "aity", "aityvyro", "aisyryku", "aisu'u", "aiguyhai"]
    return (verb in aireales)

def read_csv(filepath):
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        matrix = []
        for row in reader:
            matrix.append(row)
        return matrix

def nasal(verb):
    nasal = False
    nasals = ['ã', 'ẽ', 'ĩ', 'õ', 'ũ', 'ỹ','g̃', 'm', 'n', 'ñ', 'mb', 'nd', 'ng', 'nt']
    if any(nas in verb for nas in nasals):
        nasal = True 
    return nasal

def write_to_csv(filepath, rows):
    with open(filepath, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)

def write_verbs(verbs):
    matched = []
    unmatched = []
    for line in verbs:
        match line[5]:
            case "I":
                possible, line = inflect_time(line)
                if possible:
                    matched.append(line)
                else:
                    unmatched.append(line)
            case _:
                unmatched.append(line)
    return (matched,unmatched)

def inflect_time(line):
    possible = True
    match line[6]:
        case "P":
            line = presente(line)
        case "I":
            line = preterito_imperfecto(line)
        case "F":
            line = futuro(line)
        case "S":
            line = preterito_perfecto(line)
        case "C":
            possible = False
        
    return possible, line

def presente(line):
    if aireal(line[0]):
        match line[7]:
            case "1":
                person = "1"
                match line[8]:
                    case "S":
                        verb = "ai"+line[0]
                        number = "S"
                    case "P":
                        if nasal(line[0]):
                            verb = "ñai"+line[0]
                        else:
                            verb = "jai"+line[0]
                        number = "P"
            case "2":
                person = "2"
                verb = "pei"+line[0]
                number = line[8]
            case "3":
                person = "3"
                verb = "oi"+line[0]
                number = line[8]
    else:
        match line[7]:
            case "1":
                person = "1"
                match line[8]:
                    case "S":
                        verb = "a"+line[0]
                        number = "S"
                    case "P":
                        if nasal(line[0]):
                            verb = 'ña'+line[0]
                        else:
                            verb = "ja"+line[0]
                        number = "P"
            case "2":
                person = "2"
                verb = "pe"+line[0]
                number = line[8]
            case "3":
                person = "3"
                verb = "o"+line[0]
                number = line[8]
    line = [verb, line[0],'V','I','P',person,number]+line[1:]
    return line
       
def preterito_imperfecto(line):
    line = presente(line)
    verb = line[0]+'-mi'
    line = [verb, line[1], 'V','I','I']+line[5:]
    return line
       
def futuro(line):
    line = presente(line)
    verb = line[0]+'t'
    line = [verb, line[1], 'V','I','F']+line[5:]
    return line
       
def preterito_perfecto(line):
    line = presente(line)
    verb = line[0]+'akue'
    line = [verb, line[1], 'V','I','F']+line[5:]
    return line

def main():
    verbs = read_csv("matched-verbs.csv")
    matched, unmatched = write_verbs(verbs)
    write_to_csv("matched-verbs-guarani.csv", matched)
    write_to_csv("unmatched-verbs-guarani.csv", unmatched)

main()