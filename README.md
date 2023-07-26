# fff_referees_articles_scraping.py

Ce projet consiste en un script Python qui effectue le web scraping du site Web de la Fédération Française de Football (FFF) pour récupérer les articles de la section "Arbitrage". Le script vérifie si de nouveaux articles contiennent certains mots-clés spécifiques tels que "évaluation", "classement" ou "résultat" et envoie une notification par e-mail via l'API MailJet si tel est le cas.

## Prérequis

Avant d'exécuter le script, assurez-vous d'avoir installé les bibliothèques Python suivantes:

- `requests`
- `beautifulsoup4`
- `pandas`
- `datetime`
- `os`
- `smtplib`
- `config` (fichier de configuration contenant les informations d'authentification pour l'API MailJet)
- `mailjet_rest` (API MailJet pour l'envoi d'e-mails)
- `unidecode`

Installez les bibliothèques avec la commande suivante:

``` bash
pip install requests beautifulsoup4 pandas mailjet_rest unidecode
```

## Utilisation

1. Clonez le dépôt sur votre système local.

2. Assurez-vous d'avoir rempli le fichier `config.py` avec les informations d'authentification requises pour l'API MailJet

3. Exécutez le script Python:

``` bash
python fff_referees_articles_scraping.py
```

Le script récupérera les articles de la FFF, les enregistrera dans un fichier CSV et vérifiera s'il y a de nouveaux articles depuis la dernière exécution. Si un nouvel article contenant les mots-clés spécifiés est trouvé, il enverra une notification par e-mail.

## Structure du projet

- `fff_referees_articles_scraping.py`: Le script principal de web scraping.
- `config.py`: Fichier de configuration contenant les informations d'authentification pour l'API MailJet.
- `fff_results_log.txt`: Fichier de journalisation pour enregistrer les résultats des exécutions du script.
- D'autres fichiers CSV sont créés pour enregistrer les résultats du scraping (supprimés si plus de 10 fichiers sont présents).

## Avertissement

Le scraping de sites Web peut être contraire aux conditions d'utilisation du site Web. Assurez-vous de vérifier les politiques du site Web concerné avant d'utiliser ce script. Utilisez ce script à vos propres risques.

**Avertissement de responsabilité**: Ce projet est fourni à titre éducatif seulement. L'auteur ne sera pas responsable de toute utilisation abusive ou illégale de ce code.
