import cv2 as cv

class CameraViewer:
    def __init__(self, camera_feed=0):
        
        self.camera_cap = cv.VideoCapture(camera_feed)
        
        self.camera_cap.release()
        self.frame = None
        print(f"Open? {self.camera_cap.isOpened()}")
        if not self.camera_cap.isOpened():
            assert "Cannot open camera"
            self.camera_cap.release()
            exit()
            
    def __del__(self):
        self.camera_cap.release()
            
    def update(self):
        isRunning, frame = self.camera_cap.read()
        
        if not isRunning:
            assert "Cannot receive frame"
            return isRunning
        
    def show(self):
        cv.imshow('frame')
        
    def capture(self, event_type, event_time):
        image_name = "event_{}_{}.png".format(event_type, event_time)
        cv.imwrite(image_name, self.frame)
        return image_name