# Descrizione dell'ultimo lavoro versionato su GitHub

## Titolo del progetto
Ultimo lavoro: cartella **_es_yaml_** e file : **berlini.xsd, berlini.xml, berlini.yml**

### Sintesi
Il lavoro salvato e versionato su GitHub riguarda la cartella **_es_yaml_**, contenente esempi e risorse per la serializzazione e la validazione XML/YAML. I file principali inclusi nel commit sono: **berlini.yml**, **berlini.xsd**, **berlini.xml**.

#### Dettagli essenziali
- **Scopo:** fornire esempi pratici per la conversione e la validazione tra *YAML* e *XML*, oltre a uno *schema XSD* per la validazione.  
- **Contenuto principale:** **file di dati** (.yml, .xml) e **schema** (.xsd).  

### Note operative
- Verificare sempre la conformità dello **schema (.xsd)** con i file **XML** prima di pubblicare[^1].  
- Usare un validator YAML[^2] Schema per controllare la struttura del file **berlini.yml** prima del commit.

## Checklist (domande)
- [ ] Il repository su GitHub contiene l'ultimo commit con la cartella **es_yaml**?
- [ ] I file **berlini.yml** e **berlini.xml** sono stati validati rispetto a **berlini.xsd**?
- [ ] Serve aggiungere un file **.gitignore** per non mettere certi file generati oppure locali (es. /venv)?


[^1]: è possibile usare il seguente link per verificare la conformità del xsd https://www.freeformatter.com/xml-validator-xsd.html
[^2]: validator YAML come https://codebeautify.org/yaml-editor-online 