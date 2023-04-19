
#### Qué [[NMT]] elegir? (25/3/23)

- Poca evidencia

- Modelos de pago no parecen mejores a los opensource ([[Google]], [[Azure]])
https://www.youtube.com/watch?v=j2PmW3l55ls&ab_channel=EuroPythonConference

- Más o menos todos tienen los mismos resultados:
https://www.youtube.com/watch?v=j2PmW3l55ls&ab_channel=EuroPythonConference
https://forum.opennmt.net/t/should-i-use-opennmt-py-or-opennmt-tf/5142
https://github.com/OpenNMT/OpenNMT-py/issues/881

- [[Beam Search]] === [[Greedy]]?
https://www.youtube.com/watch?v=j2PmW3l55ls&ab_channel=EuroPythonConference

- Workshop comparación:
[[OpenNMT]] mejor accuracy
[[MarianNMT]] mejor uso de recursos
https://aclanthology.org/W18-2701.pdf

Otros con documentación y comunidad pobre:
- Moses (Perl, documentación rara, LastUpd=2017)
- SYSTRAN (Página bastante extraña)

#### Resumen:
- Recursos (MarianNMT)
- Resultados (OpenNMT, aunque seguramente no mucho)
- Documentación/Comunidad: (OpenMT y MarianMT)


Python (27/3):
- Entrena modelo c++ con archivo generado dinamicamente
- Dado el modelo generado, hacer el testing, ya que marianNMT es muy pobre