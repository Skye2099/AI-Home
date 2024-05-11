import dlib
import cv2

# 初始化 dlib 的人脸检测器和关键点检测器
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# 读取图像
image = cv2.imread("example.jpg")

# 将图像转换为灰度
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 使用人脸检测器检测人脸
faces = detector(gray)

# 遍历检测到的每张人脸
for face in faces:
    # 使用关键点检测器检测关键点
    landmarks = predictor(gray, face)
    
    # 遍历每个关键点，并在图像上绘制出来
    for n in range(0, 68):
        x = landmarks.part(n).x
        y = landmarks.part(n).y
        cv2.circle(image, (x, y), 1, (0, 255, 0), -1)

# 保存带有关键点的图像
cv2.imwrite("output.jpg", image)
