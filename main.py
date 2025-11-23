import cv2

# TODO: fps has been commented. this is because my current solution is only incrementing and not showing expected results, will fix later

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

class Redact:
    def __init__(self):
        pass

    @staticmethod
    def create_box(frame, x, y, w, h, _type):

        point1 = (x, y)
        point2 = (
            x + w + 150,
            y + h + 150,
        )


        if _type == "SENSORY":
            # TODO: Sensory will show what the SCRAMBLE is detecting; implement later
            print("Will implement this later; ignore for now")
            return

        cv2.rectangle(
            img=frame,
            pt1 = point1,
            pt2 = point2,
            color = (0,0,0),
            thickness = -1
        )

class Camera:
    def __init__(self):

        self.frame = None
        self.reval = None
        self.exit_key = 27
        self.window_title = "[/capture : debug-mode]"
        #self.width, self.height = 1280, 720
        self.width, self.height = 1080, 1080

        self.window_size = (1920, 1080)

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
            # BELOW <RESIZE FRAMES>
            self.frame = cv2.resize(self.frame, self.window_size, interpolation=cv2.INTER_AREA)

            position_text = Text(default_position="TOP_LEFT")
            amplify_text = Text(default_position="BOTTOM_LEFT")

            grayscale = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(grayscale, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))

            for (x, y, w, h) in faces:
                #position_text.set_text(f"detection: {x},{y} | {w}, {h}")
                #amplify_text.set_text("placeholder for now")
                Redact.create_box(frame=self.frame, x=x, y=y, w=w, h=h, _type="0")

            position_text.draw(self.frame)
            cv2.imshow(self.window_title, self.frame)

            key = cv2.waitKey(20)
            if key == 27:
                self.force_exit()
                break

    def force_exit(self):
        self.vc.release()
        cv2.destroyWindow(self.window_title)


class Text:
    def __init__(self, default_position : str):
        self.text = None
        self.default_position = default_position

    def set_text(self, _text):
        self.text = _text

    def _getDefaultPosition(self, frame, text_w, text_h):
        h, w, _ = frame.shape  # frame height + width

        match self.default_position:
            case "TOP_LEFT":
                return 10, 10 + text_h

            case "TOP_RIGHT":
                return w - text_w - 10, 10 + text_h

            case "BOTTOM_LEFT":
                return 10, h - 10

            case "BOTTOM_RIGHT":
                return w - text_w - 10, h - 10

            case _:
                return 10, 10 + text_h

    def draw(self, frame):
        font = cv2.FONT_HERSHEY_SIMPLEX
        # this should be like fine-tuned
        # TODO: push below variables to self __init__ ?
        fontScale = 1
        thickness = 2

        (text_w, text_h), baseline = cv2.getTextSize(
            self.text, font, fontScale, thickness
        )

        org = self._getDefaultPosition(frame, text_w, text_h)

        cv2.putText(
            img=frame,
            text=self.text,
            org=org,
            fontFace=font,
            fontScale=fontScale,
            color=(0, 255, 0),
            thickness=thickness
        )


_object = Camera()
