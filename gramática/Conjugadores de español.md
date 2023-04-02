[Spanish conjugator](https://pypi.org/project/spanishconjugator/) : Parecería errarle en los modos menos usados, ej. subjuntivo, o en tiempos poco comunes. Para lo más usual parecería andar bien. Igual verbos irregulares lo confunden.
[MLConjug3](https://mlconjug3.readthedocs.io/en/latest/usage.html): Tiene algunas categorías que son inventadas, hay que tener cuidado. Ej. Tiene las siguientes dos: "Indicativo Pretérito imperfecto" e "Indicativo pretérito imperfecto" (nótese la P mayúscula). De esas, la primera es fruta absoluta (dice cosas como "vosotros hablió" en vez de "vosotros hablabais") pero la segunda funciona (conjuga bien verbos como "satisfacer" incluso). En general parecería andar bastante bien.

Otra opción sería descargar las tablas de conjugación para todos los verbos del español y usarlas de alguna forma.

### Examples:
```python
from spanishconjugator import Conjugator
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

imperfect_conjugation = Conjugator().conjugate('satisfacer','preterite','indicative','ella')
print(imperfect_conjugation.encode('iso-8859-1').decode('utf-8'))

print(Conjugator().conjugate('haber','future','subjunctive','yo').encode('iso-8859-1').decode('utf-8'))

print(Conjugator().conjugate('haber','present_perfect','indicative','ellas').encode('iso-8859-1').decode('utf-8'))
```

```python
from mlconjug3 import Conjugator

# initialize the conjugator
conjugator = Conjugator(language='es')

# conjugate the verb "satisfacer"
verb = conjugator.conjugate("satisfacer")

# print all the conjugated forms as a list of tuples.
print(verb.iterate())
```