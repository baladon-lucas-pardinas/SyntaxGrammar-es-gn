import csv

# No hay irregulares en matched_nouns
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
            case _:
                unmatched.append(line)
    return (matched,unmatched)

def inflect_time(line):
    possible = True
    match line[8]:
        case "P":
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
    line = presente(line)
    verb = line[0]+'-mi'
    line = [verb, line[1], 'V','I','I']+line[5:]
    return line
       
def futuro(line):
    line = presente(line)
    verb = line[0]+'t'
    line = [verb, line[1], 'V','I','F']+line[5:]
    return line
       
def preterito_simple(line):
    line = presente(line)
    verb = line[0]+'kuri'
    line = [verb, line[1], 'V','I','F']+line[5:]
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
    verbs2 = duplicate_plurals(verbs)
    matched, unmatched = write_verbs(verbs2)
    write_to_csv("matched-verbs-guarani2.csv", verbs2)
    write_to_csv("matched-verbs-guarani.csv", matched)
    write_to_csv("unmatched-verbs-guarani.csv", unmatched)

main()