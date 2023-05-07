import requests
from bs4 import BeautifulSoup
import re

def check_transitivity_verb(verb):
    url = f"https://es.wiktionary.org/wiki/{verb}"
    try:
            response = requests.get(url)
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return {"Verb": verb, "Intransitive": False, "Transitive": False, "Bitransitive": False}
    soup = BeautifulSoup(response.content, "html.parser")
        
    transitivity_text = soup.select_one('#bodyContent ol').text
    is_transitive = bool(re.search(r"\btransitivo\b", transitivity_text))
    is_intransitive = bool(re.search(r"\bintransitivo\b", transitivity_text))
    is_bitransitive = bool(re.search(r"\b(?:transitivo and intransitivo|bitransitivo)\b", transitivity_text))
    
    return {"Verb": verb, "Intransitive": is_intransitive, "Transitive": is_transitive, "Bitransitive": is_bitransitive}

verbs = ['hablar', 'comer', 'vivir', 'decir'] # list of infinitive verbs to process
for verb in verbs:
    print(check_transitivity_verb(verb))