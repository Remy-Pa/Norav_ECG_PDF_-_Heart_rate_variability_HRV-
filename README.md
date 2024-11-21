# Norav ECG PDF -> HRV
# Installer .exe / .exe latest release : https://github.com/Remy-Pa/Norav_ECG_PDF_-_Heart_rate_variability_HRV-/releases/tag/v1

## English below

# Description générale
Ce programme offre un interface utilisateur pour extraire la variabilité de la fréquence cardiaque (VFC ; heart rate variability en anglais) d'enregistrements d'électrocardiograme (ECG).  
Il est nécessaire d'avoir en main un enregistrement en format PDF d'un enregistrement d'ECG provenant de la marque Norav.  
Le programme analyse un fichier PDF à la fois et permet d'analyser plusieurs parties de l'enregistrement indépendamment (utile par exemple, si chaque partie est associée à un traitement différent dans une étude).  
Ce programme a été développé comme alternative gratuite à des programmes coûteux d'analyse de VFC (surtout dans un contexte académique).  

# Installation
Le programme est disponible en format exécutable (.exe).  
Le code source est également disponible pour effectuer un dépannage ou pour modifier le code. Exécuter le code source requiert l'installation de python 3 et de bibliothèques.  
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
Ce programme offre un interface utilisateur qui permet d'entrer plusieurs informations sur le participants pour permettre d'étiqueter correctement les fichiers (seul le fichier PDF est strictement obligatoire).  
Par la suite, le programme effectue une analyse en deux temps :  
&nbsp;&nbsp;1) Le programme lit chaque page du PDF désignée par l'utilisateur et détecte les pics R (du complexe QRS du tracé d'ECG) en débutant sur une ligne, détectant chaque fois que le tracé la traverse et tentant de 'monter' le long du tracé jusqu'à son sommet (supposément un pic R).  
&nbsp;&nbsp;&nbsp;&nbsp;Le programme rend une image de chaque page, permettant de vérifier la bonne détection des pics R et de corriger les errerus, s'il y a lieu, par l'interface utilisateur.  
&nbsp;&nbsp;2) Le programme  effectue des calculs relatifs à la VFC et retourne :  
&nbsp;&nbsp;&nbsp;&nbsp;RMSSD (root mean square of successive differences between RR intervals)  
&nbsp;&nbsp;&nbsp;&nbsp;pRR40 (percentage of subsequent RR intervals differing by more than 40 ms)  
&nbsp;&nbsp;&nbsp;&nbsp;SDRR (standard deviation of RR intervals)  
&nbsp;&nbsp;&nbsp;&nbsp;LF/HF (high frequencies/low frequencies after a Fourier transform)  
&nbsp;&nbsp;&nbsp;&nbsp;Fréquence cardiaque moyenne  
  
&nbsp;&nbsp;&nbsp;&nbsp;Ces métriques sont consignées dans un fichier .csv QUI PEUT SE MONTRER INSTABLE. Il est prudent d'en faire des copies entre les participants pour éviter la perte de données.  

# Compatibilité
Ce programme a été conçu et testé pour fonctionner avec les enregistrements PDF provenant du logiciel Norav Resting ECG.  
Le code pourrait facilement être changé pour accomoder un enregistrement PDF provenant d'un autre logiciel d'ECG. Par contre, il faudrait porter attention à :  
&nbsp;&nbsp;&nbsp;&nbsp;Changer la région de l'image qui est occupée par le tracé, indentifiée par les variables 'debut' et 'fin', représentant l'espace en pixels à gauche et droite de la région de tracé, ainsi que la variable 'hauteur', le nombre de pixels entre le haut de l'image et la ligne de détection.  
&nbsp;&nbsp;&nbsp;&nbsp;Changer le temps que cette région représente (en secondes)  
&nbsp;&nbsp;&nbsp;&nbsp;Si plusieurs segments consécutifs de tracé se trouvent sur une même page, il faudrait modifier le code pour la lire plusieurs fois.  
&nbsp;&nbsp;&nbsp;&nbsp;Changer la couleur de tracé (s'assurer qu'il n'y a pas d'interférence avec la couleur de l'arrière-plan)  
La compatibilité de la version exécutable (.exe) n'a pas été testée sur un autre système que Windows 11.  

# Problèmes connus
L'écriture dans le fichier de résultat (.csv) est instable et le fait de lancer le programme peut effacer les données au moment où il tente d'en écrire des nouvelles (environ 1 fois sur 5-15). Il peut être pertinent de sauvegarder des copies des fichiers entre chaque participant dont la VFC est analysée. Relancer le code devrait permettre de continuer l'analyse normalement (mais les anciennes données sont perdues sauf si elles ont été sauvegardées ailleurs)  
Le fait de naviguer plusieurs fois dans les menus peut éventuellement mener à des erreurs. Si le code est arrêté et relancé, il devrait fonctionner correctement.  
Le programme peut parfois fermer incorrectement et demeurer actif après la fin de son exécution. Il peut être fermé en fermant le terminal (si le programme est exécuté à partir du code source) ou grâce au gestionnaire de tâches (task manager).  
La version .exe peut être plus difficile d'utilisation par cause d'erreurs inattendues qui ne peuvent pas être dépannées de manière efficace.  

## English version

# General description
This program offers a graphical user interface (GUI) to extract heart rate variability (HRV) from electrocardiogram (ECG) recording.  
It requires to have in hand a PDF file of an ECG recording coming from a Norav brand machine.  
The program analyses one file at a time and allows to analyse multiple parts of the recording independently (which is useful, for example, if each part is associated to a different treatment in a study).  
This program was developped as a free alternative to expensive programs for HRV analysis (mostly in an academic context).  

# Installation
The program is available in executable file format (.exe)  
The source code is also available to troubleshoot problems or change parts of it. To execeute the source code, python 3 is required as well as some libraries and packages.  
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

# Mecanism
This program offers a GUI which allows input of information about a participant to identify the files (only the PDF file is strictly necessary).  
Then, the program analyses the file in two steps :  
&nbsp;&nbsp;1) The program reads each page of the PDF designated by the user and detects each R peak (from the QRS complexes of the ECG recording). It does so by looking at a line and detecting each time the ECG line traverses this detection line. On each of these occurences, it attempts to 'go up' along the ECG line until it hits a peak (supposedly an R peak).  
&nbsp;&nbsp;&nbsp;&nbsp;The program returns an image of each page showing where it identified each R peak, which can be verified and corrected through the GUI if necessary.  
&nbsp;&nbsp;2) The program calculates metrics relative to HRV and returns :  
&nbsp;&nbsp;&nbsp;&nbsp;RMSSD (root mean square of successive differences between RR intervals)  
&nbsp;&nbsp;&nbsp;&nbsp;pRR40 (percentage of subsequent RR intervals differing by more than 40 ms)  
&nbsp;&nbsp;&nbsp;&nbsp;SDRR (standard deviation of RR intervals)  
&nbsp;&nbsp;&nbsp;&nbsp;LF/HF (high frequencies/low frequencies after a Fourier transform)  
&nbsp;&nbsp;&nbsp;&nbsp;Mean heart rate  
  
&nbsp;&nbsp;&nbsp;&nbsp;These metrics are consigned in a .csv file WHICH CAN BE UNSTABLE. It is wise to keep backup copies of the files between each participant to avoid all possible data loss.  

# Compatibility
The program is entirely in French, though it contains little text and could probably be modified successfully by asking ChatGPT to translate the strings from French to English.
This program was made and tested to work with ECG recording from the Norav Resting ECG software.  
The code could easily be changed to accomodate a recording from a different software. For this, it would be important :  
  Change the region which represents the graphing area, identified by the variables 'debut' and 'fin', representing the space in pixels which is to the left and right of the graphing area, as well as the variable 'hauteur', the distance (in pixels) between the top of the image and the detection line.  
  Change the time (in seconds) which is plotted on each page of the recording.  
  If your software returns multiple consecutive parts of the recording on a same page, the code must be changed to read each page multiple times.  
  Make sure the color of the ECG line is the same (black) and that there is no inteference with the background color.  
Compatibility of the executable (.exe) has not been tested on systems other than Windows 11.  

# Known problems
The writing in the results file is unstable and the fact of running the program can erase current data at the moment when the program attempts to write into the file (about 1 out of 5-15 times). It is wise to save backup copies of the result file between each run of the program (each participant PDF file). Re-running the code usually fixes the issue (but the old data is lost unless it was backed up elsewhere).  
The fact of navigating in back and forth through the menus can eventually lead to errors. If the code is stopped and re-run, it should go back to normal.  
The program can sometimes end itself incorrectly and remain active after the end of its execution. It can be stopped by killing the terminal running it (if the source code is being used) or through task manager.  
The .exe version can be harder to use due to unexpected errors which can be hard to troubleshoot.  
