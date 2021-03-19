import PySimpleGUI as sg
from Data.Library import *
import tkinter as tk
from tkinter import filedialog
import configparser
import os
from Elevate.elevate import *

config = configparser.ConfigParser()

#theme window
sg.theme('DarkAmber')

def takeInput():
	layout = [
		[sg.Text('You and your friend must use the same password!')],
		[sg.Text('Password:'), sg.InputText()],
		[sg.Submit()]
	]

	inputBox = sg.Window("Password Entry", layout)
	event, values = inputBox.read()
	inputBox.close()

	return values[0]

def promptPlayStyle(folder):
	layout = [[sg.Text("Choose Mode")], 
			[sg.Button("Online")],
			[sg.Button("Private")]]

	# Create the window
	playstyle = sg.Window("Red Souls", layout)

	# Create an event loop
	while True:
		event, values = playstyle.read()
		# End program if user closes window or
		# presses the OK button
		if event == "OK" or event == sg.WIN_CLOSED:
			break
		elif event == "Private":
			passwd = takeInput()
			meta = getMeta(passwd)
			boot = getBoot(passwd)

			startupFN = folder+"/x64/data/"+"startup.meta"
			bootFN = folder+"/x64/"+"boot_launcher_flow.ymt"

			file = open(startupFN, 'w')
			file.write(meta)
			file.close()
			file = open(bootFN, 'w')
			file.write(boot)
			file.close()
			break
		elif event == "Online":
			try:
				startupFN = folder+"/x64/data/"+"startup.meta"
				bootFN = folder+"/x64/"+"boot_launcher_flow.ymt"
				os.remove(startupFN)
				os.remove(bootFN)
			except Exception as deleteError:
				print("Error: ", deleteError)
			break


	playstyle.close()

#################################
#
#MAIN WINDOW
#################################

elevate()

layout = [[sg.Text("RUN THIS AS ADMIN! It needs to write to your Steam Folder")], 
			[sg.Button("Okay")]]

# Create the window
starter = sg.Window("Red Souls", layout)

# Create an event loop
while True:
	event, values = starter.read()
	# End program if user closes window
	# Open a Prompt for desired Play Mode on Okay press
	if event == "Okay":
		try:
			cfgfile = open("settings.ini")
			config.read("settings.ini")
			cfgfile.close()
			file_path = config['EnvVars']['path']
		except Exception as confError:
			print("No Config Exists, Generating...")
			root = tk.Tk()
			root.withdraw()
			file_path = filedialog.askdirectory(parent=root,initialdir="/",title="Please Select RDR2 Folder")
			if file_path == "":
				raise Exception

			cfgfile = open("settings.ini",'w')

			config.add_section('EnvVars')
			config.set('EnvVars', 'path', file_path)

			config.write(cfgfile)
			cfgfile.close()
		promptPlayStyle(file_path)
		break
	elif event == sg.WIN_CLOSED:
		break

starter.close()
