import cv2
import time
import HandTracking as htm

class Cricket:
    def __init__(self):
        self.detector = htm.handDetector(detectionCon=0.75)
        self.tipIds = [4, 8, 12, 16, 20]

    def score(self, img):
        img = self.detector.find_hands(img)
        lmList = self.detector.findPosition(img, draw=False)
        if len(lmList) != 0:
            add = 0
            if lmList[self.tipIds[0]][1] > lmList[self.tipIds[0] - 1][1]:
                add += 6
                for id in range(1, 5):
                    if lmList[self.tipIds[id]][2] < lmList[self.tipIds[id] - 2][2]:
                        add += 1
                if add == 10:
                    add = 5
            else:
                if lmList[self.tipIds[1]][2] < lmList[self.tipIds[1] - 2][2] and lmList[self.tipIds[4]][2] < lmList[self.tipIds[4] - 2][2]:
                    if lmList[self.tipIds[2]][2] < lmList[self.tipIds[2] - 2][2] and lmList[self.tipIds[3]][2] < lmList[self.tipIds[3] - 2][2]:
                        add = 4
                    else:
                        add = 10

                else:
                    for id in range(1, 5):
                        if lmList[self.tipIds[id]][2] < lmList[self.tipIds[id] - 2][2]:
                            add += 1

            return add

def main():
    wCam, hCam = 1000, 800
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    obj = Cricket()
    pTime = 0
    while True:
        success, img = cap.read()

        ans = obj.score(img)
        cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(ans), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 0), 25)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                    3, (255, 0, 0), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()