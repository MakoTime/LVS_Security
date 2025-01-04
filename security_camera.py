#!/usr/bin/env python
"""
File:             security_camera.py
Date:             3/01/2025
Description:      Security camera input using OpenCV
                  CameraManager ties the Camera objects neatly and allows for multiple
                  camera inputs to capture single pictures or show live feeds.
                  Each camera inherits from the threading class to allow feeds to run
                  simultaneously
"""
import threading
import cv2 as cv
import event_notifier as en

__author__ = "Benjamin Vernon-Bosley"
__copyright__ = "Livestock Visibility Solutions"

__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Benjamin Vernon-Bosley"
__email__ = "ben.vernon.bosley@gmail.com"
__status__ = "Prototype"


class Camera(threading.Thread):
    """Camera reader and displayer thread, handled by CameraManager"""
    def __init__(self, camerafeed, display_camera=False):
        threading.Thread.__init__(self)
        self.feed_name = f"{camerafeed}"
        self.camera_cap = cv.VideoCapture(camerafeed)
        self.is_showing = display_camera
        self.is_quitting = False
        self.frame = None
        if not self.camera_cap.isOpened():
            en.notify(en.SubscribedEventType.ERROR_EVENT,
                      logging_level=en.LoggingLevel.WARNING,
                      error_location=type(self).__name__,
                      description=f"Camera Unavailable")
            self.camera_cap.release()
            exit()

    def run(self):
        """Threaded loop that runs continuously, constantly reads the camera input
            and can display the camera contents if specified.
            Press Esc on a running camera window to close it permanently"""
        while(True):
            if (self.is_quitting):
                self.camera_cap.release()
                self.destroy_feed()
                return
            is_running, self.frame = self.camera_cap.read()
            try:
                assert is_running, "Camera capture is no longer running"
            except AssertionError as e:
                en.notify(en.SubscribedEventType.ERROR_EVENT,
                      logging_level=en.LoggingLevel.WARNING,
                      error_location=type(self).__name__,
                      description=e)
                return
            if self.is_showing:
                cv.imshow(self.feed_name, self.frame)
                if cv.waitKey(1) == 27:
                    self.is_showing = False
                    self.is_quitting = True

    def enable_feed(self):
        """Enables the updating of the windowed camera feed"""
        self.is_showing = True

    def disable_feed(self):
        """Disables the updating of the windowed camera feed"""
        self.is_showing = False

    def destroy_feed(self):
        """Stops the feed buffer from updating and closes the associated
            window"""
        if cv.getWindowProperty(self.feed_name, cv.WND_PROP_VISIBLE) >= 1:
            cv.destroyWindow(self.feed_name)

    def capture(self, file_path):
        """Captures the current feed to the event and time-stamped capture folder,
            even if the window isnt showing, it is still recording.
            The file name is only the name of the camera, but the folder is named after
            the event and time"""
        image_name = file_path + "\\camera-" + self.feed_name + ".png"
        try:
            assert cv.imwrite(image_name, self.frame)
        except cv.Error as e:
            en.notify(en.SubscribedEventType.ERROR_EVENT,
                      logging_level=en.LoggingLevel.ERROR,
                      error_location=type(self).__name__,
                      description=f"Unable to take capture: {e}")

    def quit(self):
        """Stops the feed, display and closes the thread"""
        self.is_quitting = True

class CameraManager:
    """Manages all the camera inputs to the system"""
    def __init__(self, cameraFeeds=None):
        """Sets up all camera(s) supplied"""
        self.cameras: dict[str: Camera] = {}
        match cameraFeeds:
            case None:
                print("Defaulting to webcam 0")
                self.add_camera(0)
            case list():
                for feed in cameraFeeds:
                    self.add_camera(feed)
            case int():
                print(f"Accessing camera number {cameraFeeds}")
                self.add_camera(cameraFeeds)
            case str():
                print(f"Accessing camera from {cameraFeeds}")
                self.add_camera(cameraFeeds)
            case _:
                print("Invalid input type")
                return

    def add_camera(self, feed):
        """Adds the camera object to the manager"""
        self.cameras.update({str(feed) : Camera(feed)})

    def remove_camera(self, feed):
        """Removes the camera object from the manager"""
        try:
            self.cameras.pop(str(feed))
        except KeyError as e:
            en.notify(en.SubscribedEventType.ERROR_EVENT,
                      logging_level=en.LoggingLevel.WARNING,
                      error_location=type(self).__name__,
                      description=f"No camera found: {e}")

    def get_camera(self, name = None):
        """Gets a camera of the specified name, if none provided, selects the first"""
        if not name:
            print("No name supplied, defaulting to first")
            try:
                return self.cameras[list(self.cameras.keys())[0]]
            except KeyError as e:
                en.notify(en.SubscribedEventType.ERROR_EVENT,
                      logging_level=en.LoggingLevel.WARNING,
                      error_location=type(self).__name__,
                      description=f"No camera found: {e}")
                return
            except IndexError as e:
                en.notify(en.SubscribedEventType.ERROR_EVENT,
                      logging_level=en.LoggingLevel.WARNING,
                      error_location=type(self).__name__,
                      description=f"No cameras available: {e}")
                return
        return self.cameras[name]

    def display_camera(self, name=None):
        """Enables/ opens up a window to display the feed of a given camera"""
        try:
            self.cameras[str(name)].enable_feed()
        except KeyError as e:
            en.notify(en.SubscribedEventType.ERROR_EVENT,
                      logging_level=en.LoggingLevel.WARNING,
                      error_location=type(self).__name__,
                      description=f"No camera found: {e}")

    def hide_camera(self, name=None):
        """Stops the display the feed of a given camera"""
        try:
            self.cameras[str(name)].is_showing = False
        except KeyError as e:
            en.notify(en.SubscribedEventType.ERROR_EVENT,
                      logging_level=en.LoggingLevel.WARNING,
                      error_location=type(self).__name__,
                      description=f"No camera found: {e}")

    def show_all_cameras(self):
        """Enables/ opens up a window to display the feed of all cameras"""
        for camera in self.cameras.values():
            camera.is_showing = True

    def hide_all_cameras(self):
        """Stops the display the feed of all cameras"""
        for camera in self.cameras.values():
            camera.is_showing = False

    def quit_all(self):
        """Closes all captures and threads of all cameras"""
        for camera in self.cameras.values():
            camera.quit()

    def capture(self, file_location, camera=None):
        """Captures images on all cameras to the given file location"""
        if not camera:
            for camera_name in self.cameras.keys():
                self.capture(file_location=file_location, camera=camera_name)
        else:
            try:
                self.cameras[str(camera)].capture(file_location)
            except KeyError as e:
                en.notify(en.SubscribedEventType.ERROR_EVENT,
                        logging_level=en.LoggingLevel.WARNING,
                        error_location=type(self).__name__,
                        description=f"No camera found: {e}")

