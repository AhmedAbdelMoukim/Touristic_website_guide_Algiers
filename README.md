# Alger, la Blanche — INFO4006 Multimédia

## Ouvrir le site
Ouvrir index.html dans Chrome, Edge ou Firefox. Aucun framework, compilation ou installation n’est nécessaire.
Toutes les pages, photos, polices, Bootstrap, le diaporama et la narration sont locaux.
La vidéo UNESCO intégrée et les liens externes nécessitent Internet. YouTube peut refuser l’intégration lorsque la page est ouverte en file:// ; le lien UNESCO reste disponible.

Pour utiliser le lecteur externe dans de meilleures conditions, ouvrir un terminal dans ce dossier :
~~~powershell
python -m http.server 8000 --bind 127.0.0.1
~~~
Puis visiter http://127.0.0.1:8000 . Arrêter le serveur avec Ctrl+C.

## Pages
- index.html : accueil, identité, introduction, incontournables et appels à l’action.
- apropos.html : histoire, quatre lieux, citation, itinéraire en tableau, carnet local et accordéon.
- multimedia.html : sept photographies filtrables et agrandissables, vidéo locale, audio et vidéo externe.
- contact.html : formulaire complet avec validation et confirmation locale.

## Fonctionnalités
Le carnet utilise localStorage et ne conserve que les noms des lieux. Cliquer à nouveau sur un lieu pour le retirer ou utiliser « Vider mon carnet ». Si le stockage est refusé, le carnet fonctionne temporairement sur la page.

Le formulaire est pédagogique : aucun envoi, aucune réservation, aucune collecte des données. L’adresse en .example du pied de page est volontairement fictive et identifiée comme telle.

## Livrables et médias
- css/style.css : styles personnalisés ; css/fonts.css : polices locales.
- js/main.js : galerie, modale, carnet et formulaire.
- images/ : photos WebP en plusieurs tailles et logo SVG original.
- video/alger-jour-nuit.mp4 : diaporama original, muet, 28 secondes, H.264 1280×720 ; légendes VTT.
- audio/bienvenue-alger.mp3 : narration française par voix de synthèse ; transcription séparée.
- vendor/ : Bootstrap 5.3.3 local, licence MIT dans les en-têtes.
- fonts/ : Google Fonts et licences OFL.
- JUSTIFICATION-TECHNIQUE.md : justification de 200 à 300 mots.
- SOURCES-ET-CREDITS.md : provenance des médias et informations.
- VERIFICATION.md : contrôles et limites de vérification.

## Vérification visuelle avant remise
Le navigateur automatisable n’était pas disponible pendant la réalisation. Les contrôles de code ne remplacent donc pas une validation visuelle.

Dans les outils de développement du navigateur, vérifier les quatre pages à 375, 768 et 1280 pixels :
1. Navigation mobile : ouvrir le hamburger, suivre les quatre liens.
2. Vérifier l’absence de défilement horizontal de la page ; le tableau a son propre défilement.
3. Galerie : tester les cinq filtres, ouvrir une photo, fermer avec Échap et au bouton.
4. Carnet : ajouter et retirer un lieu, actualiser puis vider.
5. Lire la vidéo locale et la narration ; vérifier le film externe avec une connexion.
6. Formulaire : essayer vide, avec un courriel incorrect, puis avec des données de démonstration valides.
7. Parcourir au clavier : lien d’évitement, navigation, contrôles et formulaire.

Les durées de l’itinéraire sont des suggestions, pas des horaires officiels. Aucun tarif ou horaire d’ouverture n’est inventé.
