import cv2
import time

# TODO: frames per second has been commented. this is because my current solution is only incrementing and not showing expected results, will fix later

class Text:
    def __init__(self):
        self.text = None

    def set_text(self, _text):
        self.text = _text

    def draw(self, frame):
        cv2.putText(
            img=frame,
            text=self.text,
            org=(100, 100),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=4,
            color=(0, 255, 0),
            thickness=8
        )

class Camera:
    def __init__(self):

        self.frame = None
        self.reval = None
        self.exit_key = 27
        self.window_title = "[/capture : debug-mode]"
        #self.width, self.height = 1280, 720
        self.width, self.height = 1080, 1080

        #self.frame_count = 0
        #self.start = time.time()

        cv2.namedWindow(self.window_title)

        self.vc = cv2.VideoCapture(0)
        self.vc.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.vc.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        self.main()

    def main(self):

        if self.vc.isOpened():
            self.reval, self.frame = self.vc.read()
        else:
            self.reval = False

        while self.reval:

            self.reval, self.frame = self.vc.read()
            self.frame_count += 1
            self.frame = cv2.resize(self.frame, (1920, 1080), interpolation=cv2.INTER_AREA)

            #elapsed = time.time() - self.start
            #fps = self.frame_count / elapsed

            #h1 = Text()
            #h1.set_text(f"FPS : {fps:.2f}")
            #h1.draw(frame=self.frame)

            cv2.imshow(self.window_title, self.frame)

            key = cv2.waitKey(20)
            if key == 27:
                self.force_exit()
                break

    def force_exit(self):
        self.vc.release()
        cv2.destroyWindow(self.window_title)


_object = Camera()
