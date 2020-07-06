##
 #  @filename   :   main.cpp
 #  @brief      :   2.13inch e-paper display (B) demo
 #  @author     :   Yehui from Waveshare
 #
 #  Copyright (C) Waveshare     August 15 2017
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documnetation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to  whom the Software is
 # furished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in
 # all copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 # THE SOFTWARE.
 ##

import epd2in13b
#import Image
#import ImageFont
#import ImageDraw
#import imagedata
#import socket

import time
#import sys
#sys.path.append('/home/pi/python3DrLib')
import dr.cv as cv
import numpy as np

COLORED = 1
UNCOLORED = 0
'''
def getIP():
    myname = socket.getfqdn(socket.gethostname())
    myaddr = str(socket.gethostbyname(myname))
    print('DispatcherHTTPServer.getIP::',myaddr,myname)
    return myname,myaddr
'''
def get_frame_buffer(epd,image):
	
	width=epd.width
	height=epd.height
	buf = [0xFF] * int((width * height / 8))
	# Set buffer to value of Python Imaging Library image.
	# Image must be in mode 1.
	image=cv.flip(image,1)
	for y in range(height):
		for x in range(width):
			# Set the bits for the column of pixels at the current position.
			if image[x,y] == 0:
				buf[int((x + y * width) / 8)] &= ~(0x80 >> (x % 8))
	return buf
def main():
	epd = epd2in13b.EPD()
	epd.init()
	print('epd.init done')
	
	# clear the frame buffer
	frame_black = [0x00] * int(epd.width * epd.height / 8)
	frame_red = [0x00] * int(epd.width * epd.height / 8)
	for i in range(int(epd.width * epd.height / 16)):
		frame_black[i]=0xFF
		
		if i> int(epd.width * epd.height / 32):
			frame_black[i]=0x00
		frame_red[i]=0xFF-frame_black[i]
		#if i> int(epd.width * epd.height / 32):
		#    frame_red[i] = 0x80
	# For simplicity, the arguments are explicit numerical coordinates
	'''
	epd.draw_rectangle(frame_black, 10, 60, 50, 100, COLORED);
	epd.draw_line(frame_black, 10, 60, 50, 100, COLORED);
	epd.draw_line(frame_black, 50, 60, 10, 100, COLORED);
	epd.draw_circle(frame_black, 80, 80, 15, COLORED);
	epd.draw_filled_rectangle(frame_red, 10, 120, 50, 180, COLORED);
	epd.draw_filled_rectangle(frame_red, 0, 6, 128, 26, COLORED);
	epd.draw_filled_circle(frame_red, 80, 150, 15, COLORED);
	'''
	# write strings to the buffer
	#font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', 12)
	#epd.draw_string_at(frame_black, 4, 30, "e-Paper Demo", font, COLORED)
	#epd.draw_string_at(frame_red, 6, 10, "IP:", font, UNCOLORED)
	# display the frames
	
	#epd.display_frame(frame_black, frame_red)
	
	# display images
	#frame_black = epd.get_frame_buffer(Image.open('black.bmp'))
	#frame_red = epd.get_frame_buffer(Image.open('red.bmp'))
	#epd.display_frame(frame_black, frame_red)
	
	# You can get frame buffer from an image or import the buffer directly:
	#epd.display_frame(imagedata.IMAGE_BLACK, imagedata.IMAGE_RED)
	while True:
		# 格式化成2016-03-20 11:45:39形式
		shape=(epd.width,epd.height)
		imgB=cv.drGray(shape,255)
		imgY=cv.drGray(shape,255)
		str=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		print(str)
		imgY=cv.drPutText(imgY,str,(15,15))
		cv.putText(imgY, str, (15, 15), cv.FONT_HERSHEY_PLAIN, 1.0, (0,0,0),thickness = 2, lineType=cv.LINE_AA)
		cv.putText(imgB, str, (16, 16), cv.FONT_HERSHEY_PLAIN, 1.0, (0,0,0), lineType=cv.LINE_AA)
		#imgB=cv.imread('black.png',cv.IMREAD_GRAYSCALE)#,cv.IMREAD_GRAYSCALE
		#imgY=cv.imread('red.png',cv.IMREAD_GRAYSCALE)#,cv.IMREAD_GRAYSCALE
		outB=get_frame_buffer(epd,imgB)
		outY=get_frame_buffer(epd,imgY)
		epd.display_frame(outB, outY)
		
		
if __name__ == '__main__':
    main()
