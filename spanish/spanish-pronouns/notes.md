# Notas

En el archivo pronouns.csv están los que hay que pasar a guaraní (en sorted.csv están todos los de freeling).
Hay que ver si tiene sentido pasar algo de eso igual, hay que ver cómo funcionan esas cosas en guaraní en realidad.

## Desafíos
Hay que ver cómo conjugar los usted y ustedes, que tienen agreement de 3ra persona. Se me ocurre que nuestro script al levantarlo se fije en si es formal o no, y si es formal lo pasa a 3ra persona el AGREEMENT. Total en última instancia su sintaxis se comporta así, es semántica el que sea segunda persona.

Al "vos" lo dejé sin distinguir del "tú", porque de todas formas no tenemos conjugaciones para "vos sos" o "vos hacés" en freeling, ni aparece en el jojajovai "sos" o "hacés". Sin embargo puse el "vosotros" y "vosotras" porque había alguna (casi ninguna) aparición en el jojajovai, pueden eliminarse sino.

El "se" tiene las mismas tags que el "le", hay que ver cómo distinguirlo si es que precisa. En oraciones como "él lo vio" y "él se vio" no hay diferencia sintáctica, tampoco en "él le compró un libro" y "él se compró un libro", pero sí hay que tener cuidado en "él le dio un beso a María" vs "él se dio una carta a sí mismo".

## Casos

@Vito: En cuanto a los casos te dejo esta definición:

        Caso (case): «marca de función que establece las relación gramatical entre dos elementos. Dicha marca puede manifestarse morfológicamente (a través de variaciones en la flexión de los nombres, adjetivos, pronombres, etc.) o puede ser abstracta, en el sentido de no ser visible morfológicamente. En español, solo los pronombres personales manifiestan variaciones formales de caso:

        Nominativo: yo, tú, él, ella, ello, nosotros/as, vosotros/as, ellos/as
        Acusativo: me, te, lo, la, nos, os, los, las
        Dativo: me, te, le, nos, os, les
Y esta otra aclaración:

        En español, los casos oblicuos son los que están marcados por una preposición. Así, en gramática se dice que los pronombres «mí», «ti» o «sí», que solo pueden aparecer como términos de preposición (sin ti, de mí, para sí, etc.), están en caso oblicuo.

