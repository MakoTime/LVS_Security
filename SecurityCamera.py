import cv2 as cv
import os

class Camera:
    def __init__(self, camera_feed=0):
        self.feedName = "{}".format(camera_feed)
        self.camera_cap = cv.VideoCapture(camera_feed)
        self.isShowing = False
        self.frame = None
        print(f"Open? {self.camera_cap.isOpened()}")
        if not self.camera_cap.isOpened():
            assert "Cannot open camera"
            self.camera_cap.release()
            exit()
            
    def update(self):
        isRunning, self.frame = self.camera_cap.read()
        
        if not isRunning:
            assert "Cannot receive frame"
            return False
        
    def display_feed(self):
        while(self.isShowing):
            self.update()
            if cv.waitKey(1) == 27:
                self.disable_feed()
                return
            cv.imshow(self.feedName, self.frame)

    def enable_feed(self):
        self.isShowing = True

    def disable_feed(self):
        self.isShowing = False
        try:
            cv.destroyWindow(self.feedName)
        except cv.error as e:
            print(f"Error {e}")
        
    def capture(self, event_type, event_time):
        self.update()
        path = os.path.dirname(os.path.realpath(__file__)) + "\\event_captures"
        assert os.path.exists(path)
        image_name = path + "\\event_{}_{}.png".format(event_type, event_time)
        print(image_name)
        print(f"Successful? {cv.imwrite(image_name, self.frame)}")
        return image_name
    
    def quit(self):
        print("Disabling feed")
        self.disable_feed()
        print("Releasing")
        self.camera_cap.release()
        print("Exiting")
        exit()

class CameraManager:
    def __init__(self, cameraFeeds=None):
        self.cameras: dict[str: Camera] = {}
        match cameraFeeds:
            case None:
                print("Defaulting to webcam 0")
                self.add_camera(0)
            case list():
                for feed in cameraFeeds:
                    self.add_camera(feed)
            case int():
                print("Accessing camera number {}".format(cameraFeeds))
                self.add_camera(cameraFeeds)
            case str():
                print("Accessing camera from {}".format(cameraFeeds))
                self.add_camera(cameraFeeds)
            case _:
                print("Invalid input type")
                return
            
    def add_camera(self, feed):
        self.cameras.update({feed : Camera(feed)})

    def remove_camera(self, feed):
        self.cameras.pop(feed)

    def getCamera(self, name = None):
        if not name:
            print("No name supplied, defaulting to first")
            return self.cameras[list(self.cameras.keys())[0]]
        return self.cameras[name]
    
    def quit_all(self):
        for camera in self.cameras.values():
            camera.quit()
    
if __name__ == "__main__":
    cameraViewer = CameraManager()
    camera0 = cameraViewer.getCamera(0)
    camera0.capture(1, "20-12-2024")