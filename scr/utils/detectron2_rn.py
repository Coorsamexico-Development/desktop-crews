from typing import List
import os


from detectron2.engine import DefaultPredictor

from PIL import Image, ImageColor, ImageDraw, ImageFont
import numpy as np
import cv2
from torch import fill


COLORS_BOXES = colors = list(ImageColor.colormap.values())
FONT_BOX = ImageFont.load_default()
SIZE_IMAGE = (640,640)


class PredictResult:
    def __init__(self,id, name = '', 
                 total:int= 0, 
                 boxes:List[int] = [],
                 segmentations:List[int] = [], 
                 width:int=0,
                 heigth:int=0,
                 scores:List[float] = 0):
        self.id = id
        self.name = name
        self.total = total
        self.boxes = boxes
        self.scores = scores
        self.segmentations = segmentations
        self.width = width
        self.heigth = heigth
    


class PredicDetectron2: 
    def __init__(self,min_score:float=0.01):
        self.min_score = min_score
        pass

    
    def predict_rn(self, predictor:DefaultPredictor,categories:dict[int, str]
                   , image:Image)-> tuple[list[PredictResult],np.ndarray] :
        
        image = np.array(image)
        image_bgr = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        outputs =predictor(image_bgr)
        
        instances = outputs["instances"].to("cpu")
        masks = instances.pred_masks
        scores = instances.scores
        pred_classes = instances.pred_classes.tolist()
        pred_boxes = instances.pred_boxes.tensor
        height, width = image.shape[:2]
        
        format_results: List[PredictResult] = []
        
        for index in range(len(pred_classes)):
            class_id = pred_classes[index]
            if categories[class_id] is None:
                Exception("Categori not found")
                break
            
            score = scores[index]
            if score < self.min_score: 
                continue
            mask = masks[index].numpy()
            mask = np.ascontiguousarray(mask)
            contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            polygon = [contour.flatten() for contour in contours]
            polygon = [x for x in polygon if len(x) >= 4]
            #area= sum(cv2.contourArea(contour) for contour in contours)
            
            boxes = pred_boxes[index].tolist()
            
            index_find = next((i for i, d in enumerate(format_results)
                            if d.id == class_id
                            ), None)
            if index_find is None:
                category_name = categories[class_id]
                format_results.append(PredictResult(
                    id=class_id,
                    name=category_name,
                    total=1,
                    boxes=[boxes],
                    segmentations=[polygon],
                    width=width,
                    heigth=height,
                    scores=[score]
                ))
            else:
                format_results[index_find].total += 1
                format_results[index_find].boxes.append(
                    boxes
                )
                format_results[index_find].scores.append(
                    score
                )
                format_results[index_find].segmentations.append(
                    polygon
                )
        
        return format_results, image


    def draw_boxes(self,image:np.ndarray,
                    predictions:List[PredictResult] =[],
                    max_boxes:int=1000,
                    show_boxes:bool=True,
                    show_segments:bool=True,
                    ):
        
        print("--------------Intento de dibujar los boxes ----------------")
        
        image_pil = Image.fromarray(np.uint8(image)).convert("RGB")
        draw = ImageDraw.Draw(image_pil)
        color = COLORS_BOXES[20]
        for i in range(len(predictions)):
            category_name = predictions[i].name
            boxes = predictions[i].boxes
            scores = predictions[i].scores
            segmentations = predictions[i].segmentations
            
            total_boxes = len(boxes)
            # con el fin de no dibujar mas de 1000 cajas
            for index_box in range(min(total_boxes, max_boxes)):
                score = scores[index_box]
                if score >= self.min_score:
                    x_min, y_min, width, heigth = tuple(boxes[index_box])
                    display_str = "{}: {}%".format(category_name,
                                                int(100 * score))
                    
                    if show_boxes:
                        self.__draw_bounding_box_on_image(
                            draw,
                            y_min,
                            x_min,
                            y_max=heigth,
                            x_max=width,
                            color=color,
                            display_str_list=[display_str])
                    if show_segments:
                        self.__draw_bounding_segmentation_on_image(
                            draw,
                            segments=segmentations[index_box],
                            color=COLORS_BOXES[index_box+1],
                        )
                   
                    
                    
            
            max_boxes -=total_boxes #restamos para que no dibuje mas de lo maximo
        
        np.copyto(image, np.array(image_pil))
            
            
        return Image.fromarray(np.uint8(image)).convert("RGB")


    def __draw_bounding_box_on_image(self,draw:ImageDraw,
                                y_min,
                                x_min,
                                y_max,
                                x_max,
                                color,
                                thickness=4,
                                display_str_list=[]):
        """Adds a bounding box to an image."""
        
        draw.line([(x_min, y_min), 
                (x_min, y_max), 
                (x_max, y_max), 
                (x_max, y_min),
                (x_min, y_min)
                ],
                width=thickness,
                fill=color)

        # If the total height of the display strings added to the top of the bounding
        # box exceeds the top of the image, stack the strings below the bounding box
        # instead of above.
        display_str_bbox = [FONT_BOX.getbbox(ds) for ds in display_str_list]
        display_str_heights = [bbox[3] - bbox[1] for bbox in display_str_bbox]
       
        total_display_str_height = (1.1) * sum(display_str_heights)

        if y_min > total_display_str_height:
            text_bottom = y_min
        else:
            text_bottom = y_min + total_display_str_height
        # Reverse list and print from bottom to top.
        for i in range(0, len(display_str_bbox)):
            
            left, top, right, bottom = display_str_bbox[i]
            text_width = right - left
            text_height = bottom - top
            margin = np.ceil(0.05 * text_height)
            draw.rectangle(
                            [
                            (x_min, text_bottom - text_height - 2 * margin), 
                            (x_min + text_width, text_bottom)
                            ],
                        fill=color
                        )
            draw.text((x_min + margin, text_bottom - text_height - margin),
                    display_str_list[i],
                    fill="black",
                    font=FONT_BOX)
            
            text_bottom -= text_height - 2 * margin


    def __draw_bounding_segmentation_on_image(self,draw:ImageDraw,
                                segments,
                                color,
                                thickness=4,
                                ):
        """Adds a bounding polygon to an image."""
        
        for segment in segments:
            cords = segment.reshape(-1, 2)
            polygon_format = [tuple(cord) for cord in cords]
        
            draw.polygon(
                
                polygon_format
                
                ,
                    width=thickness,
                    outline=color,
            )



