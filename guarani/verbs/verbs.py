import csv

# No hay irregulares en matched_nouns
def irregular(verb):
    irregulares = ["‘a","‘u","yguy","yta","‘e","ha"]
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
    with open(filepath, 'w',newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)

def write_verbs(verbs):
    matched = []
    unmatched = []
    for line in verbs:
        match line[7]:
            case "I":
                possible, line = inflect_time(line)
                if possible:
                    matched.append(line)
                else:
                    unmatched.append(line)
            case "N":
                line = [line[0],line[0],'V','M','N','0','0','0','0'] + line[1:]
                matched.append(line)
            case _:
                unmatched.append(line)
    return (matched,unmatched)

def inflect_time(line):
    possible = True
    match line[8]:
        case "P":
            if irregular(line[0]):
                line = inflect_irregular(line)
            else:
                line = presente(line)
        case "I":
            line = preterito_imperfecto(line)
        case "F":
            line = futuro(line)
        case "S":
            line = preterito_simple(line)
        case "C":
            possible = False
        
    return possible, line

def presente(line):
    if aireal(line[0]):
        match line[9]:
            case "1":
                person = "1"
                match line[10]:
                    case "S":
                        verb = "ai" + line[0]
                        number = "S"
                    case "P":
                        if nasal(line[0]):
                            if line[1] == 'I':
                                verb = "ñai" + line[0]
                            else:
                                verb = 'roi' + line[0]
                        else:
                            if line[1] == 'I':
                                verb = "jai" + line[0]
                            else:
                                verb = 'roi' + line[0]
                        number = "P"
            case "2":
                person = "2"
                verb = "pei" + line[0]
                number = line[8]
            case "3":
                person = "3"
                if line[2] == 'B':
                    verb = "oi" + line[0]
                else:
                    verb = "roi" + line[0]
                number = line[8]
    else:
        match line[9]:
            case "1":
                person = "1"
                match line[10]:
                    case "S":
                        verb = "a" + line[0]
                        number = "S"
                    case "P":
                        if nasal(line[0]):
                            if line[1] == 'I':
                                verb = 'ña' + line[0]
                            else:
                                verb = 'ro' + line[0]
                        else:
                            if line[1] == 'I':
                                verb = "ja" + line[0]
                            else:
                                verb = 'ro' + line[0]
                        number = "P"
            case "2":
                person = "2"
                verb = "pe" + line[0]
                number = line[10]
            case "3":
                person = "3"
                verb = "o"+line[0]
                number = line[10]
    line = [verb, line[0],'V','I','P',person,number]+line[1:]
    return line
       
def preterito_imperfecto(line):
    if irregular(line[0]):
        line = inflect_irregular(line)
    else:
        line = presente(line)
    verb = line[0]+'-mi'
    line = [verb, line[1], 'V','I','I']+line[5:]
    return line
       
def futuro(line):
    if irregular(line[0]):
        line = inflect_irregular(line)
    else:
        line = presente(line)
    verb = line[0]+'t'
    line = [verb, line[1], 'V','I','F']+line[5:]
    return line
       
def preterito_simple(line):
    if irregular(line[0]):
        line = inflect_irregular(line)
    else:
        line = presente(line)
    verb = line[0]+'kuri'
    line = [verb, line[1], 'V','I','F']+line[5:]
    return line

def inflect_irregular(verb):
    v = ''
    match verb[0]:
        case "‘a":
            match verb[9]:
                case '1':
                    match verb[10]:
                        case 'S':
                            v = "ha'a"
                        case 'P':
                            if verb[1] == 'I':
                                v = "ja'a"
                            else:
                                v = "ro'a"
                case '2':
                    match verb[10]:
                        case 'S':
                            v = "re'a"
                        case 'P':
                            v = "pe'a"
                case '3':
                    match verb[10]:
                        case 'S':
                            v = "ho'a"
                        case 'P':
                            v = "ho'a"
        case "‘u":
            match verb[1]:
                case "comer":
                    match verb[9]:
                        case '1':
                            match verb[10]:
                                case 'S':
                                    v = "ha'u"
                                case 'P':
                                    if verb[1] == 'I':
                                        v = "ja'u"
                                    else:
                                        v = "ro'u"
                        case '2':
                            match verb[10]:
                                case 'S':
                                    v = "re'u"
                                case 'P':
                                    v = "pe'u"
                        case '3':
                            match verb[10]:
                                case 'S':
                                    v = "ho'u"
                                case 'P':
                                    v = "ho'u"
                case "beber":
                    match verb[9]:
                        case '1':
                            match verb[10]:
                                case 'S':
                                    v = "hai'u"
                                case 'P':
                                    if verb[1] == 'I':
                                        v = "jai'u"
                                    else:
                                        v = "roi'u"
                        case '2':
                            match verb[10]:
                                case 'S':
                                    v = "rei'u"
                                case 'P':
                                    v = "pei'u"
                        case '3':
                            match verb[10]:
                                case 'S':
                                    v = "hoi'u"
                                case 'P':
                                    v = "hoi'u"
        case "yguy":
            match verb[9]:
                case '1':
                    match verb[10]:
                        case 'S':
                            v = "ha'yguy"
                        case 'P':
                            if verb[1] == 'I':
                                v = "ja'yguy"
                            else:
                                v = "ro'yguy"
                case '2':
                    match verb[10]:
                        case 'S':
                            v = "re'yguy"
                        case 'P':
                            v = "pe'yguy"
                case '3':
                    match verb[10]:
                        case 'S':
                            v = "ho'yguy"
                        case 'P':
                            v = "ho'yguy"
        case "yta":
            match verb[9]:
                case '1':
                    match verb[10]:
                        case 'S':
                            v = "ha'yta"
                        case 'P':
                            if verb[1] == 'I':
                                v = "ja'yta"
                            else:
                                v = "ro'yta"
                case '2':
                    match verb[10]:
                        case 'S':
                            v = "re'yta"
                        case 'P':
                            v = "pe'yta"
                case '3':
                    match verb[10]:
                        case 'S':
                            v = "ho'yta"
                        case 'P':
                            v = "ho'yta"
        case "‘e":
            match verb[9]:
                case '1':
                    match verb[10]:
                        case 'S':
                            v = "ha'e"
                        case 'P':
                            if verb[1] == 'I':
                                v = "ja'e"
                            else:
                                v = "ro'e"
                case '2':
                    match verb[10]:
                        case 'S':
                            v = "ere"
                        case 'P':
                            v = "peje"
                case '3':
                    match verb[10]:
                        case 'S':
                            v = "he'i"
                        case 'P':
                            v = "he'i"
            match verb[9]:
                case '1':
                    match verb[10]:
                        case 'S':
                            v = "ha'yta"
                        case 'P':
                            if verb[1] == 'I':
                                v = "ja'yta"
                            else:
                                v = "ro'yta"
                case '2':
                    match verb[10]:
                        case 'S':
                            v = "re'yta"
                        case 'P':
                            v = "pe'yta"
                case '3':
                    match verb[10]:
                        case 'S':
                            v = "ho'yta"
                        case 'P':
                            v = "ho'yta"
        case "ha":
            match verb[9]:
                case '1':
                    match verb[10]:
                        case 'S':
                            v = "aha"
                        case 'P':
                            if verb[1] == 'I':
                                v = "jaha"
                            else:
                                v = "roho"
                case '2':
                    match verb[10]:
                        case 'S':
                            v = "reho"
                        case 'P':
                            v = "peju"
                case '3':
                    match verb[10]:
                        case 'S':
                            v = "oho"
                        case 'P':
                            v = "oho"
    line = [v,verb[0],'V','I','P',verb[9],verb[10]] + verb[1:]
    return line

def duplicate_plurals(verbs):
    finished = []
    for line in verbs:
        match line[8]:
            case 'S':
                line = [line[0],'0','B'] + line[1:]
                finished.append(line)
            case'P':
                match line[7]:
                    case '1':
                        line2 = line
                        line = [line[0],'I','B'] + line[1:]
                        finished.append(line)
                        line2 = [line2[0],'E','B'] + line2[1:]
                        finished.append(line2)
                    case '2': 
                        line = [line[0],'0','B'] + line[1:]
                        finished.append(line)
                    case '3': 
                        line2 = line
                        line = [line[0],'0','B'] + line[1:]
                        finished.append(line)
                        line2 =  [line2[0],'0','P'] + line2[1:]
                        finished.append(line2)
    return finished

def main():
    verbs = read_csv("matched-verbs.csv")
    verbs = duplicate_plurals(verbs)
    matched, unmatched = write_verbs(verbs)
    write_to_csv("matched-verbs-guarani.csv", matched)
    write_to_csv("unmatched-verbs-guarani.csv", unmatched)

main()