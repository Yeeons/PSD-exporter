# Need to do.
## Out file location
## Process time line?

# Needs more work
## Renaming intent - Sort of done

# Done
## Add a master file doc for getting the required info from ie: jpg 600 or png 1200
## this is so that this document doesn't need to be edited.

import os

from PIL import Image
from psd_tools import PSDImage


# File namer adds width and height to name
def imageSizes( org_name, image_name, file_type, naming_ext ):
	name_width = str(image_name.size[0])
	name_height = str(image_name.size[1])
	if naming_ext == 'filler':
		image_name.save('Out folder/' + org_name + '_' + name_width + '_x_' + name_height + 'px' + file_type)
	else:
		image_name.save('Out folder/' + org_name + '_' + name_width + '_x_' + name_height + 'px' + '_' + naming_ext + file_type)
		

# Image resizer
def imageResizer(org_name, width, image_name, file_type, naming_ext):

	# Adds in a white Background to jpegs
	if file_type == '.jpg':
		bg=Image.new('RGBA',image_name.size,(255, 255, 255, 255))
		bg.paste(image_name,(0,0), image_name)
	else:
		bg = image_name 	
	
	# Scales image based on width while keeping ratio
	basewidth = width
	wpercent = (basewidth/float(bg.size[0]))
	hsize = int((float(bg.size[1])*float(wpercent)))
	img = bg.resize((basewidth,hsize), Image.LANCZOS)
	
	# Converts jpgs to RGB from RGBA
	if file_type == '.jpg':
		img = img.convert('RGB')
	elif file_type == '.png':
		pass
		
	imageSizes(org_name, img, file_type, naming_ext)
	
	
def startConverter():
	# Opens all files with in directory	
	current_path = os.getcwd()
	total = percentageDone()
	count = 0
	
	# Naming extension added to the end of the file name 
	naming_ext = "filler"
	
	for path, dirs, files in os.walk(current_path):
		for x in files:	
			name = x.split('.')
		
			if name[1] == 'psd':
				merged_image = PSDImage.load(path + '/' + x).as_PIL()
				
				# Txt file is where all info comes from for image outputs
				file = open('info.txt', 'r')
				for line in file:
					if '#' not in line:
						if '!' in line:
							naming_ext = line.replace('!', '').replace('\n', '')
							print(naming_ext)
						else:
							line_split = line.split(' ')
							image_type = '.' + line_split[0]
							width_res = int(line_split[1])
							imageResizer( name[0], width_res, merged_image, image_type, naming_ext)
				
				count = count + 1
				print(str(count) + "/" + str(total) + " files processed")
			
			else:
				pass


# Counter to let you know total
def percentageDone():
	current_path = os.getcwd()
	count = 0
	for path, dirs, files in os.walk(current_path):
		for x in files:
			if ".psd" in x:
				count = count + 1
			
	return count
	
					
startConverter()
