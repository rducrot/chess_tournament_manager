# Chess Tournament Manager
[![Python](https://badgen.net/badge/Python/3.8/blue)](https://www.python.org/)
## Description
Ce logiciel permet de gérer le déroulement d'un tournoi d'échecs.

### Menu :
1. **Gérer les informations du tournoi** : Permet d'afficher/modifier les informations du tournoi[^1].
2. **Gérer la liste des joueurs** : Permet d'afficher/modifier la liste des joueurs[^1].
3. **Entrer les scores du tournoi en cours** : Lance le déroulement du tournoi. Les joueurs sont appariés automatiquement en fonction du tour. Permet d'entrer le résultat de chaque match[^2].
4. **Charger les données d'un tournoi passé/en cours** : Charge les informations d'un tournoi terminé ou ayant effectué au moins un tour[^2].
5. **Voir les rapports** : Affiche plusieurs sortes de rapports. Cette option ne s'affiche que si tous les tours du tournoi ont été effectués.

## Installation
Depuis un terminal, placez-vous au dossier racine du projet, puis lancez les commandes suivantes :
```bash
python3 -m venv venv # Mise en place de l'environnement virtuel
venv/bin/activate # Activation de l'environnement virtuel
pip3 install -r requirements.txt # Les librairies doivent être installées depuis l'environnement virtuel.
```
## Exécution
Le logiciel se lance depuis l'environnement virtuel de la manière suivante :
```bash
python3 main.py
```
## Générer un rapport flake8-html
Un rapport flake8 est consultable depuis le fichier ```flake8_rapport/index.html```.

Pour générer un nouveau rapport, entrez la commande suivante depuis le dossier du projet :
```bash
flake8 --format=html --htmldir=flake8_rapport
```
[^1]: Les joueurs ou les caractéristiques d'un tournoi peuvent être récurrents. Afin de ne pas avoir besoin d'entrer ces informations à chaque lancement du logiciel, celles-ci sont enregistrées dans le fichier ```db.json```. Ce fichier est chargé automatiquement au lancement du logiciel s'il est présent.
[^2]: Un rapport peut être généré à tout moment entre deux tours ou à la fin du tournoi dans le fichier ```report.json```.\
Si un tournoi est interrompu, qu'un rapport est généré et que celui-ci est chargé, le déroulement du tournoi reprend au tour suivant.
