![Gutenberg](http://amaia.at/gutenberg.png)

*Un générateur automatique de diffusions pour les associations de l'ENS de Lyon.*


## Présentation.

*Gutenberg* est un utilitaire en ligne de commande qui permet de générer automatiquement des diffusions e-mail pour plusieurs associations de l'ENS de Lyon. Il attend en entrée un fichier YAML dont le schéma est décrit ci-dessous, et écrit le code HTML correspondant à l'e-mail généré dans un fichier donné.

```
gutenberg 2017-09-15.yml 2017-09-15.html
```


## Installation.

```
python3 -m pip install --user -e .
```


## Format d'entrée.

Les fichiers traités par *Gutenberg* doivent être au format YAML.

Ils doivent contenir les champs suivants :
- `author` : L'auteur de la diffusion, au format `Prénom Nom <email>`.
- `title` : Le titre de la diffusion *(qui apparaîtra notamment dans l'en-tête)*.
- `date` : La date de la diffusion, au format `1977-04-22`.
- `template` : Le thème à utiliser pour la diffusion.
  Pour l'instant, sont disponibles `enscene.diffusion` et `enscene.programmation`.

Le reste des champs dépend de la valeur de `template`. On retrouve en général :
- `greeting` : La formule d'appel à utiliser en début de diffusion.
- `introduction` : Le texte d'introduction de la diffusion, au format Markdown.
- `sections` : La liste des sections de la diffusion.
- `closing` : La formule de fermeture à utiliser en fin de diffusion.

Chaque section contient en général les champs suivants :
- `title` : Le titre de la section.
- `color` : La couleur du titre de la section.
- `image` : L'image qui accompagne la section, le cas échéant.
- `align` : La position de l'image par rapport au texte, parmi `left` et `right`.
- `date` : La date de l'événement, le cas échéant.
- `place` : Le lieu de l'événement, le cas échéant.
- `content` : Le contenu de la section, au format Markdown.
- `appendices` : La liste des points complémentaires de la section, au format Markdown.
