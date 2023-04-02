## Crawler para Wiktionary
Podríamos hacerlo con un crawler de esta forma, incluso tomando el género y número para cada forma (a partir del valor de su fila o columna en la tabla), y construyendo los sustantivos con features de ese modo. 
```python
import requests
from bs4 import BeautifulSoup

# Define the URL for the Wiktionary page for "perro"
url = "https://es.wiktionary.org/wiki/perro"

# Send a request to the URL and get the HTML response
response = requests.get(url)
html = response.content

# Use BeautifulSoup to parse the HTML and extract the inflected forms
soup = BeautifulSoup(html, 'html.parser')

inflection_table = soup.find('table', {'class': 'inflection-table'})
rows = inflection_table.find_all('tr')[1:]  # skip the first row

variations = []
for row in rows:
    cells = row.find_all('td')
    for cell in cells:
        variation = cell.text.strip()
        if variation:
            variations.append(variation)

print(variations)
# prints ['perro', 'perros', 'perra', 'perras']
```


## ChatGPT answer - NONE OF THESE ACTUALLY WORK
Yes, there are several Python libraries that can be used to determine the gender and number of a Spanish noun. Here are a few options:

1.  Pattern: This is a Python library for data mining, natural language processing, and machine learning. It includes a module for inflecting Spanish nouns, which can be used to determine their gender and number. You can install it using `pip install pattern`.

```python
`from pattern.es import gender, pluralize

`noun = "perro"
`gender(noun)  # returns "masc"`
`pluralize(noun)  # returns "perros"
```

2.  PyInflect: This is a library for inflection of words in various languages, including Spanish. You can install it using `pip install pyinflect`.


```python
import pyinflect

noun = "perro"
gender = pyinflect.get_gender(noun, lang='es')
number = pyinflect.get_word_form(noun, 'plur', inflect_oov=True)
print(f"{noun} is {gender} and {number}")
# prints "perro is Masculine and perros"
```

3.  Spacy: This is a library for industrial-strength natural language processing in Python. It includes a Spanish language model that can be used to analyze text and extract features like noun gender and number. You can install it using `pip install spacy`, and then download the Spanish language model using `python -m spacy download es_core_news_sm`.

```python
import spacy

nlp = spacy.load('es_core_news_sm')
doc = nlp("el perro negro")
for token in doc:
    if token.pos_ == "NOUN":
        print(f"{token.text} is {token.gender} and {token.number}")
# prints "perro is masc and sing"
```
These libraries can help you determine the gender and number of Spanish nouns, which can be useful in a variety of natural language processing tasks.