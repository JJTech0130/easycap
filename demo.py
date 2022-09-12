import numpy as np
from PIL import Image
import signal
from time import strftime
import pygame
import pyaudio

from easycap import *

try:
    import cv2
except:
    print("OpenCV 2 Not Available. Video can not be recorded.")

quit_now = False
screen = None
record = None
mute = False
fps = True

p = pyaudio.PyAudio()

stream = p.open(
    format=pyaudio.paInt16,
    channels=2,
    rate=44100,
    output=True,
    # If the audio output is overly staticy, try tuning this value.
    frames_per_buffer=2048,
)
renclock = pygame.time.Clock()
camclock = pygame.time.Clock()

# Converts a YUYV framebuffer into a YCbCr framebuffer
def yuyv_to_ycbcr(framebuffer):
    # Group into 4 byte chunks (-1 means "until the end")
    yuyv = np.reshape(framebuffer, (-1, 4))

    # Y1 U Y2 V
    # to
    # Y1 U V Y2 U V
    ycbcr = np.column_stack((
        (yuyv[:, 0], yuyv[:, 1], yuyv[:, 3], yuyv[:, 2], yuyv[:, 1], yuyv[:, 3])
    ))

    return ycbcr.flatten()

# Deinterlaces the framebuffer
# This is a simple "weave" deinterlacing algorithm
def deinterlace(framebuffer, size = (720, 480)):
    # It's easier to work with when it's reshaped into a 2D array
    framebuffer = np.reshape(framebuffer, (size[1], size[0] * 3))
    # Must have a second framebuffer, because we do the deinterlacing in 2 passes
    output = np.zeros((size[1], size[0] * 3), dtype="uint8")

    half_height = size[1] // 2
    half_height = 240
    
    # First 240 lines go to every other line, starting at line 1
    output[1::2, :] = framebuffer[:half_height, :]
    # Last 240 lines go to every other line, starting at line 0
    output[::2, :] = framebuffer[half_height:, :]
    
    return output.flatten()

# Converts the raw framebuffer into a PIL image
def frame(framebuffer, size = (720, 480)):
    framebuffer = yuyv_to_ycbcr(framebuffer)
    
    framebuffer = deinterlace(framebuffer, size)
    
    im = Image.frombuffer(
        "YCbCr", size, framebuffer, "raw", "YCbCr", 0, 1
    )
    im = im.convert("RGB")
    
    return im

def display_frame(im: Image.Image, mute: bool, fps: bool, fps_clock: pygame.time.Clock):
    surface = pygame.image.fromstring(im.tobytes(), im.size, im.mode)
    screen.blit(surface, (0, 0))

    if fps:
        font = pygame.font.Font(None, 36)
        text = font.render("FPS: %1.1f" % (fps_clock.get_fps()), 1, (190, 10, 10))
        screen.blit(text, (10, 10))
    if mute:
        font = pygame.font.Font(None, 20)
        mute = font.render("MUTE", 1, (190, 10, 10))
        screen.blit(mute, (10, 30))
    if record is not None:
        font = pygame.font.Font(None, 36)
        text = font.render("Recording", 1, (190, 10, 10))
        screen.blit(text, (590, 450))

    pygame.display.flip()


def handle_audio(buffer):
    global mute
    if not mute:
        stream.write(buffer)


def signal_handler(signal, frame):
    global quit_now
    quit_now = True


def main():
    signal.signal(signal.SIGINT, signal_handler)
    pygame.init()
    global screen, quit_now, record, mute, fps
    screen = pygame.display.set_mode((EASYCAP_VIDEO_WIDTH, EASYCAP_VIDEO_HEIGHT))
    pygame.display.set_caption("Fushicai EasyCAP utv007")

    with EasyCAP() as utv:
        utv.frame_handler = camclock.tick
        utv.audio_handler = handle_audio

        while not quit_now:
            display_frame(frame(utv.framebuffer), mute, fps, camclock)

            #if record is not None and record.isOpened():
            #    # maybe we should use opencv/highgui instead of pygame
            #    imcv = cv2.cvtColor(np.asarray(), cv2.COLOR_RGB2BGR)
            #    # cv2.imshow('frame', imcv)
            #    record.write(imcv)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_now = True
                    # pass
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        if record is None:
                            # http://stackoverflow.com/questions/10605163/opencv-videowriter-under-osx-producing-no-output
                            fourcc = cv2.VideoWriter.fourcc("m", "p", "4", "v")
                            # fourcc = cv2.cv.CV_FOURCC("m", "p", "4", "v")
                            filename = strftime("Recording %Y-%m-%d %H.%M.%S.mov")
                            record = cv2.VideoWriter(filename, fourcc, 20.0, (720, 480))
                        else:
                            print("finishing up the recording")
                            record.release()
                            record = None
                    elif event.key == pygame.K_SPACE:
                        screen.fill(
                            (255, 255, 255)
                        )  # flash the screen because its a snapshot
                        pygame.display.flip()
                        filename = strftime("Snapshot %Y-%m-%d %H.%M.%S.jpg")
                        #im.save(filename)
                        print("Saving snapshot as %s" % filename)
                    elif event.key == pygame.K_m:
                        mute = not mute
                    elif event.key == pygame.K_f:
                        fps = not fps
        print("exited with")
        if record is not None:
            record.release()


if __name__ == "__main__":
    main()
