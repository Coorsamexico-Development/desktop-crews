from tkinter import S
from typing import List
import tensorflow as tf
import keras_cv
from PIL import Image, ImageColor, ImageDraw, ImageFont
import numpy as np
import cv2


COLORS_BOXES = colors = list(ImageColor.colormap.values())
FONT_BOX = ImageFont.load_default()
SIZE_IMAGE = (640,640)


class PredictResult:
    def __init__(self,id, name = '', total:int= 0, boxes:List[int] = [], scores:List[int] = 0):
        self.id = id
        self.name = name
        self.total = total
        self.boxes = boxes
        self.scores = scores
    


class PredictRnYolov8: 
    def __init__(self):
        pass

    def image_resize(self,image:Image):
        return image.resize(SIZE_IMAGE)
    
    def convert_image(self,image:Image):
        image = image.resize(SIZE_IMAGE)
        image_to_predict = tf.convert_to_tensor(image, dtype=tf.uint8)
        image_to_predict = tf.cast(image_to_predict, tf.float32)
        #image_to_predict = tf.io.read_file("./assets/images/20240513_100402.jpg")
        #image_to_predict = tf.image.decode_jpeg(image_to_predict, channels=3)
        
        #image_to_predict = tf.image.resize_with_pad(
        #    image_to_predict,
        #    256,
        #    256,
        #    method=tf.image.ResizeMethod.BILINEAR,
        #    antialias=False
        #)
        return image_to_predict
    
    def predict_rn(self, rn_yolov8_model:int,categories:dict[int, str], image:Image, 
                    min_score:float=0.01)-> tuple[list[PredictResult],np.ndarray] :
        image_to_predict = self.convert_image(image)

        inference_resizing = keras_cv.layers.Resizing(
            *SIZE_IMAGE, pad_to_aspect_ratio=True, bounding_box_format="xywh"
        )
        image_batch = inference_resizing([image_to_predict])

        y_pred = rn_yolov8_model.predict(image_batch)
        
        result = {key: value for key, value in y_pred.items()}

        classes = result['classes'][0]
        scores = result['confidence'][0]
        boxes = result['boxes'][0]

        total_results = len(result['classes'][0])
        
        format_results: List[PredictResult] = []
        for index in range(total_results):
            no_class = classes[index]
            if no_class < 0:
                continue
            score = scores[index]
            if score < min_score: 
                continue
            

            index_find = next((i for i, d in enumerate(format_results)
                            if d.id == no_class
                            ), None)
            if index_find is None:
                category_name = categories[no_class]
                format_results.append(PredictResult(
                    id=no_class,
                    name=category_name,
                    total=1,
                    boxes=[boxes[index]],
                    scores=[score]
                ))
            else:
                format_results[index_find].total += 1
                format_results[index_find].boxes.append(
                    boxes[index]
                )
                format_results[index_find].scores.append(
                    score
                )
        #image_numpy=image_to_predict.numpy()
        #image_numpy = tf.cast(image_numpy, tf.uint8)
        return format_results, image_to_predict.numpy()


    def draw_boxes(self,image:np.ndarray, 
                    predictions:List[PredictResult] =[],
                    max_boxes:int=1000, 
                    min_score:float=0.01):
        print("--------------Intento de dibujar los boxes ----------------")
        for i in range(len(predictions)):
            category_name = predictions[i].name
            boxes = predictions[i].boxes
            scores = predictions[i].scores
            total_boxes = len(boxes)
            # con el fin de no dibujar mas de 1000 cajas
            for index_box in range(min(total_boxes, max_boxes)):
                score = scores[index_box]
                if score >= min_score:
                    x_min, y_min, width, heigth = tuple(boxes[index_box])
                    display_str = "{}: {}%".format(category_name,
                                                int(100 * score))
                    color = COLORS_BOXES[1]
                    image_pil = Image.fromarray(np.uint8(image)).convert("RGB")
                    
                    self.__draw_bounding_box_on_image(
                        image_pil,
                        y_min,
                        x_min,
                        y_max=y_min+heigth,
                        x_max=x_min+width,
                        color=color,
                        display_str_list=[display_str])
                    
                    
                    np.copyto(image, np.array(image_pil))
            
            max_boxes -=total_boxes #restamos para que no dibuje mas de lo maximo
            
            
        return Image.fromarray(np.uint8(image)).convert("RGB")


    def __draw_bounding_box_on_image(self,image:Image,
                                y_min,
                                x_min,
                                y_max,
                                x_max,
                                color,
                                thickness=4,
                                display_str_list=[]):
        """Adds a bounding box to an image."""
        draw = ImageDraw.Draw(image)
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
        display_str_heights = [FONT_BOX.getsize(ds)[1] for ds in display_str_list]
        # Each display_str has a top and bottom margin of 0.05.
        total_display_str_height = (1.1) * sum(display_str_heights)

        if y_min > total_display_str_height:
            text_bottom = y_min
        else:
            text_bottom = y_min + total_display_str_height
            
            
        # Reverse list and print from bottom to top.
        for display_str in display_str_list[::-1]:
            text_width, text_height = FONT_BOX.getsize(display_str)
            margin = np.ceil(0.05 * text_height)

            draw.rectangle(
                            [
                            (x_min, text_bottom - text_height - 2 * margin), 
                            (x_min + text_width, text_bottom)
                            ],
                        fill=color
                        )
            draw.text((x_min + margin, text_bottom - text_height - margin),
                    display_str,
                    fill="black",
                    font=FONT_BOX)
            
            text_bottom -= text_height - 2 * margin





    def display_image(image):
        while (True):
            #opencv_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
            cv2.imshow('Prediction', image)#Mostramos el video en pantalla

            if cv2.waitKey(1) == 27:  # Cuando oprimamos "Escape" rompe el video
                break
            



