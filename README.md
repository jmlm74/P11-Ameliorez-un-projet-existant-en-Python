# P10 - Déployez !

# P10 du parcours DA Python d'OpenClassRoom

## Déployez votre application sur un serveur comme un pro !

Jusqu’à maintenant, vous avez déployé vos applications en utilisant Heroku. C’est bien ! Mais la plupart des sociétés n’utilisent pas Heroku, pas par mépris pour cette belle entreprise mais plutôt car elles préfèrent gérer elles-mêmes leur déploiement.  
  
Il s’agit d’une étape très importante dans la vie d’un projet ! Allez, c’est parti !  


### Étapes  
#### 1 - Simuler un serveur de production en local  
Avant de mettre en ligne un projet, il est de bon ton de lancer un serveur en local pour s’assurer que tout se passe bien.  
[Incassable, incassable !](https://www.youtube.com/watch?v=85E1YY-P7_g&t=0m38s)  

Vous souvenez-vous des avantages de l’intégration continue ? Entre autre, cette méthodologie vous permet d’intégrer de nouvelles fonctionnalités à un projet en courant le moins de risques possibles. Les tests que vous avez écrits sont exécutés à chaque nouveau push. Si les tests échouent, une alerte s’affiche et rien n’est déployé.  

Il existe de nombreux outils d’intégration continue mais mon chouchou, je dois bien l’avouer, est Travis (suivez le guide ). Pas à cause de son petit nom, de ses moustaches affriolantes ou de son chapeau si hipster (quoique…), mais plutôt en raison de sa simplicité.  

Néanmoins, sachez que vous pouvez utiliser l’outil qui vous sied le mieux.  

#### 2 - Déploiement   
Tous vos tests sont verts et le build fonctionne ? Parfait ! Maintenant, déployez votre application en utilisant l’hébergeur que vous souhaitez. Vous devez configurer le serveur et effectuer un déploiement en ligne de console. N’utilisez pas Heroku ;-)  

#### 3 - Monitoring  
Votre application est en ligne. Bravo ! Mais que se passe-t-il si le serveur tombe en panne ? Utilisez Sentry pour lire tous les logs et NewRelic pour surveiller le bon fonctionnement de votre application.  

#### 4 - Automatisations  
Créez une tâche Cron qui mettra à jour les éléments récupérés d’Open Food Facts une fois par semaine.  

#### 5 - Nom de domaine  
Dernière étape (optionnelle) ! Achetez un nom de domaine et reliez-le à vos serveurs. 

## Livrables  
[Démarche](/Livrables/P10_01_demarche.pdf) - Démarche  
[Crontab](/Livrables/P10_02_crontab.png) - Crontab  
[Monitoring](/Livrables/P10_03_Monitoring.png) - Monitoring  
[Monitoring](/Livrables/P10_04_Monitoring.png) - monitoring  
[Monitoring - Alertes](/Livrables/P10_05_Monitoring-Alert.png) - Alertes  
[Travis-CI](/Livrables/P10_06_Travis-CI.png) - Travis-CI  
[Sentry](/Livrables/P10_07_Sentry.png) - Sentry  
[Init_db](/Livrables/P10_08_initdb.png) - Initialisation BdD  
[Docker-Hub](/Livrables/P10_09_Docker.png) - Dashboard Docker-Hub  
[Docker_maj](/Livrables/P10_10_Docker_maj1.png) - Mise a jour conteneurs docker  
[Monitor.sh](/Livrables/P10_12_monitor.sh) - Monitoring services (script)  
[Présentation](/Livrables/presentation.pdf) - Présentation  

[Application](https://purbeurre.jm-hayons74.fr/) - Application

