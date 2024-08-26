import bettercam
import threading
import queue


left, top = (1920 - 320) // 2, (1080 - 320) // 2
right, bottom = left + 320, top + 320
region = (left, top, right, bottom)


bufferSize = 1

class Capture(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.name = "Capture"
        self.camera = bettercam.create(output_color="BGR", max_buffer_len=16)

        self.camera.start(region=region)
        self.running = True
        self.frameBuffer = queue.Queue(maxsize=bufferSize)
        self.screen_x_center = int(right - left // 2)
        self.screen_y_center = int(top - bottom // 2)

    def run(self):
        while self.running:
            frame = self.getFrame()
        if frame is not None:
            if self.frameBuffer.full():
                self.frameBuffer.get()
            self.frameBuffer.put(frame)
            
    def getFrame(self):
        return self.camera.get_latest_frame()
    
    def getBuffer(self):
        try:
            return self.frameBuffer.get(timeout=1)
        except queue.Empty:
            return None
            
    def stop(self):
        self.running = False
        self.camera.stop()
            
capture = Capture()
capture.start()