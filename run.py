from mouse import *
from capture import *
from frame_parser import *
from ultralytics import YOLO
import torch
import matplotlib.pyplot as plt
import keyboard


def detectBaddies(model, image):
    return model.predict(source=image,
        cfg="game.yaml",
        stream=True,
        iou=0.5,
        conf=0.80,
        max_det=20,
        agnostic_nms=False,
        augment=False,
        vid_stride=False,
        visualize=False,
        verbose=False,
        show_boxes=False,
        show_labels=False,
        show_conf=False,
        save=False,
        show=False)
    
    
def init():   
    try:
        model = YOLO(f"models/pytorchmodel.pt", task="detect")
    except Exception as e:
        print("Issue with model:\n", e)
        quit(0)


    while True:
        if keyboard.is_pressed("v"):
            image = capture.getFrame()
            if image is not None:
                result = detectBaddies(model, image)
                frameParser.parse(result)
            else:
                print("no image")
                
if __name__ == "__main__":
    init()