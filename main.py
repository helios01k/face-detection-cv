import cv2
import mediapipe
from random import randint

# TODO: fps has been commented. this is because my current solution is only incrementing and not showing expected results, will fix later
# TODO: no longer using cv2 for image recognition

#face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
mpf = mediapipe.solutions.face_detection
#mpe = mediapipe.solutions.
face_detection = mpf.FaceDetection(model_selection=1, min_detection_confidence=0.3)
#eye_detection =

class Redact:
    def __init__(self):
        pass

    @staticmethod
    def create_box(frame, x, y, w, h, _type, count = None):

        # TODO : further optimize the math, rn it doesnt work as intended for random boxes (COMPLETE)
        # TODO : Mahts complete. but further sorting is needed and cleanup in refactor

        # CONFIG
        padding = 25 # white box
        escape = 0.2
        r_factor = 1.2

        x1 = x
        y1 = y
        x2 = x + w
        y2 = y + h

        r_point1 = (x1, y1)
        r_point2 = (x2, y2)

        s_point1 = (x1 + padding, y1 + padding) # white bound x1
        s_point2 = (x2 - padding, y2 - padding) #  white bound x2

        match _type:
            case "REDACT":
                if not count or count == 1:
                    cv2.rectangle(
                        img=frame,
                        pt1 = r_point1,
                        pt2 = r_point2,
                        color = (0,0,0),
                        thickness = -1
                    )
                else:
                    cv2.rectangle(
                        img=frame,
                        pt1 = r_point1,
                        pt2 = r_point2,
                        color = (0,0,0),
                        thickness = -1
                    )
                    for i in range(count):
                       # TODO: The math here is not working as iW want it to; going to study this issue further tmr 25/11/25. Will comment out the problematic math for now
                       # TODO: Document the maths furhter more.

                       # ALERT - I am going to just walkthrough the maths here in case i forget about it. We pick a random size *0.1 or *r_factor (1.5)
                       # and a random position inside the expanded area around the face (clamped by escape) the expanded area lets blocks spill outside the
                       # sensory box. (tldr: pick random sdize, random place in sensory + escape regions and draw)

                       # clamp
                        max_rand_w = int(w * (1 + 2*escape))
                        max_rand_h = int(h * (1 + 2*escape))

                       # box random
                        rand_w = randint(int(w*0.1), min(int(w*r_factor), max_rand_w))
                        rand_h = randint(int(h*0.1), min(int(h*r_factor), max_rand_h))

                       # for scramble boxe(s) only if >1

                        rx1 = randint(int(x - w*escape), int(x + w - rand_w + w*escape))
                        ry1 = randint(int(y - h*escape), int(y + h - rand_h + h*escape))

                        rx2 = rx1 + rand_w
                        ry2 = ry1 + rand_h

                        cv2.rectangle(
                            img=frame,
                            pt1=(rx1, ry1),
                            pt2=(rx2, ry2),
                            color=(0,0,0),
                            thickness=-1
                        )

            case "SENSORY":
                cv2.rectangle(
                    img=frame,
                    pt1 = s_point1,
                    pt2 = s_point2,
                    color = (255, 255, 255),
                    thickness = 2
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

            heading1 = Text(default_position="TOP_LEFT")
            heading1.set_text("SCRAMBLE GOGGLES TECHNOLOGY // HELIOS (S.C.P)")

            debug1 = Text(default_position="TOP_RIGHT")
            debug1.set_text("null")

            self.reval, self.frame = self.vc.read()
            # BELOW <RESIZE FRAMES>
            self.frame = cv2.resize(self.frame, self.window_size, interpolation=cv2.INTER_AREA)

            rgb_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            results_face = face_detection.process(rgb_frame)

            #faces = face_cascade.detectMultiScale(grayscale, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))

            # TODO: Clean up older model code
            #for (x, y, w, h) in faces:
                #position_text.set_text(f"detection: {x},{y} | {w}, {h}")
                #amplify_text.set_text("placeholder for now")
            #    Redact.create_box(frame=self.frame, x=x, y=y, w=w, h=h, _type="0")

            if results_face.detections:
                for detection in results_face.detections:
                    box = detection.location_data.relative_bounding_box
                    h, w, _ = self.frame.shape

                    x = int(box.xmin * w)
                    y = int(box.ymin * h)
                    ww = int(box.width * w)
                    hh = int(box.height * h)

                    Redact.create_box(frame=self.frame, x=x, y=y, w=ww, h=hh, _type="REDACT", count=6)
                    Redact.create_box(frame=self.frame, x=x, y=y, w=ww, h=hh, _type = "SENSORY")
                    print(f"confidence : {round(detection.score[0] * 100)}%") #=> percentage of confidence
                    debug1.set_text(f"confidence score : {round(detection.score[0] * 100)}%")

            debug1.draw(self.frame)
            heading1.draw(self.frame)

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

            # TODO: BOTTOM POSITIONS ARE NOT WORKING

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
