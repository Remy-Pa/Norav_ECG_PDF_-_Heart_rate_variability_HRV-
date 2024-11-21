import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import *
from tkinter import messagebox
import customtkinter as ctk
from PIL import ImageTk, Image
import numpy as np
import cv2 as cv2 
import os
import pandas as pd
import csv
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
import fitz
import time
from contextlib import contextmanager
import sys 
import shutil

# ####
# PRIORITÉS                                                                                                                     
# 1) faire marcher mode stat                                                                                                    FAIT
# 2) faire marcher mode graph                                                                                                   FAIT
# 3) porter mode overnight                                                                                                      FAIT
# 4) faire un outil pour manuellement placer les pics R                                                                         FAIT
# 5) changer la facon dont le fichier resultats normal est écrit? # nbs max si ammeton tu commence a 1 pis tu ajoute 3...       FAIT
# 6) Rendre beau, icone, logo, titres                                                                                           FAIT
# 7) mode fast a pas vrm de output image                                                                                        FAIT
# 8) save dans le dossier PDF                                                                                                   FAIT
# 9) verifier si cest harmonieux quand il pense trouver des artefacts

# derniere etape) .exe AVEC LOGO
# Tester avec mes data

# ####

# a verifier
                                    #   un participant du debut a la fin


#   un participant etape 2
#   plusieurs participants partie 1
#   plusieurs participants partie 2


####################################
########## DEFINITIONS #############
####################################

@contextmanager
def permission_error() :
    n =1
    while True :
        print(n)
        n += 1
        try :
            yield
            break
        except PermissionError : 
            summon_err_window('Une erreur est survenue, veuillez fermer les fichiers csv de résultats et fermer cette fenêtre.')
            time.sleep(0.4)

def summon_err_window(message) :
    messagebox.showerror('VFC eco - Erreur', message)

def mettre_images_exe(path) :
    if hasattr(sys, '_MEIPASS') :
        return os.path.join(sys._MEIPASS, path)
    else :
        return os.path.join(os.path.abspath('.'), path)    

def make_parent(titre, geometrie) :
    win = tk.Tk()
    win.title(titre)
    win.geometry(geometrie)
    win.resizable(False, False)
    filename = mettre_images_exe("C:\\Users\\remyp\\VFC eco logo partial.ico")
    icone = ImageTk.PhotoImage(file = filename)
    win.iconphoto(False, icone)
    win.icone = icone
    return win

def make_window(titre, geometrie) :
    win = tk.Toplevel(window_mode)
    win.title(titre)
    win.geometry(geometrie)
    win.resizable(False, False)
    filename = mettre_images_exe("C:\\Users\\remyp\\VFC eco logo partial.ico")
    icone = ImageTk.PhotoImage(file = filename)
    win.iconphoto(False, icone)
    win.icone = icone
    return win

def on_entry_click(event, prompt, value) :
    if prompt.get() == value :
        prompt.delete(0, "end") 
        prompt.insert(0, '') 

def focus_out(event, prompt, value) :
    if prompt.get() == '':
        prompt.insert(0, value)

def give_binds(prompt, value) :
    prompt.bind('<FocusIn>', lambda event : on_entry_click(event, prompt, value))
    prompt.bind('<FocusOut>', lambda event : focus_out(event, prompt, value))

def on_entry_click_hauteur(event):
    hauteur_spinbox.delete(0, "end")
    hauteur_spinbox.insert(0, '')

def on_focus_out_hauteur(event) :
    if hauteur_spinbox.get() == '' :
        hauteur_spinbox.insert(0, '0')

def un_part_slow() :
    global mode, speed
    mode = 'un_part'
    speed = 'vitesse normale'
    window_mode.withdraw()
    un_part_etape_1()

def un_part_fast() :
    global mode, speed
    mode = 'un_part'
    speed = 'rapide'
    window_mode.withdraw()
    un_part_etape_1()

# def plusieurs_part_slow() :
#     global mode, speed
#     mode = 'plusieurs_part'
#     speed = 'vitesse normale'
#     window_mode.withdraw()
#     plusieur_part_etape_1()
#     plusieurs_part_etape2()
    
# def plusieurs_part_fast() :
#     global mode, speed
#     mode = 'plusieurs_part'
#     speed = 'rapide'
#     window_mode.withdraw()
#     plusieur_part_etape_1()
#     plusieurs_part_etape2()

def etape_conf() :
    global etape_var
    etape_var = tk_etape_var.get()

def stat_mode() :
    global stat_var
    if stat_var_int.get() == 1 :
        stat_var = True
    elif stat_var_int.get() == 0 :
        stat_var = False 

def make_main_window() :
    global window_mode, stat_var, corring, window2, browse_folder_entry, parent_exist, tk_etape_var, stat_var_int, graph_mode_int
    
    try :
        try :
            window_corr.destroy()
        except :
            window1.destroy()
    except NameError :
        pass

    if not parent_exist :
        window_mode = make_parent('VFC eco - Menu principal', '920x270+70+70')
        parent_exist = True

    logo_display = tk.Canvas(window_mode, width = 660, height = 220)
    logo_display.grid(row = 0, column = 0, columnspan = 4, rowspan = 8)

    filename = mettre_images_exe("C:\\Users\\remyp\\VFC eco full logo.png")
    logo = Image.open(filename)
    logo = logo.resize((660, 220))
    logo_tk = ImageTk.PhotoImage(logo)
    logo_display.image = logo_tk
    logo_display.create_image(0,0, anchor = tk.NW, image = logo_tk)

    # lancer_label = tk.Label(window_mode, text = 'Appuyez sur un boutton pour lancer le logiciel')
    # lancer_label.grid(row = 0, column = 4, columnspan = 2, pady = 10)

    un_part_slow_bouton = ttk.Button(window_mode, text = '''Lancer l'analyse''', command = lambda : [stat_mode(), graph_mode_(), print(stat_var, graph_mode),etape_conf(), un_part_slow()])
    un_part_slow_bouton.grid(row = 8, column = 0, pady = 10, padx = 10)

    un_part_fast_bouton = ttk.Button(window_mode, text = '''Lancer l'analyse (mode rapide)''', command = lambda : [stat_mode(), graph_mode_(), etape_conf(), un_part_fast()])
    un_part_fast_bouton.grid(row = 8, column = 1, padx = 10, pady = 10)

    # plusieurs_part_slow_bouton = ttk.Button(window_mode, text = 'Plusieurs PDF', command = lambda : [etape_conf(), plusieurs_part_slow()])
    # plusieurs_part_slow_bouton.grid(row = 1, column = 5, padx = 10, pady = 10)

    # plusieurs_part_fast_bouton = ttk.Button(window_mode, text = 'Plusieurs PDF (rapide)', command = lambda : [etape_conf(), plusieurs_part_fast()])
    # plusieurs_part_fast_bouton.grid(row = 2, column = 5, padx = 10, pady = 10)

    rr_correct_button = ttk.Button(window_mode, text = 'Corriger les pics R', command = rr_correct)
    rr_correct_button.grid(row = 8, column = 2, padx = 10, pady = 10)

    param_label = tk.Label(window_mode, text = 'Paramètres')
    param_label.grid(row = 0, column = 4, columnspan = 2)

    line = tk.Canvas(window_mode, width = 225, height = 4)
    line.grid(row = 1, column = 4, columnspan = 2)
    line.create_line((0,2,275, 2), fill = 'gray60')

    tk_etape_var = tk.BooleanVar(value = True)
    etape_1_checkbox = ctk.CTkRadioButton(window_mode, text = 'Étape 1', variable = tk_etape_var, value = True, radiobutton_width = 10, radiobutton_height = 10, border_width_checked = 4, border_width_unchecked = 2, border_color = ('gray10', 'gray40'), fg_color = ('gray10', 'gray20'), hover_color = 'gray32', text_color = 'black')
    etape_1_checkbox.grid(row = 2, column = 4, pady = 10, sticky = 'E', padx = 4)

    etape_2_checkbox = ctk.CTkRadioButton(window_mode, text = 'Étape 2', variable = tk_etape_var, value = False, radiobutton_width = 10, radiobutton_height = 10, border_width_checked = 4, border_width_unchecked = 2, border_color = ('gray10', 'gray40'), fg_color = ('gray10', 'gray20'), hover_color = 'gray32', text_color = 'black')
    etape_2_checkbox.grid(row = 2, column = 5, pady = 10, padx = 4, sticky = 'E')

    stat_var_int = tk.IntVar()
    mode_stat_checkbox = tk.Checkbutton(window_mode, text = 'Fichier pour analyses statistiques', var = stat_var_int)
    mode_stat_checkbox.grid(row = 3, column = 4, columnspan = 2, pady = 10)
    
    ######################################## GRAPH MODE ########################################

    graph_mode_int = tk.IntVar()
    boutton_graph_mode = tk.Checkbutton(window_mode, text = 'Afficher graphiques', var = graph_mode_int)
    boutton_graph_mode.grid(column = 4, row = 4, columnspan = 2) 

    # ligne2 = tk.Canvas(window_mode, width = 890, height = 4)
    # ligne2.grid(row = 7, column = 0, columnspan = 6)
    # ligne2.create_line((0,2,890,2), fill = 'gray60')

    browse_folder_label = tk.Label(window_mode, text = 'Dossier des fichiers PDF')
    browse_folder_label.grid(row = 8, column = 3, sticky = 'E')
    browse_folder_entry = ttk.Entry(window_mode)
    browse_folder_entry.grid(row = 8, column = 4, padx = 10)
    try : 
        browse_folder_entry.insert(0, folder_path)
    except NameError :
        browse_folder_entry.insert(0, 'Dossier')
    give_binds(browse_folder_entry, 'Dossier')
    browse_folder_button = ttk.Button(window_mode, text = 'Naviguer', command = Browse_folder)
    browse_folder_button.grid(row = 8, column = 5, padx = 10, sticky = 'W')

    # browse_input_label = tk.Label(window_mode, text = 'Fichier csv de la liste des participants')
    # browse_input_label.grid(row = 8, column = 3, sticky = 'E')
    # browse_input_entry = ttk.Entry(window_mode)
    # browse_input_entry.grid(row = 8, column = 4, padx = 10)
    # browse_input_entry.insert(0, 'Liste des participants')
    # browse_input_entry.bind('<FocusIn>', lambda event : on_entry_click(event, browse_input_entry, 'Liste des participants'))
    # browse_input_entry.bind('<FocusOut')
    # browse_input_button = ttk.Button(window_mode, text = 'Naviguer', command = Browse_input)
    # browse_input_button.grid(row = 8, column = 5, padx = 10, sticky = 'W')

    # liste_part_attention = tk.Label(window_mode, text = '''Attention \nIl est fortement recommandé d'utiliser le fichier de participants fournis. Les colonnes appropriées doivent se trouver dans le fichier sélectionné''')
    # liste_part_attention.grid(row = 9, column = 0, columnspan = 6)

    window_mode.protocol("WM_DELETE_WINDOW", lambda : [ive_had_enough(), window_mode.destroy()])

    window_mode.mainloop()

# def window_progression(numero_part) :
#     global progress_var, progressbar, window_prog, rendu
#     window_prog = tk.Toplevel(window_mode)
#     window_prog.title('VFC eco - Détection des pics R : progression')
#     window_prog.geometry('200x120+100+100')

#     icone = ImageTk.PhotoImage(file = "C:\\Users\\remyp\\VFC eco logo partial.png")
#     window_prog.iconphoto(False, icone)
#     window_prog.icone = icone

#     progress_label = tk.Label(window_prog, text = f'Participant {numero_part}')
#     progress_label.pack(pady = 5)

#     rendu = tk.StringVar()
#     rendu_label = tk.Label(window_prog, textvariable = rendu)
#     rendu_label.pack(pady = 5)

#     progress_var = tk.IntVar()
#     progressbar = ttk.Progressbar(window_prog, orient = 'horizontal', length = 500, mode = 'determinate', variable = progress_var)
#     progressbar.pack(pady = 5, padx = 10)
#     progress_var.set(0)
#     threading.Thread(target = etape_1).start()

#     window_prog.protocol('WM_DELETE_WINDOW', window_mode.destroy())

#     window_prog.mainloop()

def Confirmer_nom():
    global sujet_nom
    if not sujet_nom_prompt.get() == 'Nom du participant':
        sujet_nom = sujet_nom_prompt.get()

def Confirmer_num_part():
    global numero_part
    if not numero_part_prompt.get() == 'Numéro du participant':
       numero_part = numero_part_prompt.get()

def Confirmer_nom_pdf():
    global nom_pdf, path_pdf
    nom_pdf = nom_pdf_prompt.get()
    if not nom_pdf[-4:] == '.pdf' :
        nom_pdf = nom_pdf +'.pdf'
    try :
        path_pdf = f'{folder_path}\\{nom_pdf}'
    except NameError :
        pass
    if not os.path.exists(nom_pdf) :
        # si on trouve pas le pdf
        try :
            # on regarde si on trouve le path
            if not os.path.exists(path_pdf) :
                summon_err_window('''Le fichier PDF fournis ne semble pas exister à l'endroit spécifié. \nSi aucun dossier n'a été spéficié pour les PDF, spécifiez-le et réessayez''')
                raise Arrete_de_conf()       
            # si ya pas de path  
        except NameError :
            summon_err_window('''Le fichier PDF fournis ne semble pas exister à l'endroit spécifié. \nSi aucun dossier n'a été spéficié pour les PDF, spécifiez-le et réessayez''')
            raise Arrete_de_conf()

def Browse() :
    global path_pdf, folder_path, nom_pdf
    path_pdf = filedialog.askopenfilenames(initialdir = '/', title = 'Sélectionner le fichier PDF', filetypes = (('Fichiers PDF', '*.pdf'),))[0]
    try :
        folder_path, nom_pdf = os.path.split(path_pdf)
        nom_pdf_prompt.delete(0, tk.END)
        nom_pdf_prompt.insert(0, nom_pdf)
        browse_folder_entry.insert(0, folder_path)        

    except IndexError :
        path_pdf = False
        print('path pdf index error')
        pass

def Browse_folder() :
    global folder_path, browse_folder_entry, image_folder
    
    full_path = filedialog.askdirectory(initialdir = '/', title = 'Sélectionner le dossier des fichiers PDF')
    browse_folder_entry.delete(0, tk.END)
    browse_folder_entry.insert(0, full_path)

    if full_path.split('/')[-1][:9] == 'Documents' :
        folder_path, image_folder = os.path.split(full_path)
        print(folder_path, image_folder)
    else :
        folder_path = full_path

# def Browse_input() :
#     global fichier_input, browse_input_entry
#     fichier_input = filedialog.askopenfilenames(initialdir = '/', title = '''Sélectionner le fichier d'information sur les participants''', filetypes = (('Fichiers csv', '*.csv'),))[0]
#     browse_input_entry.delete(0, tk.END)
#     browse_input_entry.insert(0, fichier_input.split('/')[-1])

def Confirmer_nbp():
    global nombre_de_pages, page_pour_preview
    if not nombre_de_pages_prompt.get() == 'Pages' :
        nombre_de_pages = nombre_de_pages_prompt.get()

    if nombre_de_pages[0] == '0' or nombre_de_pages[0] == '-' :
        summon_err_window('Veuillez choisir des pages strictement positives.')
        raise Arrete_de_conf()

    print('nbp', nombre_de_pages)

    page_pour_preview = nombre_de_pages

    # Obtenir la premiere page a partir du input
    if ',' in page_pour_preview :
        page_pour_preview = nombre_de_pages.split(',')[0]
    
    if '-' in page_pour_preview :
        page_pour_preview = page_pour_preview.split('-')[0]
    
    if '!' in page_pour_preview :
        page_pour_preview = page_pour_preview.split('!')[1]

    print('page preview', page_pour_preview)

def Confirmer_hauteur():
    global hauteur
    hauteur = 1290 - int(hauteur_spinbox.get())

def Confirmer_nbs():
    global nbs
    nbs = int(nbs_prompt.get())
    if nbs <= 0 :
        summon_err_window('Veuillez choisir un nombre de sections strictement positif.')
        raise Arrete_de_conf()

def extraire_submap(pixelmap, x_gauche, x_droite, y_haut, y_bas) :
    array = np.frombuffer(pixelmap.samples, dtype = np.uint8)
    array = array.reshape((pixelmap.height, pixelmap.width, pixelmap.n))

    cropped_array = array[y_haut:y_bas, x_gauche:x_droite]

    page_cropped = Image.frombytes('RGB', (x_droite-x_gauche, y_bas-y_haut), cropped_array.tobytes())

    return page_cropped

def creer_images() :
    global appercu_pos, y_haut, page_pour_preview, images_a_clean
    images_a_clean = True
    try :
        doc_PDF = fitz.open(path_pdf)  
    except NameError :
        doc_PDF = fitz.open(nom_pdf)

    text_numpage.set(f'page {page_pour_preview}')

    page_pour_preview = int(page_pour_preview) - 1

    if page_pour_preview > len(doc_PDF) :
        try :
            summon_err_window(f'''Le document {nom_pdf} n'a pas {page_pour_preview+1} pages. Veuillez choisir un autre document ou une autre page.''')
        except NameError :
            summon_err_window(f'''Le document PDF sélectionné n'a pas {page_pour_preview+1} pages. Veuillez choisir un autre document ou une autre page.''')

    for i in range(1, 14) :
        nom_fichier_image_appercu = f'{folder_path}\\{sujet_nom}_#{numero_part}_preview{i}.png'
        try :
            page = doc_PDF.load_page(page_pour_preview)
        except ValueError : 
            pass
        pixelmap_de_la_page = page.get_pixmap(matrix = fitz.Matrix(2000 / page.rect.width, 1500 / page.rect.height))
        x_gauche = 104 + 128*(i-1)
        x_droite = 360 + 128*(i-1)
        y_haut = 625
        y_bas = 881

        image_appercu = extraire_submap(pixelmap_de_la_page, x_gauche, x_droite, y_haut, y_bas)
        image_appercu.save(nom_fichier_image_appercu)
    appercu_pos = 1

def afficher_images() :
    global appercu_pos, tk_image_affichee
    image_affichee = Image.open(f'{folder_path}\\{sujet_nom}_#{numero_part}_preview{appercu_pos}.png')
    image_affichee = image_affichee.resize((256, 256))
    tk_image_affichee = ImageTk.PhotoImage(image_affichee)
    appercu.create_image(128, 128, image = tk_image_affichee)

def move_right() :
    global appercu_pos
    appercu_pos += 1
    if appercu_pos == 14 :
        appercu_pos = 13
    afficher_images()
    dessiner_appercu()

def move_left() :
    global appercu_pos
    appercu_pos -= 1
    if appercu_pos == 0 :
        appercu_pos = 1
    afficher_images()
    dessiner_appercu()

def dessiner_appercu() :
    global ligne_appercu
    print('jessaie gee')
    print(hauteur)
    appercu.delete(ligne_appercu)
    hauteur_appercu = int(hauteur)/1.8-y_haut
    ligne_appercu = appercu.create_line((0, hauteur_appercu, 256, hauteur_appercu))

def graph_mode_() :
    global graph_mode
    if graph_mode_int.get() == 1 :
        graph_mode = True
    elif graph_mode_int.get() == 0 :
        graph_mode = False 

class Arrete_de_conf(Exception) :
    pass

def confirmer_tout() :
    global on_va_faire_etape1
    
    if etape_var :
        on_va_faire_etape1 = True
        try :
            Confirmer_nom_pdf()
            Confirmer_nbp()
        except Arrete_de_conf :
            return None
    try :
        Confirmer_nbs()
    except Arrete_de_conf :
        return None
    if images_a_clean :
        cleanup_apres_apercu()
    if speed == 'vitesse normale' :
        mettre_top_verif()
    Confirmer_hauteur()
    Confirmer_num_part()
    Confirmer_nom()
    ive_had_enough()
    window1.destroy()
    if etape_var :
        etape_1_prog()
    else :
        get_sujet_nom_num()
        demander_sections()
    # window_progression(numero_part)

def ive_had_enough() :
    global ive_had_enough_var
    ive_had_enough_var = True
    print('ive had enough')

def arranger_nbp() :
    if nombre_de_pages == 'Toutes' or nombre_de_pages == 'All' or nombre_de_pages == 'toutes' or nombre_de_pages == 'all' :
        nombre_de_pages_liste_paires.append([1,len(doc_PDF)])

    elif '-' in nombre_de_pages :
        premiere_pag, derniere_pag = map(int, nombre_de_pages.split('-'))
        nombre_de_pages_liste_paires.append([premiere_pag, derniere_pag])

    elif '!' in nombre_de_pages :
        nombpage = int(nombre_de_pages[1:])
        nombre_de_pages_liste_paires.append([nombpage, nombpage])
    
    else :
        nombre_de_pages_liste_paires.append([1, int(nombre_de_pages)])
    print(nombre_de_pages_liste_paires)

def draw_lines_and_find_highest(image_name, current_coords) :
    # Importer l'image
    try :
        imname = f'{folder_path}\\{image_folder}\\{image_name}_resultat.png'
    except NameError :
        imname = f'{image_name}_resultat.png'
    if os.path.exists(imname) :
        image = cv2.imread(imname)
    else :
        image = cv2.imread(f'{folder_path}\\{image_folder}\\{image_name}.png')
    
    while True :
        # Préparer les current coordonnées
        current_x = current_coords[1]
        current_y = current_coords[0]

        # Initier la liste
        couleurs_coordonnees = []

        # Remplir la liste
        for x in range(current_x-2  , current_x+4) :
            for y in range(current_y - 20, current_y+1) :
                blue = image[y,x,0] #####
                red = image[y,x,2]
                couleurs_coordonnees.append([y, x, blue, red])

        #trouver le prochain pixel    
        filtered_couleurs_coordonnees = [couleur_coordonnee for couleur_coordonnee in couleurs_coordonnees if couleur_coordonnee[2] < 150 and couleur_coordonnee[3] < 150]

        if filtered_couleurs_coordonnees :
            prochain_pixel = max(filtered_couleurs_coordonnees, key = lambda x : (-x[0], -x[1]))
        else :
            print('Erreur : la liste de filtered couleurs coordonnées est vide')
        
        if current_coords[0] < 800 :
            image[current_coords[0]-30:current_coords[0]+30, current_coords[1]-2:current_coords[1]+3] = [255, 0, 0]
            image[current_coords[0]-2:current_coords[0]+3, current_coords[1]-30:current_coords[1]+30] = [255, 0, 0]
            cv2.imwrite(imname, image)
            print(f"Je pense avoir détecté quelque chose qui n'est pas un pic R à {(current_coords[1] - debut)*10/(fin-debut) + (page-1) * 10} secondes")
            R_peaks_in_pixels.append(current_coords[1])
            artefact_list.append(current_coords[1])
            break

        #si on bouge plus, faire un + et break
        if prochain_pixel[0] == current_coords[0] :
            #check autour
            top_vérif = []
            filtered_top_vérif = []
            if verifier_top :
                rayon_de_vérif = [current_x-10, current_x-1, current_x+10]
                for x in rayon_de_vérif :
                    if not x == current_x-1 :
                        for y in range(current_y, current_y+40, 5) :
                            blue = image[y,x,0]
                            red = image[y,x,2]
                            top_vérif.append([y, x, blue, red])
                            image[y,x] = [255,0,0]
                        cv2.imwrite(imname, image)
                        print('je dessine le top verif')
                    else : 
                        for y in range(current_y-6, current_y,3) :
                            blue = image[y,x,0]
                            red = image[y,x,2]
                            top_vérif.append([y, x, blue, red])
                            image[y,x] = [255,0,0]
                        cv2.imwrite(imname, image)
                filtered_top_vérif = [pixel for pixel in top_vérif if pixel[2] < 150 and pixel[3] < 150]
            # Si aucun des pixels vérifiés n'est noir, c'est bon, on append
            if filtered_top_vérif == [] :
                image[current_coords[0]-30:current_coords[0]+30, current_coords[1]-2:current_coords[1]+3] = [0, 255, 0]
                image[current_coords[0]-2:current_coords[0]+3, current_coords[1]-30:current_coords[1]+30] = [0, 255, 0]
                R_peaks_in_pixels.append(current_coords[1])
                cv2.imwrite(imname, image) 
                break
            else :
                image[current_coords[0]-30:current_coords[0]+30, current_coords[1]-2:current_coords[1]+3] = [255, 0, 0]
                image[current_coords[0]-2:current_coords[0]+3, current_coords[1]-30:current_coords[1]+30] = [255, 0, 0]
                cv2.imwrite(imname, image)
                print(f"Je pense avoir détecté quelque chose qui n'est pas un pic R à {(current_coords[1] - debut)*10/(fin-debut) + (page-1) * 10} secondes")
                R_peaks_in_pixels.append(current_coords[1])
                artefact_list.append(current_coords[1])
                break
        else :
            # Dessiner le prochain pixel en vert et s'y déplacer
            image[prochain_pixel[0], prochain_pixel[1]-4:prochain_pixel[1]+4] = [0,255,0]
            current_coords = [prochain_pixel[0], prochain_pixel[1]]

def etape_1_prog() :
    global window_progression
    window_progression = make_window('VFC eco - Détection des pics R', '325x80+100+100')
    
    if speed == 'rapide' :
        text = '''Détection des pics R. \nCe processus peut prendre environ 1 seconde par page.'''
    elif verifier_top :
        text = 'Détection des pics R en cours. \nCe processus peut prendre environ 10 secondes par page analysée. \nIl est normal que cette page ne réponde pas. \nElle peut être fermée de force pour arrêter le processus.'
    else :
        text = 'Détection des pics R en cours. \nCe processus peut prendre environ 4 secondes par page analysée. \nIl est normal que cette page ne réponde pas. \nElle peut être fermée de force pour arrêter le processus.'

    progression_label = tk.Label(window_progression, text = text)
    progression_label.pack()

    window_progression.update_idletasks()

    window_progression.after(0, etape_1())

    window_progression.protocol('WM_DELETE_WINDOW', window_mode.destroy)

    window_progression.mainloop()

def etape_1() :
    global artefact_list, R_peaks_in_pixels, mode, speed, debut, fin, page, nombre_de_pages_liste_paires, nombre_de_pages, doc_PDF, total_times, RR_en_ms, sujet_nom_num, debut, fin, hauteur, image_folder
    ####################################
    ########### Lire le PDF ############
    ####################################

    ######################################## EXTRAIRE LES PAGES À LIRE DU INPUT ########################################
    try :
        # try :
        try :
            if path_pdf :
                doc_PDF = fitz.open(path_pdf)
            else :
                doc_PDF = fitz.open(nom_pdf)

        except NameError :
            doc_PDF = fitz.open(nom_pdf)

        width, height = 3600, 2700

        nombre_de_pages = nombre_de_pages.replace(' ', '')

        nombre_de_pages_liste_paires = []

        if ',' in nombre_de_pages :
            nombre_de_pages_splitted = nombre_de_pages.split(',')
            for i in range(len(nombre_de_pages_splitted)) :
                nombre_de_pages = nombre_de_pages_splitted[i]
                arranger_nbp()
        else :
            arranger_nbp()

        ######################################## EXTRAIRE LES PAGES DU PDF ########################################
        
        image_folder = f'Documents pour {sujet_nom} # {numero_part}'
        
        numero = 1

        imfolpath = f'{folder_path}\\{image_folder}'
        if os.path.exists(imfolpath) :
            imfolpath_ok = f'{imfolpath} ({numero})'
            while os.path.exists(imfolpath_ok) :
                numero += 1
                imfolpath_ok = f'{imfolpath} ({numero})'
            image_folder = f'{image_folder} ({numero})'
        else :
            imfolpath_ok = imfolpath

        os.mkdir(imfolpath_ok)

        nb_tot_pages = 0
        # rendu_string = 'Lecture des pages'
        # window_prog.after(0, rendu.set, rendu_string)

        for paire in nombre_de_pages_liste_paires :
            premiere_page = paire[0]
            derniere_page = paire[1]
            nombre_de_pages = range(premiere_page, derniere_page+1)
            for num_de_page_PDF in nombre_de_pages :
                nb_tot_pages += 1
                nom_fichier_photo = f'{folder_path}\\{image_folder}\\{sujet_nom}_#{numero_part}_page_{num_de_page_PDF:03}.png'
                page = doc_PDF.load_page(num_de_page_PDF-1)
                pixelmap_de_la_page = page.get_pixmap(matrix = fitz.Matrix(width / page.rect.width, height / page.rect.height))
                pixelmap_de_la_page.save(nom_fichier_photo)
                print(nom_fichier_photo)
            # rendu_string += '.'
            # rendu.set(rendu_string)

        # progressbar.config(maximum = nb_tot_pages)

        ######################################## TROUVER LES PICS R ########################################

        RR_en_pixels = []
        total_times = []
        artefact_list = []
        artefact_print_list = []

        # S'arranger de prendre les bonnes pages

        pages_faites = 0
        # rendu.set('Détection des pics R')

        for paire in nombre_de_pages_liste_paires :
            premiere_page = paire[0]
            derniere_page = paire[1]
            nombre_de_pages = range(premiere_page, derniere_page+1)
            
            # Supprimer le output si il y en a déjà un et 
            for page in  nombre_de_pages :
                deb = time.time()
                try :
                    nom_de_fichier_à_supprimer = f'{folder_path}\\{image_folder}\\{sujet_nom}_#{numero_part}_page_{page:03}_resultat.png'
                except NameError :
                    nom_de_fichier_à_supprimer = f'{sujet_nom}_#{numero_part}_page_{page:03}_resultat.png'
                if os.path.exists(nom_de_fichier_à_supprimer) :
                    os.remove(nom_de_fichier_à_supprimer)
                    print(f"J'ai supprimé le fichier {nom_de_fichier_à_supprimer}")
                else :
                    print(f"Je n'ai pas trouvé de fichier appelé {nom_de_fichier_à_supprimer}")

                # Détecter les points qui sont potentiellement des pics R

                image_name = f'{sujet_nom}_#{numero_part}_page_{page:03}'
                image = cv2.imread(f'{folder_path}\\{image_folder}\\{image_name}.png')
                R_peaks_in_pixels = []
                condition1 = image[hauteur, :, 2] <150
                condition2 = image[hauteur, :, 0] <150
                pixels_détectés_à_lancienne = np.where(condition1 & condition2)[0] 
                pixels_détectés_à_lancienne_dans_la_page = pixels_détectés_à_lancienne[(pixels_détectés_à_lancienne > debut) & (pixels_détectés_à_lancienne < fin-3)]

                pixels_détectés_à_lancienne_filtrés = []
                previous_value = None

                for value in pixels_détectés_à_lancienne_dans_la_page :
                    try :
                        if (value - previous_value) >= (fin-debut)/6 :
                            # Faire en sorte de baisser la hauteur entre deux pics R irréalistement distancés
                            condition1 = np.where(image[hauteur+150, previous_value:value, 2] <150)[0]
                            condition2 = np.where(image[hauteur+150, previous_value:value, 0] <150)[0]
                            pixels_plus_bas = np.where(condition1 & condition2)[0]
                            pixels_plus_bas_liste = pixels_plus_bas.tolist()
                            pixels_détectés_à_lancienne_filtrés.extend(pixels_plus_bas_liste)
                    except :
                        pass

                    if previous_value is None or (value - previous_value) >= 64 :
                        pixels_détectés_à_lancienne_filtrés.append(value)
                        previous_value = value


                if speed == 'vitesse normale' :
                    # À partir des pixels appartenant potentiellement à des pics R, regarder le pic au complet pour voir si c'est vraiment un pic R
                    for pixel_détecté_à_lancienne_de_la_liste in pixels_détectés_à_lancienne_filtrés : 
                        current_coords = [hauteur, pixel_détecté_à_lancienne_de_la_liste]
                        start = time.time()
                        draw_lines_and_find_highest(image_name, current_coords)
                        end = time.time()
                        print(f'ca a pris {end - start} secondes')
                else :
                    for pixel in pixels_détectés_à_lancienne_filtrés :
                        image[:, pixel-1:pixel+1] = [0, 255, 0]## mettre des lignes verticales
                    R_peaks_in_pixels.extend(pixels_détectés_à_lancienne_filtrés)
                    try :
                        imname = f'{folder_path}\\{image_folder}\\{image_name}_resultat.png'
                    except NameError :
                        imname = f'{image_name}_resultat.png'
                    cv2.imwrite(imname, image)

                os.remove(f'{folder_path}\\{image_folder}\\{image_name}.png')

                if len(R_peaks_in_pixels) == 0 :
                    summon_err_window(f'''Aucun pic R n'a été trouvé à la page {page}. Pensez à diminuer la hauteur et lancer l'analyse de nouveau.''')
                    window_progression.destroy()
                    window_mode.deiconify()
                    return None

                if not page == premiere_page :
                    try :
                        RR_en_pixels[-1] += R_peaks_in_pixels[0]-debut
                    except IndexError :
                        print(f'jai foire a la page {page}')

                # Mettre des tags 'Erreur?' dans le csv, là où on dirait une erreur

                for i in range(len(R_peaks_in_pixels)-1) :
                    if R_peaks_in_pixels[i] in artefact_list :
                        while len(RR_en_pixels) > len(artefact_print_list):
                            artefact_print_list.append('')
                        artefact_print_list.append('Erreur?')

                    # Mettre les valeurs dans les listes à imprimer au csv

                    RR_en_pixels.append(R_peaks_in_pixels[i+1]-R_peaks_in_pixels[i])
                    # total time : temps entre le début et le moment ou le RR commence
                    total_times.append((R_peaks_in_pixels[i] - debut)*10/(fin-debut) + (page-1) * 10)

                # Tranformer R en RR

                if not page == derniere_page :
                    RR_en_pixels.append(fin - R_peaks_in_pixels[-1])
                    total_times.append((R_peaks_in_pixels[-1] - debut)*10/(fin-debut) + (page-1) * 10)

                pages_faites += 1
                # progress_var.set(pages_faites)
                print(f'la page a pris {time.time()-deb} secondes')

        # Transformer RR en pixel à RR en ms

        RR_en_ms = [RR * (10000/(fin-debut)) for RR in RR_en_pixels]


        while len(RR_en_pixels) > len(artefact_print_list) :
            artefact_print_list.append('')
            
        ######################################## CRÉER LE CSV AVEC LES RR ########################################

        sujet_nom_num = f'{sujet_nom}_#{numero_part}'
        # Write the CSV file
        while True :
            try :
                try :
                    filename = f'{folder_path}\\{image_folder}\\{sujet_nom_num}_RR.csv'
                except NameError :
                    filename = f'{sujet_nom_num}_RR.csv'
                with open(filename, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['''Temps depuis le début de l'enregistrement (s)''', 'RR (ms)', '''Erreur possible'''])
                    for (total_time, unRR_en_ms, instance_artefact) in zip(total_times, RR_en_ms, artefact_print_list):
                        writer.writerow([total_time,unRR_en_ms, instance_artefact])  
                break
            except PermissionError :
                summon_err_window('Une erreur est survenue, veuillez fermer les fichiers csv de résultats et fermer cette fenêtre.')
                continue
    except Exception as e :
        summon_err_window(f'''Une erreur de type « {e} » est survenue, veuillez réessayer. \nCertains messages d'erreur sont intuitifs à corriger, vous pouvez alors corriger l'erreur.''')
        window_progression.destroy()
        window_mode.deiconify()
    window_progression.destroy()
    window2_func()


    # except Exception as e :
    #     summon_err_window(f'''Une erreur de type « {e} » est survenue, veuillez réessayer. \nCertains messages d'erreur sont intuitifs à corriger, vous pouvez alors corriger l'erreur.''')
    #     window_mode.destroy()

def get_sujet_nom_num() :
    global sujet_nom_num
    if sujet_nom_num == '' :
        sujet_nom_num = f'{sujet_nom}_#{numero_part}'

def etape_2() :
    global numero_part, sujet_nom_num, section_values
    ######################################## METTRE DES ZÉROS AUX POINTS SUPPRIMÉS POUR LES MATHS AVEC DIFF ########################################
    encodings = ['utf-8', 'utf-8-sig', 'ISO-8859-1', 'Windows-1252']

    print('je commence etape 2')

    for enc in encodings:
        try:
            df_corrige = pd.read_csv(f'{folder_path}\\{image_folder}\\{sujet_nom_num}_RR Corrigé.csv', index_col = False, encoding = enc)
        except (UnicodeDecodeError, NameError, FileNotFoundError) as e :
            if isinstance(e, FileNotFoundError) :
                summon_err_window(f'''Aucun fichier appelé « {sujet_nom_num}_RR Corrigé.csv » n'a été trouvé. Si aucun artéfact n'est trouvé, copiez et collez le fichier « {sujet_nom_num}_RR.csv » et ajoutez au nom  «  Corrigé » Cela sert à ne pas accidentellement utiliser les RR non-corrigés. \nRelancez ensuite le programme en utilisant l'option \n« Étape 2 » ''')    
                window_mode.destroy()
                return None
            try :
                df_corrige = pd.read_csv(f'{sujet_nom_num}_RR Corrigé.csv', index_col = False, encoding = enc)
            except (UnicodeDecodeError, FileNotFoundError) as e :
                if isinstance(e, FileNotFoundError) and enc == encodings[-1] :
                    summon_err_window(f'''Aucun fichier appelé « {sujet_nom_num}_RR Corrigé.csv » n'a été trouvé. \nSi aucun artéfact n'est trouvé, copiez et collez le fichier « {sujet_nom_num}_RR.csv » dans File Explorer et ajoutez au nom  «  Corrigé » \nCela sert à ne pas accidentellement utiliser les RR non-corrigés. \nRelancez ensuite le programme en utilisant l'option \n« Étape 2 » ''')    
                    window_mode.destroy()
                    return None
    ######################################## CALCUL DE LA VFC ########################################

    deja_montre = False

    filename_result = f'{folder_path}/Résultats VFC.csv'
    filename_stat = f'{folder_path}\\Résultats VFC stat.csv'

    # Faire les calculs pour chaque section
    for groupe_colonne in range(nbs) :
        lower_bound = int(section_values[groupe_colonne*2])
        upper_bound = int(section_values[groupe_colonne*2+1])
        filtered_df = df_corrige[(df_corrige['''Temps depuis le début de l'enregistrement (s)'''] > lower_bound) & (df_corrige['''Temps depuis le début de l'enregistrement (s)'''] < upper_bound)] 

        # Mean HR
        mean_HR = 60000/np.mean(filtered_df['RR (ms)'])

        # Interpolate using Cubic Spline
        x = filtered_df['''Temps depuis le début de l'enregistrement (s)''']
        y = filtered_df['RR (ms)']
        if len(x) == 0 :
            summon_err_window('Veuillez vérifier les valeurs de sections données. Il semble y avoir aucun RR dans une des sections.')
            demander_sections()
            return None

        try :
            cs = CubicSpline(x, y)
        except ValueError :
            summon_err_window(f'''Il semble y avoir moins de 2 éléments dans la liste des RR (tirée du document {sujet_nom_num}_RR Corrigé.csv), veuillez réessayer avec plus de pics RR.''')            
            return None
        
        # Interpoler de la première à la dernière valeur de total time de la section, par bonds de 0.1 sec
        x_interp = np.arange(x.iloc[0], x.iloc[-1], 0.1)
        y_interp = cs(x_interp)
        
        average = np.mean(y)

        y_interp = y_interp-average

        # Faire la FFT
        fft_result = np.fft.fft(y_interp)
        fft_magnitude = np.abs(fft_result)

        n = len(y_interp)
        sampling_frequency = 1 / (x_interp[1] - x_interp[0])
        frequencies = np.fft.fftfreq(n, d=1/sampling_frequency)

        magnitude_squared = fft_magnitude**2
        PSD = (1/(n*sampling_frequency)) * magnitude_squared

        # On veut juste la partie positive
        frequencies_positive = frequencies[:n//2]
        fft_magnitude_positive = fft_magnitude[:n//2]
        PSD_positive = PSD[:n//2]


        # Sélectionner les fréquences pour matcher la littérature hf lf etc
        LFmask = np.logical_and(frequencies_positive > 0.04 , frequencies_positive < 0.15) 

        LF = frequencies_positive[LFmask]
        PSD_LF = PSD_positive[LFmask]


        HFmask = np.logical_and(frequencies_positive > 0.15, frequencies_positive < 0.4)

        HF = frequencies_positive[HFmask]
        PSD_HF = PSD_positive[HFmask]


        # Intégrer pour avoir les HF et LF
        LFintegral = np.trapezoid(PSD_LF, LF)
        HFintegral = np.trapezoid(PSD_HF, HF)
        FRatio = LFintegral/HFintegral

        ######################################## TIME DOMAIN ########################################

        # sdrr
        sdrr = filtered_df['RR (ms)'].std()

        # pRR40
        diff = np.abs(filtered_df['RR (ms)'].diff())
        num_diff_50 = len(diff[(diff > 50) & (diff <= 600)])

        pRR50 = num_diff_50/(len(filtered_df))

        # Créer un array de diff 
        diff_values = filtered_df['RR (ms)'].diff()

        # Éliminer les diff de plus de 500 pour éliminer les zéros
        diff_values[diff_values > 500] = np.nan

        # RMSSD
        rmssd = np.sqrt(np.nanmean(diff_values**2))

        ######################################## METTRE LES RÉSULTATS DANS LE CSV ########################################

        if numero_part == 'X' :
            numero_part = 100

        parametres = [rmssd, pRR50, sdrr, LFintegral, HFintegral, FRatio, mean_HR]

        parametres_liste = ['RMSSD', 'pRR50', 'SDRR', 'LF', 'HF', 'LF/HF', 'FC'] 
        values = {parametres_liste[_] : parametre for _, parametre in enumerate(parametres)} 
        
        if graph_mode and not deja_montre :
            fig = plt.figure(figsize = (12,6))


            fig.canvas.manager.set_window_title('VFC eco - Graphiques')
            ax1 = plt.subplot2grid((1,3), (0,0), colspan = 2)
            ax2 = plt.subplot2grid((1,3), (0,2))

            # mettre des titres, ax2 c'est pour le fft

            y_plot = y_interp+average

            x = x.reset_index(drop = True)

            ax1.set_xlim((x[0],x[0]+40))
            ax1.scatter(x,y, color = 'r', label = 'Intervalles RR')
            ax1.plot(x_interp, y_plot, color = 'b', label = 'Données interpolées')
            ax1.set_title('Premières 40 secondes de la première section')
            ax1.set_ylabel('Intervalles RR (ms)')
            ax1.set_xlabel('''Temps depuis le début de l'enregistrement (s)''')
            ax1.legend()

            ax2.set_xlim(0,0.5)
            ax2.plot(frequencies_positive, PSD_positive)
            lines = [0.04, 0.15, 0.4]
            for line in lines :
                ax2.axvline(line, color = 'r', linestyle = '--')
            ax2.set_title('Transformée de Fourier des RR de la première section')
            ax2.set_xlabel('Fréquences (Hz)')
            ax2.tick_params(axis = 'y', which = 'both', left = False, right = False, labelleft = False)

            plt.show()
            deja_montre = True

        while True :
            try :
                rows = []
                print('rows :', rows)
                try :
                    filename_result = f'{folder_path}/Résultats VFC.csv'
                except NameError :
                    filename_result = 'Résultats VFC.csv'

                nbs_max = int(nbs)
                expand_header = False

                # creer le fichier si il existe pas deja et mettre un header
                if not os.path.exists(filename_result) :
                    csv_result_header = ['']
                    for sec in range(nbs_max) :
                        csv_result_header += [f'Section {sec+1}']*7
                    csv_result_header = [csv_result_header, ['Numéro du participant'] + parametres_liste*nbs_max]
                    with open(filename_result, mode = 'w', newline= '') as file :
                        writer = csv.writer(file)
                        writer.writerows(csv_result_header)

                for enc in encodings :
                    try :
                        df1 = pd.read_csv(filename_result, encoding = enc)
                        df2 = pd.read_csv(filename_stat, encoding = enc)
                        print(df1,len(df1), '\n', df2, len(df2))
                    except UnicodeDecodeError :
                        pass
                if len(df1) == 0 or len(df2) == 0 :
                    summon_err_window('''Une erreur est survenue. Veuillez recommencer l'étape 2''')
                    window_mode.deiconify()
                    return None

                with open(filename_result, mode='r', newline = '') as file:
                    reader = csv.reader(file)
                    for row in reader :
                        print(len(row))
                        if (len(row)-1)/7 > nbs_max :
                            nbs_max = int((len(row)-1)/7)
                            expand_header = True
                        print('''J'ajoute a rows :''', row)
                        rows.append(row)
                print(nbs_max)

                # si c'est la premiere section, mettre le numero du participant et les resultats de la premiere section 
                if groupe_colonne == 0 :
                    rows.append([numero_part] + [value[1] for value in values.items()])

                # si c'est pas la premiere section, ajouter a la ligne du participant les valeurs de cette section
                else : 
                    rows[-1] += [value[1] for value in values.items()] 

                try :
                    if groupe_colonne == nbs-1 :
                        rows[2:] = sorted(rows[2:], key = lambda x : int(x[0]))
                except ValueError :
                    del rows[:2]
                    print(rows)

                print('\n \nvoici les rows : \n \n', rows)

                with open(filename_result, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    if expand_header :
                        csv_result_header = ['']
                        for sec in range(nbs_max) :
                            csv_result_header += [f'Section {sec+1}']*7
                        csv_result_header = [csv_result_header, ['Numéro du participant'] + parametres_liste*nbs_max] 
                        writer.writerows(csv_result_header)
                        del rows[:2]
                        writer.writerows(rows)
                    else :
                        writer.writerows(rows)
                break
            except PermissionError :
                summon_err_window('Veuillez fermer le fichier de résultats, puis fermer cette fenêtre.')
                continue

        if stat_var :
            while True :
                try :
                    try :
                        filename_stat = f'{folder_path}\\Résultats VFC stat.csv'
                    except NameError:
                        filename_stat = 'Résultats VFC stat.csv'

                    # initier le fichier et mettre un header au besoin
                    if not os.path.exists(filename_stat) :
                        csv_header = ['Numéro du participant', 'Section', '''Ajouter des paramètres pertinents (p. ex.: sexe, traitement, l'ordre des traitements, etc.)''','Paramètre', 'Valeur']

                        with open(filename_stat, 'w', newline = '', encoding = 'utf-8-sig') as file_created :
                            writer = csv.writer(file_created)
                            writer.writerow(csv_header)

                    encodings = ['utf-8', 'utf-8-sig', 'ISO-8859-1', 'Windows-1252']
                    for enc in encodings:
                        try:
                            df_stat = pd.read_csv(filename_stat, encoding = enc)
                        except UnicodeDecodeError :
                            print(f'{enc} a pas marché')
                            pass

                    colnames = df_stat.columns.tolist()

                    colnames = [_ if not _[:7] == 'Unnamed' else '' for _ in colnames]

                    nb_cols_vides = len(colnames)-4

                    df_stat = df_stat.fillna('')

                    for parametre, valeur in values.items() :
                        df_stat.loc[len(df_stat)] = [numero_part, groupe_colonne+1] + ['']*nb_cols_vides + [parametre, valeur]

                    with open(filename_stat, 'w', newline = '') as filestat :
                        writer = csv.writer(filestat)
                        writer.writerow(colnames)
                        for ligne in df_stat.itertuples(index = False) :
                            writer.writerow(ligne)
                    break
                except PermissionError :
                    summon_err_window('Veuillez fermer le fichier de résultats (fichier pour statistiques), puis fermer cette fenêtre.')
                    continue

    window_fini = make_window('VFC eco - Confirmation', f'{len(filename_result)*8+230}x60+100+100')
    label_fini = ttk.Label(window_fini, text = f'Le processus est terminé. \nLes résultats se trouvent dans le document {filename_result}', justify = 'center')
    label_fini.pack()
    pas_fini_buttin = ttk.Button(window_fini, text = 'Prochain participant', command = lambda : [window_fini.destroy(), window_mode.deiconify()])
    pas_fini_buttin.pack()
    fini_fini_button = ttk.Button(window_fini, text = 'Fermer le logiciel', command = lambda : window_mode.destroy())
    fini_fini_button.pack()
    window_fini.protocol('WM_DELETE_WINDOW', lambda : [window_fini.destroy(), window_mode.destroy()])
    window_fini.mainloop()

def rr_correct() :
    global debut, fin, page_corr_spin, rs_ajout, rs_suppr, window_corr, corring, removing, page_a_corr, zoomed, undoin, num_act, rs_ajout, rs_suppr
    corring = True
    corrige = False
    try :
        window_mode.withdraw()
    except :
        try :
            window2.destroy()
        except :
            pass

    page_a_corr = None
    rs_ajout = []
    rs_suppr = []

    def create_im_corr() :
        global debut, fin, fichier_corr_path, page_corr_spin, im_corr, zoomed, x_marge, y_marge, fact, undoin, image, act_del, corrige, page_a_corr
        print(page_corr_spin.get())
        print('fichier corr etait', fichier_corr_path)
        print(fichier_corr_path[-12:])
        print(fichier_corr_path[-16:-13])

        if fichier_corr_path[-12:] == '_corrige.png' :
            corrige = True
        else :
            corrige = False

        page_a_corr = int(page_corr_spin.get())

        if not str(page_corr_spin.get()) == fichier_corr_path[-16:-13] and not corrige :
            if os.path.exists(f'{fichier_corr_path[:-16]}{page_a_corr:03}_resultat_corrige.png') :
                print('ca existe')
                fichier_corr_path = f'{fichier_corr_path[:-16]}{page_a_corr:03}_resultat_corrige.png'
            else : 
                fichier_corr_path = f'{fichier_corr_path[:-16]}{page_a_corr:03}_resultat.png'
                print('ca existe pas')
        elif not page_corr_spin.get() == fichier_corr_path[-24:-21] and corrige :
            if os.path.exists(f'{fichier_corr_path[:-24]}{page_a_corr:03}_resultat_corrige.png') :
                print('ca existe')
                fichier_corr_path = f'{fichier_corr_path[:-24]}{page_a_corr:03}_resultat_corrige.png'
            else : 
                fichier_corr_path = f'{fichier_corr_path[:-24]}{page_a_corr:03}_resultat.png'
                print('ca existe pas')

        else :
            print( 'le fichier etait correct', fichier_corr_path)

        print('cest devenu', fichier_corr_path)

        try :
            im_corr = Image.open(fichier_corr_path)
            image = cv2.imread(fichier_corr_path)
        except NameError :
            return None
        if undoin :
            print('je cherche', folder_path, act_del)
            im_corr = Image.open(f'{folder_path}\\Memoire{act_del}.png')
            image = cv2.imread(f'{folder_path}\\Memoire{act_del}.png')
            undoin = False

        if not zoomed :
            crop_im_corr = im_corr.crop((debut, 516, fin, 2442))
        else : 
            crop_im_corr = im_corr.crop((x_marge, y_marge, x_marge+1073*fact, y_marge+642*fact))

        crop_im_corr = crop_im_corr.resize((1073, 642), Image.LANCZOS)
        im_corr_aff = ImageTk.PhotoImage(crop_im_corr)
        canvas_corr.image = im_corr_aff
        canvas_corr.create_image(0,0, anchor = tk.NW, image = im_corr_aff)

    def Browse_corr() :
        global page_a_corr, page_corr_spin, fichier_corr_path, corrige, folder_path, image_folder
        try :
            indir = f'{folder_path}\\{image_folder}'
        except NameError :
            indir = '/'

        fichier_corr_path = filedialog.askopenfilenames(initialdir = indir, title = 'Sélectionnez la page à corriger', filetypes = (('Fichiers png', '*.png'),))[0]
        full_path, fichier_corr = os.path.split(fichier_corr_path)
        folder_path, image_folder = os.path.split(full_path)
        browse_corr_entry.delete(0, tk.END)
        browse_corr_entry.insert(0, fichier_corr)
        if not fichier_corr[-12:] == '_corrige.png' :
            page_a_corr = fichier_corr[-16:-13] 
            corrige = False
        else :
            page_a_corr = fichier_corr[-24:-21]
            corrige = True
        page_corr_spin.delete(0, tk.END)
        page_corr_spin.insert(0, page_a_corr)
        print(fichier_corr_path)

    def pluss(image, x, y, couleur) :
        image[y-2:y+3, x-30:x+30] = couleur
        image[y-30:y+30, x-2:x+3] = couleur
        print(x, y)

    def faire_plus(event) :
        global page_a_corr, rs_ajout, rs_suppr, fichier_corr_path, removing, debut, x_marge, y_marge, fact, image, num_act
        if not zoomed :
            x, y = event.x*3+debut, event.y*3+516
            print(debut)
        else :
            x, y = event.x*fact+x_marge, event.y*fact+y_marge

        print('jai save memoire', folder_path, num_act)
        cv2.imwrite(f'{folder_path}\\Memoire{num_act}.png', image)

        if removing :
            plus_x = []
            plus_y = []
            color = [66, 135, 245]
            for i in range(x-40, x+40) :
                brg = [image[y+6, i, coul] for coul in range(3)]
                if brg[2] == 0 and (brg[1] == 255 or brg[0] == 255) :
                    plus_x.append(i)
            for j in range(y-40, y+40) :
                brg = [image[j, x+6, coul] for coul in range(3)]
                if brg[2] == 0 and (brg[1] == 255 or brg[0] == 255) :
                    plus_y.append(j)
            try :
                x_centre = int(sum(plus_x)/len(plus_x))
                y_centre = int(sum(plus_y)/len(plus_y))
            except ZeroDivisionError :
                return None
            R_suppr = (int(page_a_corr)-1)*10+(x_centre-debut)*10/(fin-debut)
            rs_suppr.append(R_suppr)
            pluss(image, x_centre, y_centre, color)
            if not fichier_corr_path[-12:] == '_corrige.png' :
                cv2.imwrite(f'{fichier_corr_path[:-4]}_corrige.png', image)
                fichier_corr_path = f'{fichier_corr_path[:-4]}_corrige.png'
            else : 
                cv2.imwrite(fichier_corr_path, image)
            past_actions.append(('supprimer', x_centre, y_centre, num_act))
            create_im_corr()
        else :
            color = [0, 255, 0]
            R_ajout = (int(page_a_corr)-1)*10+(x-debut)*10/(fin-debut)
            rs_ajout.append(R_ajout)
            pluss(image, x, y, color)
            if not fichier_corr_path[-12:] == '_corrige.png' :
                cv2.imwrite(f'{fichier_corr_path[:-4]}_corrige.png', image)
                fichier_corr_path = f'{fichier_corr_path[:-4]}_corrige.png'
            else : 
                cv2.imwrite(fichier_corr_path, image)
            past_actions.append(('ajouter', x, y, num_act))
            create_im_corr()
        num_act += 1

    def removin() :
        global removing
        removing = True

    def addin() :
        global removing
        removing = False

    def undo() :
        global undoin, image, act_del
        last_action = past_actions[-1]

        if last_action[0] == 'ajouter' :
            rs_suppr.append((int(page_a_corr)-1)*10+(last_action[1]-debut)*10/(fin-debut))
        else :
            rs_ajout.append((int(page_a_corr)-1)*10+(last_action[1]-debut)*10/(fin-debut))
        undoin = True
        act_del = last_action[3]
        create_im_corr()

        del[past_actions[-1]]

    def zoomin(event) : 
        global im_corr, x_marge, y_marge, zoomed, fact
        if not zoomed :
            x_zoom, y_zoom = event.x*3+debut, event.y*3+516
        else :
            x_zoom, y_zoom = event.x*fact+x_marge, event.y*fact+y_marge

        def check_bord(coord_zoom, debut, fin, longueur_canvas, facteur) :
            '''Certains noms de variables sont applicables seulement en X mais cest pas grave'''
            # si c'est trop proche à gauche, on se colle sur la limite gauche
            if coord_zoom - debut < longueur_canvas*facteur/2 :
                left = debut
                right = debut+longueur_canvas*facteur
            # si c'est trop proche à droite, on se colle sur la limite à droite
            elif fin - coord_zoom < longueur_canvas*facteur/2 :
                left = fin-longueur_canvas*facteur
                right = fin
            # si c'est au milieu de l'image, on met se met là où le click a eu lieu
            else :
                left = coord_zoom - longueur_canvas*facteur/2
                right = coord_zoom + longueur_canvas*facteur/2
            # si on a zoom déjà et là on veut clicker un pixel impair, on va essayer d'afficher de X.5 pixels à Y.5 pixels... donc on arrondi ça à X+1 et Y+1
            if not int(left) == left :
                left += 0.5
                right += 0.5
            # si en ajustant pour pas zoom entre deux pixels on s'est mis à afficher en dehors du tracé ECG, on se tasse de 1 à gauche
            if right > fin :
                left -= 1
                right -=1
            return int(left), int(right)

        if not zoomed :
            fact = 2

        else :
            fact = 1

        left, right = check_bord(x_zoom, debut, fin, 1073, fact)
        up, down = check_bord(y_zoom, 516, 2442, 642, fact)

        print(left, right, up, down)

        crop_im_zoom = im_corr.crop((left, up, right, down))
        crop_im_zoom = crop_im_zoom.resize((1073, 642), Image.LANCZOS)
        im_corr_aff = ImageTk.PhotoImage(crop_im_zoom)
        canvas_corr.create_image(0,0, anchor = tk.NW, image = im_corr_aff)
        canvas_corr.image = im_corr_aff

        x_marge = left
        y_marge = up
        zoomed = True

        canvas_corr.bind('<Button-1>', faire_plus)

    def zoomout() :
        global zoomed, im_corr
        if zoomed :
            crop_im_corr = im_corr.crop((debut, 516, fin, 2442))
            crop_im_corr = crop_im_corr.resize((1073, 642), Image.LANCZOS)
            im_corr_aff = ImageTk.PhotoImage(crop_im_corr)
            canvas_corr.create_image(0,0, anchor = tk.NW, image = im_corr_aff)
            canvas_corr.image = im_corr_aff
            zoomed = False
        else :
            pass

    removing = False
    zoomed = False
    undoin = False
    past_actions = []

    num_act = 1


    window_corr = make_window('VFC eco - Correction des RR', '1100x705+70+5')

    canvas_corr = tk.Canvas(window_corr, width = 1073, height = 642)
    canvas_corr.grid(row = 0, column = 0, columnspan = 15, padx = 10, pady = 10)
    canvas_corr.bind('<Button-1>', faire_plus)

    page_corr_spin = tk.Spinbox(window_corr, from_ = 0, to = 999, command = create_im_corr)
    page_corr_spin.grid(row = 1, column = 14, sticky = 'W')
    page_corr_label = tk.Label(window_corr, text = 'Page à corriger')
    page_corr_label.grid(row = 1, column = 12, sticky = 'E')

    browse_corr_label = tk.Label(window_corr, text = 'Fichier à corriger (image)')
    browse_corr_label.grid(row = 1, column = 0, pady = 10, sticky = 'E')
    browse_corr_entry = tk.Entry(window_corr)
    browse_corr_entry.insert(0, 'Fichier à corriger')
    give_binds(browse_corr_entry, 'Fichier à corriger')
    browse_corr_entry.grid(row = 1, column = 1, pady = 10)
    browse_corr_button = ttk.Button(window_corr, text = 'Naviguer', command = lambda : [Browse_corr(), create_im_corr()])
    browse_corr_button.grid(row = 1, column = 2, pady = 10, sticky = 'W')

    retour_corr = ttk.Button(window_corr, text = 'Retour', command = lambda : [cleanup_apres_corr(), window_corr.destroy()])
    retour_corr.grid(row = 1, column = 3)

    zoomin_butt = ttk.Button(window_corr, text = 'Agrandir', command = lambda : canvas_corr.bind('<Button-1>', zoomin))
    zoomin_butt.grid(row = 1, column = 4, sticky = 'E')

    zoomout_butt = ttk.Button(window_corr, text = 'Réduire', command = zoomout)
    zoomout_butt.grid(row = 1, column = 5, sticky = 'W')

    undo_but = ttk.Button(window_corr, text = 'Annuler', command = undo)
    undo_but.grid(row = 1, column = 6, padx= 10)

    aj_but = ttk.Button(window_corr, text = 'Ajouter des R', command = addin)
    aj_but.grid(row = 1, column = 7, sticky = 'E')
    ret_but = ttk.Button(window_corr, text = 'Retirer des R', command = removin)
    ret_but.grid(row = 1, column = 8, sticky = 'W')

    window_corr.protocol('WM_DELETE_WINDOW', window_mode.destroy)

    window_corr.mainloop()

def cleanup_apres_corr() :
    global rs_ajout, rs_suppr 

    print('folder path \n \n', folder_path, image_folder)

    try :
        for i in range(100) :
            if os.path.exists(f'{folder_path}\\Memoire{i}.png') :
                os.remove(f'{folder_path}\\Memoire{i}.png')
    except NameError :
        print('pas de folder path, tas rien fait')
        if not win2 :
            window_mode.deiconify()
        return None

    if len(rs_ajout) + len(rs_suppr) == 0 :
        print('tas ouvert le fichier mais tas rien fait')
        window_mode.deiconify()
        return None

    rs_ajout_vrai = []

    rs_ajout = sorted(rs_ajout)

    print('rs suppr', rs_suppr, len(rs_suppr))
    print('rs ajout', rs_ajout)

    if not len(rs_suppr) == 0 :
            for R_ajoute in rs_ajout :
                ok = True
                for idx, R_suppr in enumerate(rs_suppr) :
                    if abs(R_ajoute - R_suppr) < 0.01 :
                        print(R_ajoute, R_suppr)
                        ok = False
                        del rs_suppr[idx]
                if ok :
                    rs_ajout_vrai.append(R_ajoute)
    else :
        rs_ajout_vrai = rs_ajout

    print('rs suppr apres cleanup',rs_suppr)
    print('rs ajout vrai', rs_ajout_vrai)

    sujet_nom_num = fichier_corr_path.split('/')[-1].split('_page')[0]

    try :
        print('a')
        if os.path.exists(f'{folder_path}\\{image_folder}\\{sujet_nom_num}_RR Corrigé.csv') :
            file = f'{folder_path}\\{image_folder}\\{sujet_nom_num}_RR Corrigé.csv'
        else :
            file = f'{folder_path}\\{image_folder}\\{sujet_nom_num}_RR.csv'
    except NameError :
        if os.path.exists(f'{sujet_nom_num}_RR Corrigé.csv') :
            file = f'{sujet_nom_num}_RR Corrigé.csv'
        else :
            file = f'{sujet_nom_num}_RR.csv'


    encodings = ['utf-8', 'utf-8-sig', 'ISO-8859-1', 'Windows-1252']
    for enc in encodings:
        try:
            df_rr = pd.read_csv(file, index_col = False, encoding = enc)
            break
        except (UnicodeDecodeError, FileNotFoundError) as e :
            if isinstance(e, FileNotFoundError) :
                summon_err_window(f'Veuillez spécifier le dossier contenant le fichier de RR ({sujet_nom_num}_RR.csv) à la page précédente')
                window_corr.destroy()
                window_mode.deiconify()
                # juste delete les corrigés quon a fait qui sont pas bons parce que pas de fichier RR
                for r in rs_ajout_vrai + rs_suppr :
                    page = r//10 + 1
                    try :
                        if os.path.exists(f'{folder_path}\\{sujet_nom_num}_page#{page:03}_resultat_corrige.png') :
                            os.remove(f'{folder_path}\\{sujet_nom_num}_page#{page:03}_resultat_corrige.png')
                    except NameError :
                        if os.path.exists(f'{sujet_nom_num}_page#{page:03}_resultat_corrige.png') :
                            os.remove(f'{sujet_nom_num}_page#{page:03}_resultat_corrige.png')
                break

    df_rr = df_rr.sort_values(by = '''Temps depuis le début de l'enregistrement (s)''').reset_index(drop = True)

    # supprimer du df
    print(rs_suppr)
    rs_suppr_rounded = [np.ceil(_*20)/20 for _ in rs_suppr]
    print(rs_suppr_rounded)
    df_rr['rounded'] = np.ceil(df_rr['''Temps depuis le début de l'enregistrement (s)''']*20)/20
    print(df_rr)
    df_r_a_suppr = df_rr['rounded'].isin(rs_suppr_rounded)
    print(df_r_a_suppr)


    indexes_a_suppr = df_r_a_suppr[df_r_a_suppr].index.tolist()

    for idx in indexes_a_suppr :
        if idx == 0 :
            df_rr = df_rr.drop(idx)
        else :
            i = idx-1
            temps_total = df_rr.loc[i, '''Temps depuis le début de l'enregistrement (s)''']
            rr = df_rr.loc[idx-1:idx, 'RR (ms)'].sum()
            df_rr.loc[idx-1] = {'''Temps depuis le début de l'enregistrement (s)''' : temps_total, 'RR (ms)' : rr}
            df_rr = df_rr.drop(idx)    
    print(df_rr)
    df_rr = df_rr.drop(['rounded'], axis = 1)
    print(df_rr)

    df_rr = df_rr.reset_index(drop = True)

    # ajouter au df
    for ajout in rs_ajout_vrai :
        position = df_rr[df_rr['''Temps depuis le début de l'enregistrement (s)'''] > ajout]
        # Si il y a rien de plus grand que l'ajout (on ajoute a la fin)
        if len(position) == 0 :
            temps_total = ajout
            rr = (temps_total - df_rr.loc[len(df_rr)-1, '''Temps depuis le début de l'enregistrement (s)'''])*1000
            df_rr.loc[len(df_rr)] = {'''Temps depuis le début de l'enregistrement (s)''' : temps_total, 'RR (ms)' : rr}
        else :
            p = position.index[0]
            temps_total = ajout
            rr1 = (temps_total - df_rr.loc[p-1, '''Temps depuis le début de l'enregistrement (s)''']) *1000
            rr2 = (df_rr.loc[p, '''Temps depuis le début de l'enregistrement (s)''']- temps_total)*1000

            df_a_concat = pd.DataFrame({'''Temps depuis le début de l'enregistrement (s)''' : [df_rr.loc[p-1, '''Temps depuis le début de l'enregistrement (s)'''], temps_total], 'RR (ms)' : [rr1, rr2]})

            df_rr = pd.concat([df_rr.iloc[:p-1], df_a_concat, df_rr.iloc[p:]]).reset_index(drop = True)

    try :
        df_rr = df_rr.drop('Erreur possible', axis = 1)
    except KeyError :
        pass
    print(df_rr)

    #df_rr.to_csv marche pas meme avec encoding utf 8 sig
    while True :
        try :
            print('trying')
            if not file[-11:] == 'Corrigé.csv' :
                filename = f'{file[:-4]} Corrigé.csv' 
            else :
                filename = file

            print('filename',filename)
            print(df_rr)

            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['''Temps depuis le début de l'enregistrement (s)''', 'RR (ms)'])
                for row in df_rr.itertuples(index = False) :
                    writer.writerow(row)
            break
        except PermissionError :
            summon_err_window('Une erreur est survenue, veuillez fermer les fichiers csv de résultats et fermer cette fenêtre.')
            continue
    if not win2 : 
        window_mode.deiconify()

def un_part_etape_1() :
    global window1, hauteur, nombre_de_pages, appercu, nbs_prompt, hauteur_spinbox, text_numpage, nombre_de_pages_prompt, nom_pdf_prompt, sujet_nom_prompt, numero_part_prompt, page_pour_preview, ligne_appercu, nbs, sujet_nom, numero_part, browse_folder_entry, verifier_top_int

    ####################################
    ########## Inputs un part ##########
    ####################################

    window1 = make_window(f'VFC eco - {speed}', '763x465+70+70')
    
    row_var = 0
    nombre_de_pages = '1'
    hauteur = '0'
    sujet_nom = 'participant_X'
    numero_part = 'X'

    ######################################## RETOUR ########################################

    retour_bouton = ttk.Button(window1, text = 'Retour', command = lambda : [window1.destroy(), window_mode.deiconify(), print(verifier_top)])
    retour_bouton.grid(row = row_var, column = 0, sticky = 'w', padx = 10)
    row_var += 1

    ######################################## NOM DU SUJET ########################################

    sujet_nom_label = ttk.Label(window1, text= 'Nom du participant')
    sujet_nom_label.grid(row = row_var, column= 0, sticky = 'e', padx=10, pady=10)
    sujet_nom_prompt = ttk.Entry(window1)
    sujet_nom_prompt.insert(0, 'Nom du participant')
    sujet_nom_prompt.grid(row = row_var, column = 1, sticky = 'w', padx=10, pady=10)
    give_binds(sujet_nom_prompt, 'Nom du participant')

    sujet_nom_boutton = ttk.Button(window1, text = 'Confirmer', command=Confirmer_nom)
    sujet_nom_boutton.grid(row = row_var, column = 2)

    ######################################## NUMÉRO SUJET ########################################

    row_var += 1

    numero_part_label = ttk.Label(window1, text = 'Numéro du participant')
    numero_part_label.grid(row = row_var, column = 0, sticky='e', padx=10, pady=10)
    numero_part_prompt = ttk.Entry(window1)
    numero_part_prompt.insert(0, 'Numéro du participant')
    numero_part_prompt.grid(row = row_var, column = 1, sticky = 'w', padx=10, pady=10)
    give_binds(numero_part_prompt, 'Numéro du participant')  

    numero_part_boutton = ttk.Button(window1, text = 'Confirmer', command=Confirmer_num_part)
    numero_part_boutton.grid(row = row_var, column = 2)

    ######################################## NOM DU FICHIER ########################################

    row_var +=1

    nom_pdf_label = ttk.Label(window1, text = "Nom du fichier pdf")
    nom_pdf_label.grid(row = row_var, column = 0, sticky = 'e', padx = 10)
    nom_pdf_prompt = ttk.Entry(window1)
    nom_pdf_prompt.insert(0, 'Nom du fichier')
    nom_pdf_prompt.grid(row = row_var, column = 1,  padx = 10, pady = 10, sticky = 'w')
    give_binds(nom_pdf_prompt, 'Nom du fichier')

    nom_pdf_boutton = ttk.Button(window1, text = 'Confirmer', command = lambda : [Confirmer_nom_pdf(), creer_images(), afficher_images(), Confirmer_hauteur(), dessiner_appercu()])
    nom_pdf_boutton.grid(row = row_var, column = 2, padx = 10, pady = 10)
    nom_pdf_browse = ttk.Button(window1, text = 'Naviguer', command = lambda : [Browse(), creer_images(), afficher_images(), Confirmer_hauteur(), dessiner_appercu()])
    nom_pdf_browse.grid(row = row_var, column = 3, padx = 10)

    ######################################## NOMBRE DE PAGES ########################################

    row_var += 1

    nombre_de_pages_label = ttk.Label(window1, text = "Pages")
    nombre_de_pages_label.grid(row = row_var, column = 0, padx= 10, pady=10, sticky = 'e')
    nombre_de_pages_prompt = ttk.Entry(window1)
    nombre_de_pages_prompt.insert(0, 'Pages')
    nombre_de_pages_prompt.grid(row = row_var, column = 1, padx = 10, pady = 10, sticky = 'w')
    give_binds(nombre_de_pages_prompt, 'Pages')

    nombre_de_pages_boutton = ttk.Button(window1, text = 'Confirmer', command= lambda : [Confirmer_nbp(), creer_images(), afficher_images(), Confirmer_hauteur(), dessiner_appercu()])
    nombre_de_pages_boutton.grid(row = row_var, column = 2, padx = 10, pady = 10)


    ######################################## HAUTEUR ########################################

    row_var += 1

    hauteur_label = ttk.Label(window1, text = 'Hauteur')
    hauteur_label.grid(row = row_var, column = 0, padx = 10, pady = 10, sticky = 'e')
    hauteur_spinbox = tk.Spinbox(window1, from_ = -300, to = 160, increment = 5, command = lambda : [Confirmer_hauteur(), dessiner_appercu()])
    hauteur_spinbox.grid(row = row_var, column = 1, padx = 10, pady = 10, sticky = 'w')
    hauteur_spinbox.bind("<FocusIn>", on_entry_click_hauteur)
    hauteur_spinbox.bind('<FocusOut>', on_focus_out_hauteur)

    hauteur_spinbox.delete(0, "end")
    hauteur_spinbox.insert(0, "0")

    hauteur_boutton = ttk.Button(window1, text = 'Confirmer', command=Confirmer_hauteur)
    hauteur_boutton.grid(row = row_var, column = 2, padx = 10, pady = 10)

    ######################################## NOMBRE DE SECTIONS ########################################

    row_var += 1

    nbs_label = ttk.Label(window1, text = 'Nombre de sections')
    nbs_label.grid(row = row_var, column = 0, padx = 10, pady= 10, sticky = 'e')
    nbs_prompt = ttk.Entry(window1)
    nbs_prompt.insert(0, '1')
    nbs_prompt.grid(row = row_var, column = 1,  padx = 10, pady = 10, sticky = 'w')
    give_binds(nbs_prompt, '1')
    nbs = '1'

    nbs_boutton = ttk.Button(window1, text = 'Confirmer', command=Confirmer_nbs)
    nbs_boutton.grid(row = row_var, column = 2,  padx = 10, pady = 10)

    row_var += 1

    browse_folder_label = tk.Label(window1, text = 'Dossier des fichiers PDF')
    browse_folder_label.grid(row = row_var, column = 0, sticky = 'e')
    browse_folder_entry = ttk.Entry(window1)
    browse_folder_entry.grid(row = row_var, column = 1, padx = 10)
    try :
        browse_folder_entry.insert(0, folder_path)
    except NameError :
        browse_folder_entry.insert(0, 'Dossier')
    give_binds(browse_folder_entry, 'Dossier')
    browse_folder_button = ttk.Button(window1, text = 'Naviguer', command = Browse_folder)
    browse_folder_button.grid(row = row_var, column = 2, padx = 10, sticky = 'W')


    ######################################## INSTRUCTIONS ########################################

    row_var += 2
    confirm_label = ttk.Label(window1, text = 'Appuyez sur confirmer tout afin de fermer cette page.')
    confirm_label.grid(row= row_var, column=0, columnspan = 5, pady = 10)

    row_var += 1
    nbp_instructions = tk.Label(window1, text = 'Pour sélectionner les X premières pages, entrez X dans la case pages. Pour seulement sélectionner la page Y, entrez !Y. \nPour les pages Z à W, entrez Z-W. Séparez les entrées par une virgule. \nPar exemple : « 4, !6, 8-10 » sélectionnerait les pages 1, 2, 3, 4, 6, 8, 9, 10.')
    nbp_instructions.grid(row= row_var, column=0, columnspan = 6, pady = 10, padx = 10)

    ######################################## APPERCU ######################################## 

    appercu_label = tk.Label(window1, text = 'Aperçu de la hauteur')
    appercu_label.grid(column = 4, columnspan = 3, row = 0)

    appercu = tk.Canvas(window1, width = 256, height = 256)
    appercu.grid(column = 4, columnspan = 3, row = 1, rowspan = 6)

    page_pour_preview = '1'

    left_boutton = tk.Button(window1, text = '<-', command = move_left)
    left_boutton.grid(row = row_var-3, column = 4)
    right_boutton = tk.Button(window1, text = '->', command = move_right)
    right_boutton.grid(row = row_var-3, column = 6)

    text_numpage = tk.StringVar()
    label_numpage = tk.Label(window1, textvariable = text_numpage)
    label_numpage.grid(row = row_var-3, column = 5)

    ligne_appercu = appercu.create_line(0,0,1,0)

    ######################################## CONFIRMER TOUT ########################################

    boutton_confirmer_tout = ttk.Button(window1, text = 'Confirmer tout', command = confirmer_tout)
    boutton_confirmer_tout.grid(column =5, row = row_var-2)

    if speed == 'vitesse normale' :
        verifier_top_int = tk.IntVar()
        ver_top_checkbox = tk.Checkbutton(window1, text = 'Vérifier chaque pic (prend plus de temps)', var = verifier_top_int)
        ver_top_checkbox.grid(row = row_var-1, column = 4, columnspan= 3)

    window1.protocol("WM_DELETE_WINDOW", handle_win1_destroy)
    
    window1.mainloop()

def mettre_top_verif() :
    global verifier_top
    if verifier_top_int.get() == 1 :
        verifier_top = True
    elif verifier_top_int.get() == 0 :
        verifier_top = False 

def handle_win1_destroy() :
    ive_had_enough()
    window1.destroy()
    if not window_mode.winfo_viewable() and not on_va_faire_etape1 :
        window_mode.destroy()

def cleanup_apres_apercu() :
    try :
        for i in range(1,14) :
            noms_possibles = [f'{folder_path}\\{sujet_nom}_#{numero_part}_preview{i}.png', f'{folder_path}\\participant_X_#{numero_part}_preview{i}.png', f'{folder_path}\\{sujet_nom}_#X_preview{i}.png', f'{folder_path}\\participant_X_#X_preview{i}.png']
            for nom_de_fichier_a_supprimer_appercu in noms_possibles :
                if os.path.exists(nom_de_fichier_a_supprimer_appercu) :
                    os.remove(nom_de_fichier_a_supprimer_appercu)
    except NameError :
        return None

    print('cleanup')


# def plusieur_part_etape_1() :
#     global sujet_nom, numero_part, nom_pdf, path_pdf, nombre_de_pages, hauteur, nbs
#     if mode == 'plusieurs_part' and etape_var :
#         encodings = ['utf-8', 'utf-8-sig', 'ISO-8859-1', 'Windows-1252']
#         for enc in encodings:
#             try :
#                 df_participants = pd.read_csv(fichier_input, encoding = enc)
#             except UnicodeDecodeError :
#                 pass
#         for part in range(len(df_participants)) :
#             sujet_nom = df_participants['Nom du participant'][part]
#             numero_part = df_participants['Numéro du participant'][part]
#             nom_pdf = df_participants['Nom du fichier pdf'][part]
#             if not nom_pdf[-4:] == '.pdf' :
#                 nom_pdf += '.pdf'
#             path_pdf = f'{folder_path}\\{nom_pdf}'
#             nombre_de_pages = df_participants['Nombre de pages'][part]
#             hauteur = 1290 - int(df_participants['Hauteur'][part]) 
#             nbs = int(df_participants['Nombre de sections'][part])
#             window_mode.withdraw()
#             # window_progression(numero_part)

########################################
########## Correction  des RR ##########
########################################

def window2_func() :
    global win2, window2
    print('window2 func')
    if etape_var :
        ive_had_enough_var = False
        while not ive_had_enough_var :
            smallest_indices = sorted(range(len(RR_en_ms)), key=lambda x: RR_en_ms[x])[:10]

            win2 = True

            window2 = make_window('VFC eco - Correction des RR', '345x290+100+100')

            ######################################## AFFICHER LES 10 PLUS PETITS RR ########################################
            num_indices = len(smallest_indices)
            for i in range(min(10, num_indices)):
                RR_value = round(RR_en_ms[smallest_indices[i]])
                time_value = round(total_times[smallest_indices[i]])
                label_text = f"RR : {RR_value} ms, Temps depuis le début de l'enregistement : {time_value} s"
                label = ttk.Label(window2, text=label_text)
                label.grid(row=i, column=0, padx = 10)

            if num_indices < 10:
                warning_text = f"Seulement {num_indices} intervalles RR sont disponibles."
                warning_label = ttk.Label(window2, text=warning_text, foreground="red")
                warning_label.grid(row=10, column=0)
            else :
                VFC2_label1 = ttk.Label(window2, text = 'Voici les 10 plus petits intervalles RR.')
                VFC2_label1.grid(row = 10, column = 0)

            VFC2_label2 = ttk.Label(window2, text = 'Vous devez maintenant retirer les artéfacts.')
            VFC2_label2.grid(row = 11, column = 0, padx= 10)

            VFC2_corr = ttk.Button(window2, text = 'Corriger les pics R', command = rr_correct)
            VFC2_corr.grid(row = i+3, column = 0)

            VFC2_skip = ttk.Button (window2, text = 'Correction terminée', command = skip_corr_or_destroy)
            VFC2_skip.grid(row = i+4, column = 0)

            window2.protocol("WM_DELETE_WINDOW", lambda : window_mode.destroy())

            window2.mainloop()

def skip_corr_or_destroy() :
    filename = f'{folder_path}\\{image_folder}\\{sujet_nom_num}_RR Corrigé.csv'
    if not os.path.exists(filename) :
        shutil.copy(f'{filename[:-12]}.csv', filename)
    ive_had_enough() 
    window2.destroy() 
    demander_sections()


########################################
########### Faire  les maths ###########
########################################

######################################## DEMANDER LES SECTIONS ########################################
def demander_sections() :
    global section_values, brokey, total_times
    print('je demande sections')

    try :
        folder_path, image_folder
    except NameError :
        summon_err_window('Veuillez préciser où se trouve les fichiers pour ce participant à la page précédente.')
        window_mode.deiconify()
        return None

    print(folder_path, image_folder, sujet_nom_num)


    if not etape_var :
        try :
            if os.path.exists(f'{folder_path}\\{image_folder}\\{sujet_nom_num}_RR Corrigé.csv') :
                file = f'{folder_path}\\{image_folder}\\{sujet_nom_num}_RR Corrigé.csv'
            else :
                file = f'{folder_path}\\{image_folder}\\{sujet_nom_num}_RR.csv'
        except NameError :
            if os.path.exists(f'{sujet_nom_num}_RR Corrigé.csv') :
                file = f'{sujet_nom_num}_RR Corrigé.csv'
            else :
                file = f'{sujet_nom_num}_RR.csv'

        print('file', file)

        encodings = ['utf-8', 'utf-8-sig', 'ISO-8859-1', 'Windows-1252']
        for enc in encodings:
            try:
                df_total_times = pd.read_csv(file, encoding = enc)
                break
            except (UnicodeDecodeError, FileNotFoundError) as e :
                if isinstance(e, FileNotFoundError) :
                    summon_err_window(f'Veuillez spécifier le dossier contenant le fichier de RR ({sujet_nom_num}_RR.csv) à la page précédente')
                    window_mode.deiconify()
                    brokey = True
                    return None
        total_times = df_total_times['''Temps depuis le début de l'enregistrement (s)'''].tolist()

    if mode == 'un_part' :
        if nbs == 1 :
            section_values = [0, total_times[-1]]
            print(section_values)
            etape_2()
        else :
            sections = []

            def Confirmer_sections() :
                global section_values
                section_values = []
                for entry in sections:
                    section_values.append(entry.get())
                window3.destroy()
                etape_2()

            window3 = make_window('VFC eco - Sections', f'280x{nbs*20+55}+100+100')

            VFC3_Label1 = ttk.Label(window3, text='Début de la section (s)')
            VFC3_Label1.grid(row=0, column=0)

            VFC3_Label2 = ttk.Label(window3, text='Fin de la section (s)')
            VFC3_Label2.grid(row=0, column=2)

            for y in range(nbs) :
                for x in [0, 2] :
                    section_ordre = ttk.Entry(window3)
                    # if x == 0 :
                    #     sticcy = 'E'
                    # else :
                    #     sticcy = 'W'
                    section_ordre.grid(row=y+1, column=x, padx = 5)#, sticky = sticcy)
                    sections.append(section_ordre)
                section_a = ttk.Label(window3, text = 'à')
                section_a.grid(row = y+1, column = 1)    

            VFC3_button = ttk.Button(window3, text='Confirmer', command=Confirmer_sections)
            VFC3_button.grid(row=nbs+1, column=0, columnspan=3)

            window3.protocol('WM_DELETE_WINDOW', lambda : window_mode.destroy())

            window3.mainloop()
    print(f'les sections sont {section_values}')

# def plusieurs_part_etape2() :
#     global sujet_nom, numero_part, nom_pdf, nombre_de_pages, hauteur, section_values
#     encodings = ['utf-8', 'utf-8-sig', 'ISO-8859-1', 'Windows-1252']
#     for enc in encodings:
#         try:
#             df_participants = pd.read_csv(fichier_input, encoding = enc, header = 1)
#         except UnicodeDecodeError :
#             pass
#     for ligne in df_participants.iterrows(index = False) :
#         sujet_nom = ligne['Nom du participant']
#         numero_part = ligne['Numéro du participant']
#         nom_pdf = ligne['Nom du fichier pdf']
#         nombre_de_pages = ligne['Nombre de pages']
#         hauteur = 1290 - int(ligne['Hauteur']) 
#         nbs = int(ligne['Nombre de sections'])
#         if nbs == 1 :
#             encodings = ['utf-8', 'utf-8-sig', 'ISO-8859-1', 'Windows-1252']
#             for enc in encodings:
#                 try:
#                     df_total_times = pd.read_csv(f'{folder_path}\\{sujet_nom_num}_RR Corrigé.csv', encoding = enc)
#                 except UnicodeDecodeError :
#                     pass
#             section_values = [0, df_total_times['''Temps depuis le début de l'enregistrement'''][-1]]
#         else :
#             section_values = ligne[5:]
#         etape_2()

####################################
############### Mode ###############
####################################

debut = 192
fin = 3414
sujet_nom_num = ''

stat_var = False
graph_mode = False
win2 = False
parent_exist = False
on_va_faire_etape1 = False
brokey = False
images_a_clean = True
verifier_top = False

make_main_window()