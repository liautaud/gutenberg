![Conveyor](http://amaia.at/conveyor.png)

*Un générateur automatique de diffusions pour les associations de l'ENS de Lyon.*

## Présentation.

*Conveyor* est un utilitaire en ligne de commande qui permet de générer automatiquement des diffusions e-mail de plusieurs associations de l'ENS de Lyon. Il attend en entrée un fichier YAML dont le schéma est décrit ci-dessous, et renvoie le code HTML correspondant au corps de l'e-mail généré.

```
./conveyor 2017-09-15.yml --out=2017-09-15.html
```

## Format d'entrée.

Les fichiers traités par *Conveyor* doivent être au format YAML.

Ils doivent contenir les champs suivants :
- `author` : L'auteur de la diffusion, au format `Prénom Nom <email>`.
- `title` : Le titre de la diffusion *(qui apparaîtra notamment dans l'en-tête)*.
- `subtitle` : Le sous-titre de la diffusion, le cas échéant.
- `date` : La date de la diffusion, au format `1977-04-22`.
- `template` : Le thème à utiliser pour la diffusion. Pour l'instant, sont disponibles `enscene-diffusion` et `enscene-programmation`.

Le reste des champs dépend de la valeur de `template`. On retrouve en général :
- `greeting` : La formule d'appel à utiliser en début de diffusion.
- `introduction` : Le texte d'introduction de la diffusion, au format Markdown.
- `sections` : La liste des sections de la diffusion.

Chaque section contient en général les champs suivants :
- `title` : Le titre de la section.
- `type` : Le type de la section, parmi `theater`, `dance`, `music`, `other`.
- `image` : L'image qui accompagne la section, le cas échéant.
- `align` : La position de l'image par rapport au texte, parmi `left` et `right`.
- `dates` : La liste des dates de l'événement, le cas échéant, au format `1977-04-22 01:00`.
- `place` : Le lieu de l'événement, le cas échéant.
- `content` : Le contenu de la section, au format Markdown.
- `appendices` : La liste des points complémentaires de la section, au format Markdown.
