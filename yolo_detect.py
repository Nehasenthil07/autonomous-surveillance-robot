import cv2
from ultralytics import YOLO
import os
import time
from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node

class YoloDetector(Node):
    def __init__(self):
        super().__init__('yolo_detector')

        # Publisher for movement
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # Load YOLO
        self.model = YOLO('yolov8n.pt')

        # Open DroidCam stream
        self.cap = cv2.VideoCapture("http://10.85.206.62:4747/video")

    def run(self):
        while rclpy.ok():
            ret, frame = self.cap.read()

            if not ret:
                print("❌ Failed to grab frame")
                break

            results = self.model(frame)
            person_detected = False

            for result in results:
                for box in result.boxes:
                    cls = int(box.cls[0])
                    label = self.model.names[cls]

                    if label == "person":
                        person_detected = True
                        print("🚨 ALERT: Human detected!")

                        # 🔊 Sound
                        os.system('play -nq -t alsa synth 0.1 sine 1000')

                        # 📸 Save image
                        filename = f"intruder_{int(time.time())}.jpg"
                        cv2.imwrite(filename, frame)

            # 🤖 Movement
            twist = Twist()
            if person_detected:
                twist.linear.x = 0.5
            else:
                twist.linear.x = 0.0

            self.cmd_pub.publish(twist)

            # Display
            annotated = results[0].plot()
            cv2.imshow("YOLO Detection", annotated)

            if cv2.waitKey(1) & 0xFF == 27:
                break

        self.cap.release()
        cv2.destroyAllWindows()


def main():
    rclpy.init()
    node = YoloDetector()
    node.run()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
