from PIL import Image, ImageDraw
import os
import sys
import getopt
import cv2
from math import trunc
from progressbarsimple import ProgressBar

output_x = 200
output_y = 20


def parse_video(file):

    image_list = []

    video = cv2.VideoCapture(file)

    CV_CAP_PROP_FPS = 5
    CV_CAP_PROP_FRAME_COUNT = 7

    frame_rate = round(video.get(CV_CAP_PROP_FPS))
    total_frames = round(video.get(CV_CAP_PROP_FRAME_COUNT))
    running_time = round(total_frames / frame_rate)

    # Format running time into HH:MM:SS
    m, s = divmod(running_time, 60)
    h, m = divmod(m, 60)

    frames_per_pixel = int(total_frames / output_x)

    print('Running time: {:d}:{:d}:{:d}'.format(trunc(h), trunc(m), trunc(s)))
    print('Framerate: %d' % (frame_rate))
    print('Total Frames: %d' % (total_frames))
    print('-----------------------------------')
    print('Taking a snapshot every %d frames' % (frames_per_pixel))

    myProgressBar = ProgressBar(nElements=30, nIterations=total_frames)

    # Parse through video and take snapshots.
    while video.isOpened():
        for x in range(total_frames):
            if x == (total_frames - 1):
                myProgressBar.finished = True
                return image_list
            if x % round(frames_per_pixel) == 0:
                # print(x)
                video.set(1, x)
                ret, frame = video.read()
                if ret is False:
                    print('fuck')
                    break
                cv2_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(cv2_image)
                pil_image = pil_image.convert('RGB')
                size = 150, 150
                pil_image.thumbnail(size, Image.ANTIALIAS)

                image_list.append(pil_image)
                myProgressBar.progress(x)
    print('Total of %d snapshots taken' % (len(image_list)))
    video.release()
    return image_list


def get_average_colour(img):

    width, height = img.size
    r_average = 0
    g_average = 0
    b_average = 0

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
        print('No file specified.')
        exit()

    input_video = argv[0]
    split_list = input_video.split('\\')[-1]

    print('Starting on ' + split_list)

    image_list = parse_video(input_video)
    colour_list = []

    im = Image.new('RGB', (output_x, output_y), (255, 255, 255, 0))

    print('Processing images')
    for image in image_list:
        colour_list.append(get_average_colour(image))

    print('Painting lines')
    image_x = 0
    for colour in colour_list:
        draw_line(im, colour, image_x)
        image_x += 1

    print('Saving image')
    print('-----------------------------------')
    im.save(split_list + ".png", "PNG")


if __name__ == "__main__":
    main(sys.argv[1:])
