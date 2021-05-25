import time
import datetime
import threading
from gpiozero import MotionSensor
from picamera import PiCamera


def main():

    try:

        # Start a thread to listen motion sensor and record video
        motion_thread = threading.Thread(target=motion_listener, args=())
        motion_thread.daemon = True
        motion_thread.start()

        while True:
            time.sleep(10)
            print(".")

    except KeyboardInterrupt:
        print ( "App stopped" )

def motion_listener():

    try:

        # gpio pin 27
        pir = MotionSensor(27)
        presence_detected = 0

        camera = PiCamera()
        camera.resolution = (640, 480)
        # invert the image/video in 180o 
        camera.hflip = True
        camera.vflip = True

        while True:

            # Start a preview and let the camera warm up for 2 seconds
            #camera.start_preview()
            #time.sleep(2)

            pir.wait_for_motion()
            
            presence_detected = presence_detected + 1
            current_date_and_time = datetime.datetime.now()
            path = '/home/pi/workspace/camera/'
            extension = '.h264'
            file_name = path + str(current_date_and_time) + extension
            print('Motion detected: ' + str(presence_detected) + '  |  ' + str(current_date_and_time))
                
            camera.start_recording(file_name)
            camera.wait_recording(30)
            #pir.wait_for_no_motion()
            camera.stop_recording()

    except RuntimeError:
        print('runtime error')


if __name__ == '__main__':
    print ( "Press Ctrl-C to exit" )
    main()