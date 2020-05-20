import edgeiq
from zumi.zumi import Zumi
from zumi.util.screen import Screen
import time
import cv2
import random
import alwaysai_utils


def meander(zumi):
    screen = Screen()
    screen.look_around_open()
    command = random.randint(1, 2)
    angle = random.randint(1, 100)
    duration = random.randint(1, 3)
    print('app.py: meander: command: {}'.format(command))
    if command == 1:
        zumi.turn_left(angle, duration)
    else:
        zumi.turn_right(angle, duration)


def found_someone(zumi):
    screen = Screen()
    screen.happy()
    zumi.circle()


def main():
    zumi = Zumi()
    obj_detect = alwaysai_utils.object_detector("alwaysai/mobilenet_ssd")
    print("Loaded model:\n{}\n".format(obj_detect.model_id))
    print("Engine: {}".format(obj_detect.engine))
    print("Accelerator: {}\n".format(obj_detect.accelerator))
    print("Labels:\n{}\n".format(obj_detect.labels))

    fps = edgeiq.FPS()
    should_wait = False
    displayed_frame_size = False
    frame_center = (0, 0)
    labels = ['person']

    try:
        with edgeiq.WebcamVideoStream(cam=0) as video_stream, \
                edgeiq.Streamer() as streamer:
            # Allow Webcam to warm up
            time.sleep(2.0)
            fps.start()

            # loop detection
            while True:
                frame = video_stream.read()
                frame = edgeiq.rotate(frame, 180)
                if displayed_frame_size == False:
                    height, width, channels = frame.shape
                    print('app.py: main: frame w x h: {} x {}'.format(
                        width, height))
                    frame_center = (width/2, height/2)
                    displayed_frame_size = True

                results = obj_detect.detect_objects(frame, confidence_level=.5)
                predictions = results.predictions
                frame = edgeiq.markup_image(
                    frame, predictions, colors=obj_detect.colors)

                # Generate text to display on streamer
                text = ["Model: {}".format(obj_detect.model_id)]
                text.append(
                    "Inference time: {:1.3f} s".format(results.duration))
                text.append("Objects:")

                if labels:
                    predictions = edgeiq.filter_predictions_by_label(
                        predictions, labels)
                if len(predictions) == 0:
                    meander(zumi)
                else:
                    for prediction in predictions:
                        print('app.py: main: object detected: {}:{}'.format(
                            prediction.label, prediction.confidence))
                        text.append("{}: {:2.2f}%".format(
                            prediction.label, prediction.confidence * 100))
                        found_someone(zumi)

                streamer.send_data(frame, text)

                fps.update()

                if streamer.check_exit():
                    break

    finally:
        fps.stop()
        print("elapsed time: {:.2f}".format(fps.get_elapsed_seconds()))
        print("approx. FPS: {:.2f}".format(fps.compute_fps()))
        print("Program Ending")


if __name__ == "__main__":
    main()
