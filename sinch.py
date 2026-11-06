# -*df = pd.read_csv(f,- coding: utf-8 -*-
"""
Created on Wed Nov  4 12:05:39 2026

@author: mh2656
"""

# Import packages
from tkinter.filedialog import askdirectory
import pandas as pd
import psutil,os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from PIL import Image

# Check run times
print("Welcome to SINCH!")
print()
print("Before we start, were all of your files obtained over the same sample runtime? (y/n) ")
runtimes = input()

if runtimes.lower() == 'y':
   print("Enter runtime in minutes: ")
   mins = input()
   print("Enter frequency of data sampling in seconds: ")
   secs = input()
   print("Got it. Go ahead and select your data folder!")
   
   # Load in files and concatenate into data frame
   path = askdirectory(title="Select Folder")
   csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
   li = []
   for file in csv_files:
       df = pd.read_csv(os.path.join(path, file), skiprows=3, sep=",")
       li.append(df)
   df = pd.concat(li, axis=0, ignore_index = True)
   
   # Figure out where to split data frame
   mins = float(mins) * 60
   secs = float(secs)
   n = int(mins / secs)
           
   # Create smaller data frames for each injection volume
   df_1 = df.iloc[0:n]
   df_2 = df.iloc[n:n*2]
   df_5 = df.iloc[n*2:n*3]
   df_10 = df.iloc[n*3:n*4]
   df_20 = df.iloc[n*4:n*5]

   # Define data for plotting
   fig, ax = plt.subplots()
   x1 = df_1["Time(min)"]
   x2 = df_2["Time(min)"]
   x5 = df_5["Time(min)"]
   x10 = df_10["Time(min)"]
   x20 = df_20["Time(min)"]
   y1 = df_1["Relative Abundance"]
   y2 = df_2["Relative Abundance"]
   y5 = df_5["Relative Abundance"]
   y10 = df_10["Relative Abundance"]
   y20 = df_20["Relative Abundance"]

   # Plot data
   ax.fill_between(x20, y20, color='#440154')
   ax.fill_between(x10, y10, color='#3b528b')
   ax.fill_between(x5, y5, color='#21918c')
   ax.fill_between(x2, y2, color='#5ec962')
   ax.fill_between(x1, y1, color='#fde725')

   # Create legend
   legend_elements = [Line2D([0],[0], marker='o', label='1 μL', color='#fde275'),
                      Line2D([0],[0], marker='o', label='2 μL', color='#5ec962'),
                      Line2D([0],[0], marker='o', label='5 μL', color='#21918c'),
                      Line2D([0],[0], marker='o', label='10 μL', color='#3b528b'),
                      Line2D([0],[0], marker='o', label='20 μL', color='#440154')]

   # Add graph features
   ax.set_xlabel("Retention time / minutes")
   ax.set_ylabel("Relative abundance")
   ax.legend(handles=legend_elements)

   # Check file before saving
   plt.savefig("temp.jpg")
   print("Opening plot preview...")
   preview = Image.open("temp.jpg")
   preview.show()

   # Save plot
   print("Save plot? (y/n) ")
   save_decision = input()
   if save_decision.lower() == 'y':
      print("Enter file name to save under: ")
      save_plot = input()
      save_name = save_plot + ".jpg"
      saved = plt.savefig(save_name)
      print("File saved successfully!")
   elif save_decision.lower() == 'n':
       print("Saving aborted. Please re-run this script if you change your mind.")
   else:
       print("Your input was not a valid option. Please re-run this script and type either 'y' or 'n' only.")
       
   # Close image viewer
   for process in (process for process in psutil.process_iter() if process.name()=="Photos.exe"):
       process.kill()
   
elif runtimes.lower() == 'n':
    print("This script is not suited for varying runtimes. Sorry!")
    
else:
    print("Your input was not a valid option. Please re-run this script and type either 'y' or 'n' only.")
