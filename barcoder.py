from PIL import Image, ImageDraw
import os, sys, getopt
import cv2
import math

output_x = 4000
output_y = 400

def parse_video(file):

	image_list = []

	video = cv2.VideoCapture(file)

	frame_rate = round(video.get(5))
	total_frames = video.get(7)
	running_time = total_frames / frame_rate

	m, s = divmod(running_time, 60)
	h, m = divmod(m, 60)

	frames_per_pixel = int(total_frames / output_x)

	print 'Running time: %d:%02d:%02d' % (h, m, s)
	print 'Framerate: %d' % (frame_rate)
	print 'Total Frames: %d' % (total_frames)
	print '-----------------------------------'
	print 'Taking a snapshot every %d frames' % (frames_per_pixel)

	while video.isOpened():
		# Current frame
		frame_id = video.get(1)
		ret, frame = video.read()

		if ret == False:
			break

		if frame_id % round(frames_per_pixel) == 0:
			cv2_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			pil_image = Image.fromarray(cv2_image)
			pil_image = pil_image.convert('RGB')
			size = 150, 150
			pil_image.thumbnail(size, Image.ANTIALIAS)

			image_list.append(pil_image)

	print 'Total of %d snapshots taken' % (len(image_list))
	video.release()
	return image_list

def get_average_colour(img):

	width, height = img.size
	r_average, g_average, b_average = 0

	for x in range(0, width):
		for y in range(0, height):
			r, g, b = img.getpixel((x, y))
			r_average = (r + r_average) / 2
			g_average = (g + g_average) / 2
			b_average = (b + b_average) / 2

	return (int(r_average), int(g_average), int(b_average))

def draw_line(img, colour, x):
	draw = ImageDraw.Draw(img)
	draw.line((x, 500, x, 0), colour)

def main(argv):

	if not argv:
		print ('No file specified.')
		exit()

	input_video = argv[0]
	split_list = input_video.split('\\')[-1]
	
	print 'Starting on ' + split_list

	image_list = parse_video(input_video)
	colour_list = []

	im = Image.new('RGB', (4000, output_y), (255, 255, 255, 0)) 

	print 'Processing images'
	for image in image_list:
		colour_list.append(get_average_colour(image))

	print 'Painting lines'
	image_x = 0
	for colour in colour_list:
		draw_line(im, colour, image_x)
		image_x += 1

	print 'Saving image'
	print '-----------------------------------'
	im.save(split_list + ".png", "PNG")

if __name__ == "__main__":
    main(sys.argv[1:])