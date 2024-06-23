import tkinter as tk
from tkinter import ttk
import time
import pyautogui
import numpy as np
import cv2 as cv2
import csv 
import os
import pandas as pd
import numpy as np
import csv
import re
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
import math

window1 = tk.Tk()
window1.title('VFC étape 1')

########################################################################################NOM DU SUJET########################################################################################

def on_entry_click_nom(event):
    if sujet_nom_prompt.get() == 'Nom du participant':
        sujet_nom_prompt.delete(0, "end")  # Delete the current content of the Entry widget
        sujet_nom_prompt.insert(0, '')  # Insert an empty string

def on_focus_out_nom(event):
    if sujet_nom_prompt.get() == '':
        sujet_nom_prompt.insert(0, 'Nom du participant')  # If the Entry widget is empty, insert the default text

def Confirmer_nom():
    global sujet_nom
    sujet_nom = sujet_nom_prompt.get()
    print(sujet_nom)

sujet_nom_prompt = ttk.Entry(window1)
sujet_nom_prompt.insert(0, 'Nom du participant')
sujet_nom_prompt.grid(row = 0, column = 0, padx = 10, pady = 10)
sujet_nom_prompt.bind("<FocusIn>", on_entry_click_nom)  # Bind the on_entry_click function to the FocusIn event
sujet_nom_prompt.bind("<FocusOut>", on_focus_out_nom)  # Bind the on_focus_out function to the FocusOut event

sujet_nom_boutton = ttk.Button(window1, text = 'Confirmer', command=Confirmer_nom)
sujet_nom_boutton.grid(row = 0, column = 1, columnspan=2, padx = 10, pady = 10)

########################################################################################NUMÉRO SUJET########################################################################################

def on_entry_click_numero_part(event):
    if numero_part_prompt.get() == 'Numéro du participant':
        numero_part_prompt.delete(0, "end")  # Delete the current content of the Entry widget
        numero_part_prompt.insert(0, '')  # Insert an empty string

def on_focus_out_numero_part(event):
    if numero_part_prompt.get() == '':
        numero_part_prompt.insert(0, 'Numéro du participant')  # If the Entry widget is empty, insert the default text

def Confirmer_num_part():
    global numero_part
    numero_part = numero_part_prompt.get()
    print(numero_part)

numero_part_prompt = ttk.Entry(window1)
numero_part_prompt.insert(0, 'Numéro du participant')
numero_part_prompt.grid(row = 1, column = 0, padx = 10, pady = 10)
numero_part_prompt.bind("<FocusIn>", on_entry_click_numero_part)  # Bind the on_entry_click function to the FocusIn event
numero_part_prompt.bind("<FocusOut>", on_focus_out_numero_part)  # Bind the on_focus_out function to the FocusOut event

numero_part_boutton = ttk.Button(window1, text = 'Confirmer', command=Confirmer_num_part)
numero_part_boutton.grid(row = 1, column = 1, columnspan=2, padx = 10, pady = 10)

########################################################################################NOMBRE DE PAGES########################################################################################

def on_entry_click_nbp(event):
    if nombre_de_pages_prompt.get() == 'Nombre de pages':
        nombre_de_pages_prompt.delete(0, "end")  # Delete the current content of the Entry widget
        nombre_de_pages_prompt.insert(0, '')  # Insert an empty string

def on_focus_out_nbp(event):
    if nombre_de_pages_prompt.get() == '':
        nombre_de_pages_prompt.insert(0, 'Nombre de pages')  # If the Entry widget is empty, insert the default text

def Confirmer_nbp():
    global nombre_de_pages
    nombre_de_pages = nombre_de_pages_prompt.get()
    print(nombre_de_pages)

nombre_de_pages_prompt = ttk.Entry(window1)
nombre_de_pages_prompt.insert(0, 'Nombre de pages')
nombre_de_pages_prompt.grid(row = 2, column = 0, padx = 10, pady = 10)
nombre_de_pages_prompt.bind("<FocusIn>", on_entry_click_nbp)  # Bind the on_entry_click function to the FocusIn event
nombre_de_pages_prompt.bind("<FocusOut>", on_focus_out_nbp)  # Bind the on_focus_out function to the FocusOut event

nombre_de_pages_boutton = ttk.Button(window1, text = 'Confirmer', command=Confirmer_nbp)
nombre_de_pages_boutton.grid(row = 2, column = 1, columnspan=2, padx = 10, pady = 10)


########################################################################################HAUTEUR########################################################################################

def on_entry_click_hauteur(event):
    if hauteur_prompt.get() == 'Hauteur':
        hauteur_prompt.delete(0, "end")  # Delete the current content of the Entry widget
        hauteur_prompt.insert(0, '')  # Insert an empty string

def on_focus_out_hauteur(event):
    if hauteur_prompt.get() == '':
        hauteur_prompt.insert(0, 'Hauteur')  # If the Entry widget is empty, insert the default text

def Confirmer_hauteur():
    global hauteurp
    hauteurp = hauteur_prompt.get()
    print(hauteurp)

hauteur_prompt = ttk.Entry(window1)
hauteur_prompt.insert(0, 'Hauteur')
hauteur_prompt.grid(row = 3, column = 0, padx = 10, pady = 10)
hauteur_prompt.bind("<FocusIn>", on_entry_click_hauteur)  # Bind the on_entry_click function to the FocusIn event
hauteur_prompt.bind("<FocusOut>", on_focus_out_hauteur)  # Bind the on_focus_out function to the FocusOut event

hauteur_boutton = ttk.Button(window1, text = 'Confirmer', command=Confirmer_hauteur)
hauteur_boutton.grid(row = 3, column = 1, columnspan=2, padx = 10, pady = 10)

########################################################################################NOMBRE DE SECTIONS########################################################################################

def on_entry_click_nbs(event):
    if nbs_prompt.get() == 'Nombre de sections':
        nbs_prompt.delete(0, "end")  # Delete the current content of the Entry widget
        nbs_prompt.insert(0, '')  # Insert an empty string

def on_focus_out_nbs(event):
    if nbs_prompt.get() == '':
        nbs_prompt.insert(0, 'Nombre de sections')  # If the Entry widget is empty, insert the default text

def Confirmer_nbs():
    global nbs
    nbs = nbs_prompt.get()
    print(nbs)

nbs_prompt = ttk.Entry(window1)
nbs_prompt.insert(0, 'Nombre de sections')
nbs_prompt.grid(row = 4, column = 0, padx = 10, pady = 10)
nbs_prompt.bind("<FocusIn>", on_entry_click_nbs)  # Bind the on_entry_click function to the FocusIn event
nbs_prompt.bind("<FocusOut>", on_focus_out_nbs)  # Bind the on_focus_out function to the FocusOut event

nbs_boutton = ttk.Button(window1, text = 'Confirmer', command=Confirmer_nbs)
nbs_boutton.grid(row = 4, column = 1, columnspan=2, padx = 10, pady = 10)

#######################################################################INSTRUCTIONS###############################################################

hauteur_label = ttk.Label(window1, text = 'La hauteur par défaut est zéro. Une hauteur négative peut être nécessaire si les complexes QRS sont très petits.')
hauteur_label.grid(row=5, column=0, columnspan = 3, pady = 10)
confirm_label = ttk.Label(window1, text = 'Appuyez sur confirmer avant de fermer cette page.')
confirm_label.grid(row=6, column=0, columnspan = 3, pady = 10)
ten_sec_label = ttk.Label(window1, text = 'Lorsque vous fermerez cette page, vous aurez 10 secondes pour ouvrir le fichier PDF en plein écran, à la page 1')
ten_sec_label.grid(row=7, column=0, columnspan = 3, pady = 10)

window1.mainloop()

nbs = int(nbs)
nombre_de_pages = int(nombre_de_pages)
hauteur = 540 - int(hauteurp)
print('Nom du participant :', sujet_nom)
print('Nombre de pages :', nombre_de_pages)
print('Hauteur :', hauteur)


####################################################################################################LECTURE###################################################################################################
##############################################################################################################################################################################################################

time.sleep(10)
for i in range(1,nombre_de_pages+1) : 
    filename_string = f'{sujet_nom}_#{numero_part}_page_{i:03}.png'
    print(filename_string)
    time.sleep(0.4)
    screenshot = pyautogui.screenshot()
    screenshot.save(filename_string)
    pyautogui.press('pagedown')
pyautogui.press('esc')

debut = 330
fin = 1593

def draw_lines_and_find_highest(image_name, current_coords) :
    #importer l'image
    if os.path.exists(f'{image_name}_output.png') :
        image = cv2.imread(f'{image_name}_output.png')
    else :
        image = cv2.imread(f'{image_name}.png')
    
###############################################partir la boucle while ici#########################################

    while True :

        #préparer les current coordonnées
        current_x = current_coords[1]
        current_y = current_coords[0]

        #initier la liste
        couleurs_coordonnees = []

        #remplir la liste
        for x in range(current_x-1, current_x+4) :
            for y in range(current_y - 20, current_y+1) :
                blue = image[y,x,0]
                red = image[y,x,2]
                couleurs_coordonnees.append([y, x, blue, red])

        #trouver le prochain pixel    
        filtered_couleurs_coordonnees = [couleur_coordonnee for couleur_coordonnee in couleurs_coordonnees if couleur_coordonnee[2] < 150 and couleur_coordonnee[3] < 150]

        if filtered_couleurs_coordonnees :
            prochain_pixel = max(filtered_couleurs_coordonnees, key = lambda x : (-x[0], -x[1]))
        else :
            print('Erreur : la liste de filtered couleurs coordonnées est vide')
        
        #si on bouge plus, faire un + et break
        if prochain_pixel[0] == current_coords[0] :
            #check autour
            top_vérif = []
            rayon_de_vérif = [current_x-8, current_x-1, current_x+8]
            for x in rayon_de_vérif :
                if not x == current_x-1 :
                    for y in range(current_y, current_y+30) :
                        blue = image[y,x,0]
                        red = image[y,x,2]
                        top_vérif.append([y, x, blue, red])
                        image[y,x] = [255,0,0]
                        cv2.imwrite(f'{image_name}_output.png', image)
                else : 
                    for y in range(current_y-5, current_y) :
                        blue = image[y,x,0]
                        red = image[y,x,2]
                        top_vérif.append([y, x, blue, red])
                        image[y,x] = [255,0,0]
                        cv2.imwrite(f'{image_name}_output.png', image)

            filtered_top_vérif = [pixel for pixel in top_vérif if pixel[2] < 150 and pixel[3] < 150]
            #si aucun des pixels vérifiés n'est noir, c'est bon, on append
            if filtered_top_vérif == [] :
                image[current_coords[0]-20:current_coords[0]+20, current_coords[1]] = [0, 255, 0]
                image[current_coords[0], current_coords[1]-20:current_coords[1]+20] = [0, 255, 0]
                R_peaks_in_pixels.append(current_coords[1])
                cv2.imwrite(f'{image_name}_output.png', image) ################################################problème ici jsp c'est quoi exactement
                # cv2.imshow('title',image)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                break
            else :
                image[current_coords[0]-20:current_coords[0]+20, current_coords[1]-1:current_coords[1]+1] = [0, 0, 255]
                image[current_coords[0]-1:current_coords[0]+1, current_coords[1]-20:current_coords[1]+20] = [0, 0, 255]
                cv2.imwrite(f'{image_name}_output.png', image)
                print(f"Je pense avoir détecté quelque chose qui n'est pas un pic à {(current_coords[1] - debut)*10/(fin-debut) + (page-1) * 10} secondes")
                R_peaks_in_pixels.append(current_coords[1])
                # cv2.imshow('title',image)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                break
        else :
            #dessiner le prochain pixel en vert et s'y déplacer
            image[prochain_pixel[0], prochain_pixel[1]-4:prochain_pixel[1]+4] = [0,255,0]
            current_coords = [prochain_pixel[0], prochain_pixel[1]]
            # cv2.imshow('title',image)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

for i in range(1, nombre_de_pages+1) :
    nom_de_fichier_à_supprimer = f'{sujet_nom}_#{numero_part}_page_{i:03}_output.png'
    if os.path.exists(nom_de_fichier_à_supprimer) :
        os.remove(nom_de_fichier_à_supprimer)
        print(f"J'ai supprimé le fichier {nom_de_fichier_à_supprimer}")
    else :
        print(f"Je n'ai pas trouvé de fichier appelé {nom_de_fichier_à_supprimer}")

reste = None
RR_en_pixels = []
total_times = []

#gérer les listes et append entre les pages
for page in range(1,nombre_de_pages+1) :
    image_name = f'{sujet_nom}_#{numero_part}_page_{page:03}'
    image = cv2.imread(f'{image_name}.png')
    R_peaks_in_pixels = []
    pixels_détectés_à_lancienne = np.where(image[hauteur,:,2] <150)[0] 
    pixels_détectés_à_lancienne_filtrés = pixels_détectés_à_lancienne[(pixels_détectés_à_lancienne > debut) & (pixels_détectés_à_lancienne < fin)]

    pixels_détectés_à_lancienne_filtrés_liste = []
    previous_value = None

    for value in pixels_détectés_à_lancienne_filtrés :
        if previous_value is None or (value - previous_value) >= 10 :
            pixels_détectés_à_lancienne_filtrés_liste.append(value)
            previous_value = value


    for pixel_détecté_à_lancienne_de_la_liste in pixels_détectés_à_lancienne_filtrés_liste :
        current_coords = [hauteur, pixel_détecté_à_lancienne_de_la_liste]
        draw_lines_and_find_highest(image_name, current_coords)
    
    if not page == 1 :
        RR_en_pixels[-1] += R_peaks_in_pixels[0]-debut
        # print(RR_en_pixels[-1])

    for i in range(len(R_peaks_in_pixels)-1) :
        RR_en_pixels.append(R_peaks_in_pixels[i+1]-R_peaks_in_pixels[i])
        # total time : temps entre le début et le moment ou le RR commence
        total_times.append((R_peaks_in_pixels[i] - debut)*10/(fin-debut) + (page-1) * 10)
    if page < nombre_de_pages :
        RR_en_pixels.append(fin - R_peaks_in_pixels[-1])
        total_times.append((R_peaks_in_pixels[-1] - debut)*10/(fin-debut) + (page-1) * 10)


# if len(RR_en_pixels) == len(total_times)+1 :
#     del RR_en_pixels[-1]
    
# print(RR_en_pixels)

print(type(RR_en_pixels))
RR_en_ms = [RR * (10000/(fin-debut)) for RR in RR_en_pixels]
print('RR en ms', ['%.0f' % elem for elem in RR_en_ms])
print('total_times', total_times)
print('RR len', len(RR_en_ms), "Total len", len(total_times))
print(type(RR_en_ms))


#####################################################################################FIN DE LA LECTURE################################################################################

sujet_nom_num = f'{sujet_nom}_#{numero_part}'
# Write the CSV file
with open(f'{sujet_nom_num}_line_distances.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['x', 'y'])
    for (total_time, unRR_en_ms) in zip(total_times, RR_en_ms):
        writer.writerow([total_time,unRR_en_ms])
print(type(RR_en_ms))
# Get the indices of the 10 smallest values of 'Période'
smallest_indices = sorted(range(len(RR_en_ms)), key=lambda x: RR_en_ms[x])[:10]
print('smallest indices :', smallest_indices)
# Print the 10 smallest values of 'Période' with their corresponding 'total_time'
# print("10 Smallest RR_en_ms:")
# for idx in smallest_indices:
#     print(f"Période: {RR_en_ms[idx]}, Temps depuis le début de l'enregistement: {total_times[idx]}")

################################################################WINDOW 2######################################################################################################################################
##############################################################################################################################################################################################################

window2 = tk.Tk()
window2.title('VFC étape 2')

# Check if there are enough elements in smallest_indices
num_indices = len(smallest_indices)
for i in range(min(10, num_indices)):
    RR_value = round(RR_en_ms[smallest_indices[i]])
    time_value = round(total_times[smallest_indices[i]])
    label_text = f"RR : {RR_value} ms, Temps depuis le début de l'enregistement : {time_value} s"
    label = ttk.Label(window2, text=label_text)
    label.grid(row=i, column=0)

# If there are fewer than 10 elements, notify the user
if num_indices < 10:
    warning_text = f"Only {num_indices} RR values available."
    warning_label = ttk.Label(window2, text=warning_text, foreground="red")
    warning_label.grid(row=10, column=0)

VFC2_label1 = ttk.Label(window2, text = 'Voici les 10 plus petits intervalles RR.')
VFC2_label1.grid(row = 10, column = 0)

VFC2_label2 = ttk.Label(window2, text = 'Vous devez maintenant retirer les artéfacts. Lorsque les artéfacts sont corrigés, fermez cette page.')
VFC2_label2.grid(row = 11, column = 0)

window2.mainloop()

###############################################################WINDOW 3#################################################################

if nbs == 1 :
    section_values = [0, total_times[-1]]
else :
    sections = []

    def Confirmer_sections():
        global section_values
        section_values = []
        for entry in sections:
            section_values.append(entry.get())
        window3.quit()  # Quit the mainloop after getting the values

    def create_gui():
        global window3
        window3 = tk.Tk()
        window3.title('VFC étape 3')

        VFC3_Label1 = ttk.Label(window3, text='Début de la section (s)')
        VFC3_Label1.grid(row=0, column=0)

        VFC3_Label2 = ttk.Label(window3, text='Fin de la section (s)')
        VFC3_Label2.grid(row=0, column=1)

        for y in range(nbs):
            for x in range(2):
                section_ordre = tk.Entry(window3)
                section_ordre.grid(row=y+1, column=x, pady=10, padx=10)
                sections.append(section_ordre)

        VFC3_button = ttk.Button(window3, text='Confirmer', command=Confirmer_sections)
        VFC3_button.grid(row=nbs+1, column=0, columnspan=2, pady=10)

        window3.mainloop()

    create_gui()

    # Now section_values contains the entered values
    print('Section values:', section_values)

###############################################################RESTORE  LIST###############################################################

# Read the two CSV files into DataFrames
df_full = pd.read_csv(f'{sujet_nom_num}_line_distances.csv')
df_partial = pd.read_csv(f'{sujet_nom_num}_line_distances Corrigé.csv')

# Round the 'x' values to a certain decimal precision
decimal_precision = 2  # You can adjust this as needed
df_full['x_rounded'] = df_full['x'].round(decimal_precision)
df_partial['x_rounded'] = df_partial['x'].round(decimal_precision)

# Find x values in the full list that are not in the partial list
missing_x = df_full[~df_full['x_rounded'].isin(df_partial['x_rounded'])]

# Add the missing x values with y values set to 0 to the partial list
result = pd.concat([df_partial, missing_x.assign(y=0)])

# Sort by 'x' values
result = result.sort_values('x')

# Write the result to a new CSV file
result.to_csv(f'{sujet_nom_num}_line_distances_avec_zeros.csv', index=False)

###############################################################CALCUL DE VFC###############################################################
###########################################################################################################################################

# Load the CSV file
df = pd.read_csv(f'{sujet_nom_num}_line_distances Corrigé.csv')
try :
    dfpd = pd.read_csv(f'{sujet_nom_num}_line_distances_avec_zeros.csv')
except FileNotFoundError :
    dfpd = df

groupe_colonne=0

for i in range(nbs) :
    lower_bound = int(section_values[i*2])
    upper_bound = int(section_values[i*2+1])
    filtered_df = df[(df['x'] > lower_bound) & (df['x'] < upper_bound)] 
    filtered_df_pour_diff = dfpd[(dfpd['x'] > lower_bound) & (dfpd['x'] < upper_bound)]

    mean_HR = 60000/np.mean(filtered_df['y'])

    # Interpolate using Cubic Spline
    x = filtered_df['x']
    y = filtered_df['y']
    cs = CubicSpline(x, y)


    # Generate interpolated x values every 0.1
    x_interp = np.arange(x.iloc[0], x.iloc[-1], 0.1)

    # Interpolate y values
    y_interp = cs(x_interp)


    # Create a new DataFrame with the interpolated values
    df_interp = pd.DataFrame({'x': x_interp, 'y': y_interp})

    # Save the interpolated data to a new CSV file
    df_interp.to_csv(f'{sujet_nom_num}_interpolated_data{i+1}.csv', index=False)


    # Load the CSV file
    data = pd.read_csv(f'{sujet_nom_num}_interpolated_data{i+1}.csv')

    average = np.mean(y)

    # Assuming your CSV file has columns 'x' and 'y'
    x = data['x'].values 
    y = data['y'].values - average

    # Perform the FFT
    fft_result = np.fft.fft(y)
    fft_magnitude = np.abs(fft_result)

    # Calculate the corresponding frequencies
    n = len(y)
    sampling_frequency = 1 / (x[1] - x[0])
    frequencies = np.fft.fftfreq(n, d=1/sampling_frequency)

    magnitude_squared = fft_magnitude**2
    PSD = (1/(n*sampling_frequency)) * magnitude_squared

    # On veut juste la partie positive
    frequencies_positive = frequencies[:n//2]
    fft_magnitude_positive = fft_magnitude[:n//2]
    PSD_positive = PSD[:n//2]


    # Select data points within the range 0.04 to 0.15
    LFmask = np.logical_and(frequencies_positive > 0.04 , frequencies_positive < 0.15) 

    LF = frequencies_positive[LFmask]
    PSD_LF = PSD_positive[LFmask]


    HFmask = np.logical_and(frequencies_positive > 0.15, frequencies_positive < 0.4)

    HF = frequencies_positive[HFmask]
    PSD_HF = PSD_positive[HFmask]


    # Perform trapezoidal integration
    LFintegral = np.trapz(PSD_LF, LF)
    HFintegral = np.trapz(PSD_HF, HF)


    # print("LF :", LFintegral)
    # print("HF :", HFintegral)
    # print("LF/HF :", LFintegral/HFintegral)
    # print('mean hr :', mean_HR)

##################################################time domain###################################################

    Column_Name = 'y'

    # Calculate standard deviation
    std_dev = filtered_df[Column_Name].std()

    # Calculate the number of successive data points that differ by more than 40
    diff = np.abs(filtered_df_pour_diff[Column_Name].diff())
    num_diff_40 = len(diff[(diff > 40) & (diff <= 300)])

    print('len filtered df :', len(filtered_df), 'len dfpd', len(filtered_df_pour_diff))

    pRR40 = num_diff_40/(len(filtered_df))

    # Calculate the root mean square of the difference between each successive data value
    #rms_diff = np.sqrt(np.mean(filtered_df_pour_diff[Column_Name].diff()**2))

    # Calculate the differences between consecutive data values
    diff_values = filtered_df_pour_diff[Column_Name].diff()

    # Set differences greater than 250 to NaN
    diff_values[diff_values > 500] = np.nan

    # Calculate the root mean square of the differences
    rms_diff = np.sqrt(np.nanmean(diff_values**2))



    row_number = int(numero_part)+1

    values = {
        int(groupe_colonne*7+1) : rms_diff,
        int(groupe_colonne*7+2) : pRR40,
        int(groupe_colonne*7+3) : std_dev,
        int(groupe_colonne*7+4) : LFintegral,
        int(groupe_colonne*7+5) : HFintegral,
        int(groupe_colonne*7+6) : LFintegral/HFintegral,
        int(groupe_colonne*7+7) : mean_HR
    }
    csv_file_path = 'Résultats_VFC.csv'

    # Read the existing CSV data
    rows = []
    with open(csv_file_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)

    # Ensure that row_number is within the valid range
    if row_number < 0 or row_number >= len(rows):
        print(f"Error: row_number ({row_number}) is out of range.")
        exit()



    # Update the values at the specified column indices on the specified row
    for col_index, value in values.items():
        try:
            rows[row_number][col_index] = value
        except Exception as e:
            print('rows', rows)
            print('row number', row_number)
            print('col index', col_index)
            

    # Write the updated data back to the CSV file
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    groupe_colonne +=1