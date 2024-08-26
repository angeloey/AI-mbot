import torch
from capture import *
from mouse import *

device = 0

class Target:
    def __init__(self, x, y, w, h, cls):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.cls = cls

class FrameParser:
    def __init__(self):
        self.arch = self.get_arch()
    
    def parse(self, result):
        for frame in result:
            if frame.boxes:
                target = self.sort_targets(frame)
                if target:
                    mouse.calculateOffset(int(target.x), int(target.y))
            else:
                print("no detections")
                    
                               
               
    def sort_targets(self, frame):
        boxes_array = frame.boxes.xywh.to(self.arch)
        classes_tensor = frame.boxes.cls.to(self.arch)
        
        if not classes_tensor.numel():
            return None

        center = torch.tensor([capture.screen_x_center, capture.screen_y_center], device=self.arch)
        distances_sq = torch.sum((boxes_array[:, :2] - center) ** 2, dim=1)

        head_mask = classes_tensor == 7
        if head_mask.any():
            head_distances_sq = distances_sq[head_mask]
            nearest_head_idx = torch.argmin(head_distances_sq)
            nearest_idx = torch.nonzero(head_mask)[nearest_head_idx].item()
        else:
            return None

        target_data = boxes_array[nearest_idx, :4].cpu().numpy()
        target_class = classes_tensor[nearest_idx].item()

        return Target(*target_data, target_class)
    
    def get_arch(self):
        arch = f'cuda:{device}'
        return arch

frameParser = FrameParser()