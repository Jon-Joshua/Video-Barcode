from PIL import Image, ImageDraw
import cv2
from math import trunc
import argparse

output_x = 2000
output_y = 200

def parse_video(file):

    # OpenCV2 video object.
    video = cv2.VideoCapture(file)

    # Open CV FPS + Frame Count codes.
    CV_CAP_PROP_FPS = 5
    CV_CAP_PROP_FRAME_COUNT = 7

    frame_rate = round(video.get(CV_CAP_PROP_FPS))
    total_frames = round(video.get(CV_CAP_PROP_FRAME_COUNT))
    running_time = round(total_frames / frame_rate)

    # Format running time into HH:MM:SS
    m, s = divmod(running_time, 60)
    h, m = divmod(m, 60)

    frames_per_pixel = int(total_frames / output_x)
    total_snaps = int(total_frames / frames_per_pixel)

    print('Running time: {:d}:{:d}:{:d}'.format(trunc(h), trunc(m), trunc(s)))
    print('Framerate: {:d}'.format(frame_rate))
    print('Total Frames: {:d}'.format(total_frames))
    print('-----------------------------------')
    print('Taking a snapshot every {:d} frames for a total of {:d} snapshots'.format(frames_per_pixel, total_snaps))

    image_list = []

    # Create list of all frames that need to be grabbed.
    frame_list = create_frame_list(total_frames, frames_per_pixel)
    last_frame = frame_list[-1]

    while video.isOpened():
        for frame in frame_list:
            print(frame)

            # Set frame to next in frame list and break if not valid frame.
            video.set(1, frame)
            ret, frame = video.read()
            if ret is False:
                break

            # Create 150 x 150 thumbnail of frame so we don't use all the memory.
            cv2_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(cv2_image)
            pil_image = pil_image.convert('RGB')
            size = 150, 150
            pil_image.thumbnail(size, Image.ANTIALIAS)

            image_list.append(pil_image)

        video.release()

    print('Total of {:d} snapshots taken'.format(len(image_list)))
    return image_list


def create_frame_list(total_frames, frames_per_pixel):
    # Save all numbers that have no remainder from when divided by frames_per_pixel.
    frame_list = []
    for x in range(total_frames):
        if x % frames_per_pixel == 0:
            frame_list.append(x)
    return frame_list


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


def main(args):
    input_video = args.video
    split_list = input_video.split('\\')[-1]

    print('Starting on {}'.format(split_list))

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

    parse = argparse.ArgumentParser()
    parse.add_argument('-v', '--video', help='Video file path.')
    args = parse.parse_args()

    main(args)
