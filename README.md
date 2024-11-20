# Norav ECG PDF -> HRV

## English below

# Description générale
Ce programme offre un interface utilisateur pour extraire la variabilité de la fréquence cardiaque (VFC ; heart rate variability en anglais).
Il est nécessaire d'avoir en main un enregistrement en format PDF d'un enregistrement d'ECG provenant de la marque Norav.
Le programme analyse un fichier PDF à la fois et permet d'analyser plusieurs parties de l'enregistrement indépendamment (par exemple, si chaque partie est associée à un traitement différent dans une étude).
Ce programme a été développé comme alternative gratuite à des programmes coûteux d'analyse de VFC.

# Téléchargement 
Le programme est disponible en format exécutable (.exe).
Le code source est également disponible pour effectuer un dépannage ou pour modifier le code. Exécuter le code source requiert l'installation de python 3 et de bibliothèques.
Pour télécharger les bibliothèques nécessaire, sur windows, entrez dans l'invite de commande (CMD) :
  pip install # ... à venir

# Fonctionnement
Ce programme offre un interface utilisateur qui permet d'entrer plusieurs informations sur le participants (seul le fichier PDF est strictement obligatoire).
Par la suite, le programme effectue une analyse en deux temps :
  1) Le programme lit chaque page désignée du PDF et détecte les pics R (du complexe QRS du tracé d'ECG)
       Le programme rend une image de chaque page, permettant de vérifier la bonne détection des pics R et de corriger les errerus, s'il y a lieu, par l'interface utilisateur.
  2) Le programme  effectue des calculs relatifs à la VFC et retourne :
       RMSSD (root mean square of successive differences between RR intervals)
       pRR40 (percentage of subsequent RR intervals differing by more than 40 ms)
       SDRR (standard deviation of RR intervals)
       LF/HF (high frequencies/low frequencies after a Fourier transform)
       Fréquence cardiaque moyenne

       Ces métriques sont consignées dans un fichier .csv QUI PEUT SE MONTRER INSTABLE. Il est prudent d'en faire des copies entre les participants pour éviter la perte de données.

# Compatibilité
Ce programme a été conçu et testé pour fonctionner avec les enregistrements PDF provenant du logiciel Norav Resting ECG.
Le code pourrait facilement être changé pour accomoder un enregistrement PDF provenant d'un autre logiciel d'ECG. Par contre, il faudrait porter attention à :
  Changer la région de l'image qui est occupée par le tracé
  Changer le temps que cette région représente (en secondes) 
  Si plusieurs segments consécutifs de tracé se trouvent sur une même page, il faudrait modifier le code pour la lire plusieurs fois
  Changer la couleur de tracé (s'assurer qu'il n'y a pas d'interférence avec la couleur de l'arrière-plan)
La compatibilité de la version exécutable (.exe) n'a pas été testée sur un autre système que Windows 11.

# Problèmes connus
Le fichier de résultat est instable et le fait de lancer le programme peut effacer les données au moment où il tente d'en écrire des nouvelles. Il peut être pertinent de sauvegarder des copies des fichiers entre chaque participant dont la VFC est analysée. Relancer le code devrait permettre de continuer l'analyse normalement (mais les anciennes données sont perdues sauf si elles ont été sauvegardées ailleurs)
Le fait de naviguer plusieurs fois dans les menus peut éventuellement mener à des erreurs. Si le code est arrêté et relancé, il devrait fonctionner correctement.
Le programme peut parfois fermer incorrectement et demeurer actif après la fin de son exécution. Il peut être fermé en fermant le terminal (si le programme est exécuté à partir du code source) ou grâce au gestionnaire de tâches (task manager).

# General description
This program offers a user interface to extract heart rate variability (HRV)
