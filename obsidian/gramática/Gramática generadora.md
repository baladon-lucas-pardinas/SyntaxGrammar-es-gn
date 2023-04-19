(Agustín, 02/04) Mi idea es con las palabras que tenemos, generar una serie de reglas de HPSG que generen oraciones en base a las features. La cosa es que para lograr la concordancia de género, número, etc, precisaríamos:
1. Que sea fácil de hacer en guaraní
2. Que haya una herramienta que lo haga automático en español
Lo primero parece ser cierto, porque hay supuestamente tan solo 6 verbos irregulares en todo el idioma, por lo que conjugar y lograr concordancia parecería sencillo dentro de todo, al menos a nivel de verbo.
Lo segundo, parecería ser cierto también. [[Conjugadores de español|Acá]] hablo acerca de las herramientas encontradas.

En ese caso, habría que generar las reglas de producción de alguna forma, a un archivo capaz, porque van a ser un disparate. Pero con eso tendríamos cosas del estilo "Verbo: Satisfizo, Pronombre: Él, Tiempo: Pretérito perfecto, Modo: Indicativo", que nos van a permitir usar HPSG, si es que tenemos features similares para determinantes, sustantivos, etc.