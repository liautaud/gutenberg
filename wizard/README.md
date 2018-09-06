![Gutenberg](http://amaia.at/gutenberg.png)

*Une interface web pour Gutenberg.*


## Présentation.

Le module `gutenberg.wizard` est une interface web pour simplifier l'utilisation de Gutenberg. 

Elle utilise Flask et Bulma, et permet de générer automatiquement les fichiers YAML et HTML à partir d'une entrée de formulaire.

```
FLASK_APP=index.py flask run
```


## Installation.

Vous devez préalablement avoir installé la bibliothèque `gutenberg` sur votre serveur. Pour cela, vous pouvez vous référer aux instructions du fichier `README.md` à la racine du dépôt.

```
python3 -m pip install --user -r requirements.txt
```