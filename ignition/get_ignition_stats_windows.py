def get_stats():

	# Importing cannot be done at the module level or else it breaks.
	# This is because certain libraries are not thread safe. 
	# https://github.com/celery/celery/issues/2964	

	from PIL import Image
	from PIL import ImageDraw
	from PIL import ImageFont

	import glob
	import os

	import cv2
	import numpy as np
	import pandas as pd
	import matplotlib.pyplot as plt
	import csv
	import pytesseract
	from datetime import datetime

	def add_margin(pil_img, top, right, bottom, left, color):
	    width, height = pil_img.size
	    new_width = width + right + left
	    new_height = height + top + bottom
	    result = Image.new(pil_img.mode, (new_width, new_height), color)
	    result.paste(pil_img, (left, top))
	    return result

	list_of_files = glob.glob('/home/pi/screenshots/*') 
	latest_file = max(list_of_files, key=os.path.getctime)

	# latest_file = '/Users/raymondfeng/Desktop/TrickyWays/cropped/chubert.jpeg'
	  
	left = 292
	top = 364 - 2
	right = 908 + 8
	bottom = 466 - 2

	# img = canny_edge(latest_file) 
	# img = img[top:bottom, left:right] 
	# cv2.imwrite('/Users/raymondfeng/Desktop/TrickyWays/cropped/chubert_cropped.jpeg', img)
	# im = Image.open('/Users/raymondfeng/Desktop/TrickyWays/cropped/chubert_cropped.jpeg')

	im = canny_edge(latest_file)
	im = im[top:bottom, left:right]
	cv2.imwrite('/home/pi/cropped.jpeg', im)
	im = Image.open('/home/pi/cropped.jpeg')

	num_ppl = []
	num_ppl_width = 45
	left = 419
	num_rows = 5
	y_delta = im.size[1] / num_rows
	for i in range(num_rows):
		img = im.crop((left, i*y_delta,
			left+num_ppl_width, (i+1)*y_delta))
		# img = add_margin(img, 5, 0, 5, 0, (255,255,255)) # Supposedly helps the OCR
		# path_name = os.path.join('/Users/raymondfeng/Downloads/pre_ocr', 
		# 	str(datetime.now())[10:19].replace(':','_') + '_' + str(i) + '_' + 'num_ppl.png')
		path_name = os.path.join('/home/pi/pre_ocr', 
			str(datetime.now())[10:19].replace(':','_') + '_' + str(i) + '_' + 'num_ppl.png')
		img = img.resize((round(img.size[0]*10), round(img.size[1]*10)), Image.ANTIALIAS)
		img.save(path_name)
		img = cv2.imread(path_name, 0)
		thresh, img = cv2.threshold(img,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)
		img = 255 - img
		cv2.imwrite(path_name, img)
		img = Image.open(path_name)
		result = pytesseract.image_to_string(img, config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789+')
		draw = ImageDraw.Draw(img)
		font = ImageFont.truetype("/home/pi/open-sans/OpenSans-Regular.ttf", 52)
		draw.text((0, 0),str(result),(0),font=font)
		img.save(path_name)
		num_ppl.append(result)

	avg_pot = []
	avg_pot_width = 64
	left = 487
	num_rows = 5
	y_delta = im.size[1] / num_rows
	for i in range(num_rows):
		img = im.crop((left, i*y_delta,
			left+avg_pot_width, (i+1)*y_delta))
		img = add_margin(img, 5, 5, 5, 0, (0,0,0)) # Supposedly helps the OCR
		# path_name = os.path.join('/Users/raymondfeng/Downloads/pre_ocr', 
		# 	str(datetime.now())[10:19].replace(':','_') + '_' + str(i) + '_' + 'avg_pot.png')
		path_name = os.path.join('/home/pi/pre_ocr', 
			str(datetime.now())[10:19].replace(':','_') + '_' + str(i) + '_' + 'avg_pot.png')
		img = img.resize((round(img.size[0]*10), round(img.size[1]*10)), Image.ANTIALIAS)
		img.save(path_name)
		img = cv2.imread(path_name, 0)
		thresh, img = cv2.threshold(img,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)
		img = 255 - img
		cv2.imwrite(path_name, img)
		img = Image.open(path_name)
		result = pytesseract.image_to_string(img, config='--psm 10 --oem 3 -c tessedit_char_whitelist=.0123456789$')
		draw = ImageDraw.Draw(img)
		font = ImageFont.truetype("/home/pi/open-sans/OpenSans-Regular.ttf", 52)
		draw.text((0, 0),str(result),(0),font=font)
		img.save(path_name)
		avg_pot.append(result)
		if '.' not in result: result = result[:-2] + '.' + result[-2:] # TODO: This is clunky

	plrs_flop = []
	plrs_flop_width = 32
	left = 573 + 5
	num_rows = 5
	y_delta = im.size[1] / num_rows
	for i in range(num_rows):
		img = im.crop((left, i*y_delta,
			left+plrs_flop_width, (i+1)*y_delta))
		img = add_margin(img, 5, 0, 5, 0, (0,0,0)) # Supposedly helps the OCR
		# path_name = os.path.join('/Users/raymondfeng/Downloads/pre_ocr', 
		# 	str(datetime.now())[10:19].replace(':','_') + '_' + str(i) + '_' + 'plrs_flop.png')
		path_name = os.path.join('/home/pi/pre_ocr', 
			str(datetime.now())[10:19].replace(':','_') + '_' + str(i) + '_' + 'plrs_flop.png')
		img = img.resize((round(img.size[0]*12), round(img.size[1]*12)), Image.ANTIALIAS)
		img.save(path_name)
		img = cv2.imread(path_name, 0)
		# img = cv2.filter2D(img, -1, np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]]))
		# img = cv2.GaussianBlur(img, (3,3), 0)
		img = cv2.erode(img, np.ones((5,5), np.uint8), iterations=2)
		thresh, img = cv2.threshold(img,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)
		img = 255 - img
		cv2.imwrite(path_name, img)
		img = Image.open(path_name)
		result = pytesseract.image_to_string(img, config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789')
		# result = pytesseract.image_to_string(img, config='--psm 7 --oem 0 -c tessedit_char_whitelist=0123456789%')
		font = ImageFont.truetype("/home/pi/open-sans/OpenSans-Regular.ttf", 52)
		draw = ImageDraw.Draw(img)
		draw.text((0, 0),str(result),(0),font=font)
		img.save(path_name)
		plrs_flop.append(result)

	print(num_ppl, avg_pot, plrs_flop)
	return num_ppl, avg_pot, plrs_flop

def canny_edge(file_path):
	import cv2
	import numpy as np
	import math
	# https://stackoverflow.com/questions/45322630/how-to-detect-lines-in-opencv
	img = cv2.imread(file_path)
	img = img[200:-200,200:-200] # Cropping the borders

	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	kernel_size = 5
	blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)

	low_threshold = 50
	high_threshold = 150
	edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

	rho = 1  # distance resolution in pixels of the Hough grid
	theta = np.pi / 180  # angular resolution in radians of the Hough grid
	threshold = 15  # minimum number of votes (intersections in Hough grid cell)
	min_line_length = 50  # minimum number of pixels making up a line
	max_line_gap = 20  # maximum gap in pixels between connectable line segments
	line_image = np.copy(img) * 0  # creating a blank to draw lines on

	# Run Hough on edge detected image
	# Output "lines" is an array containing endpoints of detected line segments
	lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
	                    min_line_length, max_line_gap)

	top = sorted(lines, key=lambda x: x[0][1])[0] # Top is the line with smallest y coord.
	bottom = sorted(lines, key=lambda x:x[0][1])[-1] # Bottom is the line with largest y coord.
	left = sorted(lines, key=lambda x:x[0][0])[0] # Left is the line with the smallest x coord
	right = sorted(lines, key=lambda x:x[0][0])[-1] # Right is the line with the largest x coord
	borders = [top, bottom, left, right]
	for line in borders:
	    for x1,y1,x2,y2 in line:
	    	cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),5)

	top, bottom, left, right = top[0][1], bottom[0][1], left[0][0], right[0][0]
	img = img[top:bottom,left:right]
	return img

def main():
	get_stats()

if __name__ == '__main__':
	main()

