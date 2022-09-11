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


def convert_pil(framebuffer):
    yuyv = np.reshape(framebuffer, ((EASYCAP_FRAME_SIZE // 4), 4))
    together = np.vstack(
        (yuyv[:, 0], yuyv[:, 1], yuyv[:, 3], yuyv[:, 2], yuyv[:, 1], yuyv[:, 3])
    ).T.reshape((480, 720 * 3))
    # deinterlace
    deinterlaced = np.zeros((480, 720 * 3), dtype="uint8")
    deinterlaced[1::2, :] = together[:240, :]
    deinterlaced[::2, :] = together[240:, :]
    im = Image.frombuffer(
        "YCbCr", (720, 480), deinterlaced.flatten(), "raw", "YCbCr", 0, 1
    ).convert("RGB")
    return im


def display_frame(im, utv):
    surface = pygame.image.fromstring(im.tobytes(), im.size, "RGB")
    screen.blit(surface, (0, 0))

    font = pygame.font.Font(None, 36)
    #font2 = pygame.font.Font(None, 20)
    text = font.render("FPS: %1.1f" % (camclock.get_fps()), 1, (190, 10, 10))
    #framenum = font2.render("Frame: %d" % (utv.frame_counter), 1, (190, 10, 10))
    #screen.blit(framenum, (10, 30))
    screen.blit(text, (10, 10))
    if record is not None:
        text = font.render("Recording", 1, (190, 10, 10))
        screen.blit(text, (590, 450))
    # print "fps", renclock.get_fps()
    pygame.display.flip()
    renclock.tick()

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
    global screen, quit_now, record, mute
    screen = pygame.display.set_mode((EASYCAP_VIDEO_WIDTH, EASYCAP_VIDEO_HEIGHT))
    pygame.display.set_caption("Fushicai EasyCAP utv007")

    with EasyCAP() as utv:
        utv.frame_handler = camclock.tick
        utv.audio_handler = handle_audio

        while not quit_now:
            im = convert_pil(utv.framebuffer)
            display_frame(im, utv)

            if record is not None and record.isOpened():
                # maybe we should use opencv/highgui instead of pygame
                imcv = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR)
                # cv2.imshow('frame', imcv)
                record.write(imcv)

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
                        im.save(filename)
                        print("Saving snapshot as %s" % filename)
                    elif event.key == pygame.K_m:
                        mute = not mute
        print("exited with")
        if record is not None:
            record.release()


if __name__ == "__main__":
    main()
