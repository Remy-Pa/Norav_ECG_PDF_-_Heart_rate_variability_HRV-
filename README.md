# Norav ECG PDF -> HRV
# Installer .exe / .exe latest release : https://github.com/Remy-Pa/Norav_ECG_PDF_-_Heart_rate_variability_HRV-/releases/tag/v1 VFC eco.exe au bas de la page

## English below

# Description générale
Ce logiciel offre une interface utilisateur pour extraire la variabilité de la fréquence cardiaque (VFC ; heart rate variability en anglais) d'enregistrements d'électrocardiograme (ECG). Il est nécessaire d'avoir en main en format PDF un enregistrement d'ECG provenant de la marque Norav. Le logiciel analyse un fichier PDF à la fois et permet d'analyser plusieurs parties de l'enregistrement indépendamment (utile par exemple, si chaque partie est associée à un traitement différent dans une étude). Ce logiciel a été développé comme alternative gratuite à des logiciels coûteux d'analyse de VFC (surtout dans un contexte académique).  

# Installation
Le logiciel est disponible en format exécutable (.exe). Le code source est également disponible pour effectuer un dépannage ou pour modifier le code. Exécuter le code source requiert l'installation de python 3 et de bibliothèques.  
Pour télécharger les bibliothèques nécessaire, sur windows, entrez dans l'invite de commande (CMD) :  
```
pip install customtkinter  
pip install numpy  
pip install scipy  
pip install pandas  
pip install pillow  
pip install opencv-python  
pip install matplotlib  
pip install pymupdf  
```
# Fonctionnement
Ce logiciel offre un interface utilisateur qui permet d'entrer plusieurs informations sur le participants pour permettre d'étiqueter correctement les fichiers (seul le fichier PDF est strictement obligatoire). Par la suite, le logiciel effectue une analyse en deux temps :  
1. Le logiciel lit chaque page du PDF désignée par l'utilisateur et détecte les pics R (du complexe QRS du tracé d'ECG) en débutant sur une ligne horizontale, détectant chaque fois que le tracé la traverse et tentant de 'monter' le long du tracé jusqu'à son sommet (supposément le sommet d'un pic R, corrélant à un battement de c&oelig;ur). Ainsi, la ligne de détection devrait être assez basse pour détecter tous les pics R (certains peuvent être plus bas que d'autres), mais assez haute pour ne pas détecter les autres composantes de l'ECG, comme l'onde p, par exemple.  
&nbsp;&nbsp;&nbsp;&nbsp;Le logiciel rend une image de chaque page, permettant de vérifier la bonne détection des pics R et de corriger les erreurs, s'il y a lieu, par l'interface utilisateur.  
2. Le logiciel  effectue des calculs relatifs à la VFC et retourne :  
&nbsp;&nbsp;&nbsp;&nbsp;RMSSD (root mean square of successive differences between RR intervals)  
&nbsp;&nbsp;&nbsp;&nbsp;pRR40 (percentage of subsequent RR intervals differing by more than 40 ms)  
&nbsp;&nbsp;&nbsp;&nbsp;SDRR (standard deviation of RR intervals)  
&nbsp;&nbsp;&nbsp;&nbsp;LF/HF (high frequencies/low frequencies after a Fourier transform)  
&nbsp;&nbsp;&nbsp;&nbsp;Fréquence cardiaque moyenne  
  
&nbsp;&nbsp;&nbsp;&nbsp;Ces métriques sont consignées dans un fichier .csv. À noter que les données peuvent être effacé par le logiciel. Il est prudent d'en faire des copies entre les participants pour éviter la perte de données.  
Voir https://doi.org/10.1111/j.1542-474X.1996.tb00275.x pour plus d'information sur la VFC.

# Compatibilité
Ce logiciel a été conçu et testé pour fonctionner avec les enregistrements PDF provenant du logiciel Norav Resting ECG. Le code pourrait facilement être changé pour accomoder un enregistrement PDF provenant d'un autre logiciel d'ECG. Par contre, il faudrait porter attention à :  
* Changer la région de l'image qui est occupée par le tracé, indentifiée par les variables 'debut' et 'fin', représentant l'espace en pixels à gauche et droite de la région de tracé, ainsi que la variable 'hauteur', le nombre de pixels entre le haut de l'image et la ligne de détection.  
* Changer le temps que cette région représente (en secondes).  
* Si plusieurs segments consécutifs de tracé se trouvent sur une même page, il faudrait modifier le code pour la lire plusieurs fois.  
* Changer la couleur de tracé (s'assurer qu'il n'y a pas d'interférence avec la couleur de l'arrière-plan).  
La compatibilité de la version exécutable (.exe) n'a pas été testée sur un autre système que Windows 11.  

# Problèmes connus
* L'écriture dans le fichier de résultat (.csv) peut parfois échouer et le fait de lancer le logiciel peut effacer les données au moment où il tente d'en écrire des nouvelles (environ 1 fois sur 5-15). Il peut être pertinent de sauvegarder des copies des fichiers entre chaque participant dont la VFC est analysée. Relancer le code devrait permettre de continuer l'analyse normalement (mais les anciennes données sont perdues sauf si elles ont été sauvegardées ailleurs).  
* Le fait de naviguer plusieurs fois dans les menus peut éventuellement mener à des erreurs. Si l'exécution est arrêtée et le code est relancé, il devrait fonctionner correctement.  
* Le logiciel peut parfois fermer incorrectement et demeurer actif après la fin de son exécution. Il peut être fermé en fermant le terminal (si le logiciel est exécuté à partir du code source) ou grâce au gestionnaire de tâches (task manager).
* Le logiciel pourrait être plus rapide si la manière de détecter les pixels noirs était différente (créer un tableau de booléens et vérifier les valeurs par index au lieu de vérifier chaque pixel plusieurs fois). Voir le commentaire dans Source code/VFC eco source.py à la ligne 514 dans draw_lines_and_find_highest().

## English version

# General description
This software offers a graphical user interface (GUI) to extract heart rate variability (HRV) from electrocardiogram (ECG) recording. It requires to have in hand a PDF file of an ECG recording coming from a Norav brand machine. The software analyses one file at a time and allows to analyse multiple parts of the recording independently (which is useful, for example, if each part is associated to a different treatment in a study). This software was developped as a free alternative to expensive softwares for HRV analysis (mostly in an academic context).  

# Installation
The software is available in executable file format (.exe) The source code is also available to troubleshoot problems or change parts of it. To execeute the source code, python 3 is required as well as some libraries and packages.  
To install the needed libraries and packages, on windows, type in the command prompt (CMD):  
```
pip install customtkinter
pip install numpy
pip install scipy
pip install pandas
pip install pillow
pip install opencv-python
pip install matplotlib
pip install pymupdf
```

# Mechanism
This software offers a GUI which allows input of information about a participant to identify the files (only the PDF file is strictly necessary).  
Then, the software analyses the file in two steps:  
1. The software reads each page of the PDF designated by the user and detects each R peak (from the QRS complexes of the ECG recording). It does so by looking along a row of the image and detecting each time the ECG line crosses this detection row. On each of these occurences, it attempts to 'go up' along the ECG line until it hits a peak (supposedly the top of an R peak, which correlates to a heart beat). That way, the detection row should be low enough to catch all R peaks (some can be lower than others), but high enough to not catch the other things such as, for example, p-waves.  
&nbsp;&nbsp;&nbsp;&nbsp;The software returns an image of each page showing where it identified each R peak, which can be verified and corrected through the GUI if necessary.  
2. The software calculates metrics relative to HRV and returns:  
&nbsp;&nbsp;&nbsp;&nbsp;RMSSD (root mean square of successive differences between RR intervals)  
&nbsp;&nbsp;&nbsp;&nbsp;pRR40 (percentage of subsequent RR intervals differing by more than 40 ms)  
&nbsp;&nbsp;&nbsp;&nbsp;SDRR (standard deviation of RR intervals)  
&nbsp;&nbsp;&nbsp;&nbsp;LF/HF (high frequencies/low frequencies after a Fourier transform)  
&nbsp;&nbsp;&nbsp;&nbsp;Mean heart rate  
  
&nbsp;&nbsp;&nbsp;&nbsp;These metrics are consigned in a .csv file. Note that the software sometimes irreversably deletes data from this file. It is wise to keep backup copies of the files between each participant to avoid all possible data loss.  
See https://doi.org/10.1111/j.1542-474X.1996.tb00275.x for more information on HRV metrics.

# Compatibility
The software is entirely in French, though it contains little text and could probably be modified successfully by asking ChatGPT to translate the strings from French to English. This software was made and tested to work with ECG recording from the Norav Resting ECG software. The code could easily be changed to accomodate a recording from a different software. For this, it would be important to:  
* Change the region which represents the graphing area, identified by the variables 'debut' and 'fin', representing the space in pixels which is to the left and right of the graphing area, as well as the variable 'hauteur', the distance (in pixels) between the top of the image and the detection line.
* Change the time (in seconds) which is plotted on each page of the recording.
* If your software returns multiple consecutive parts of the recording on a same page, the code must be changed to read each page multiple times.
* Make sure the color of the ECG line is the same (black) and that there is no inteference with the background color.  
Compatibility of the executable (.exe) has not been tested on systems other than Windows 11.  

# Known problems
* The writing in the results file can sometimes fail and the fact of running the software can erase current data at the moment when the software attempts to write into the file (about 1 out of 5-15 times). It is wise to save backup copies of the result file between each run of the software (each participant PDF file). Re-running the code usually fixes the issue (but the old data is lost unless it was backed up elsewhere).  
* The fact of navigating in back and forth through the menus can eventually lead to errors. If the execution is stopped and the code is re-run, it should go back to normal.  
* The software can sometimes end itself incorrectly and remain active after the end of its execution. It can be stopped by killing the terminal running it (if the source code is being used) or through task manager.  
* The .exe version can be harder to use due to unexpected errors which can be hard to troubleshoot and debug.
* The software could probably be faster if the way of detecting the black pixels was changed to creating a boolean array of a part of each page where the values can then be checked by index (current method might check for pixel color multiple times). See comment in Source code/VFC eco source.py at ligne 514 in draw_lines_and_find_highest().
