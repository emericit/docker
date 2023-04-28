# docker

## Tests en Python

On crée la série de tests dans des boucles `for`. En fonction du test à faire,
on fait une boucle sur les `credentials` et/ou la version (`v1`ou `v2`) de l'API,
et/ou la `sentence` pour laquelle on veut calculer le sentiment.

L'URL est construite en fonction de ces paramètres.
On fait ensuite la requête HTTP avec `requests.get()`.

On vérifie que le code de retour est bien `200` pour un utilisateur valide ayant
les permissions nécessaires, et `403` pour un utilisateur invalide ou n'ayant pas
les droits.

On vérifie que le résultat du score est bien un nombre négatif pour la phrase `that sucks` et
positif pour la phrase `life is beautiful`.
Il semble que les versions `v1` et `v2` de l'API donnent à chaque fois les mêmes résultats.

## Fichier de log

La librairie `logging` permet de créer facilement un fichier de log `api_test.log`. L'avantage est 
que la plupart du temps, on aura un visuel plus agréable avec des couleurs, et une mise en évidence
des messages d'erreur.
On a choisi de créer un logger qui contient deux `Handler`:
- un `StreamHamdler` pour la console, avec le niveau `WARNING`. La console affiche donc les messages
  de niveau `WARNING`, `ERROR` et `CRITICAL`, qui correspondent à des résultats différents des résultats
  attendus.
- un `FileHandler` dans le fichier `api_test.log`, de niveau `DEBUG`. Le fichier de log contient donc
  tous les messages, y compris ceux de niveau `INFO` et `DEBUG`. Les résultats conformes aux
  attentes sont donc aussi dans le fichier de log.


## Dockerfile

J'ai choisi de partir de l'image `alpine` qui est très légère, et d'installer la dépendance `requests`
en faisant 
```
RUN pip install
```

## Script bash

Il contient 3 commandes 
```
docker build -t XXX ./XXX
```
pour construire chacune des images `authentication`, `authorization` et `content`.
C'est redondant avec le `docker-compose.yml`, puisque j'ai mis une section `build` pour chacune des images,
mais ça permet de tester les images une par une.

La dernière commande lance
```
docker-compose up
```
qui lance les 4 containers en même temps (nos 3 + celui de l'API), et affiche les logs de chacun d'eux.

## docker-compose.yml

### `networks`
Pour que les images puissent communiquer entre elles, il faut les mettre dans le même réseau. 
De plus, si ce réseau est un réseau défini par l'utilisateur (et non pas le `bridge` par défaut), les
images peuvent communiquer entre elles par leur nom de service (et non pas par leur IP). C'est tellement
pratique qu'il ne faut pas s'en priver. Je crée donc un réseau `test_suite` dans le `docker-compose.yml`,
sur lequel tournent les 4 images.

### `depends on`
Pour que les images `authentication`, `authorization` et `content` puissent communiquer avec l'API, il faut
que l'API soit lancée avant. On peut le faire en ajoutant une dépendance dans le `docker-compose.yml`:
```
depends_on:
  - api
```

### `environment`
On passe une variable d'environnement à nos 3 images, donnant le nom d'hôte du service `api` dans le réseau.
Ensuite dans le script, on la récupère avec `os.environ.get('API_HOST', 'localhost')`. Quand on lance
en local sur la machine hôte, sans définir la variable d'environnement, `localhost` est bien le bon nom d'hôte. 

Il y a aussi une variable d'environnement `LOG`, qui active l'écriture des logs dans le fichier `api_test.log`.

### `volumes`
On a monté le dossier courant des images `alpine` dans `/usr/src/app`. On crée un sous-répertoire
`logs` pour y mettre le fichier de log `api_test.log`. Quand le script est lancé, il écrit dans ce fichier,
et crée le répertoire au besoin.

On veut récupérer seulement ce répertoire depuis la machine hôte, et pas tout le dossier courant. Sinon il y aurait
un problème de sécurité, puisqu'on verrait tout le code source de l'application dans le dossier monté.
