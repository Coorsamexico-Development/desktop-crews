import matplotlib.pyplot as plt
import tensorflow as tf
import keras_cv
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
import numpy as np
import cv2

CATEGORY_NAMES = {6: 'tuerca pequeña', 2: 'tornillo para madera', 1: 'lag tornillo para madera', 7: 'perno',
                  5: 'tornillo de óxido negro', 4: 'tornillo brillante', 3: 'tornillo corto para madera',
                  0: 'tornillo tirafondo largo', 8: 'tuerca grande', 10: 'tuerca mediana',
                  9: 'tuerca mediana-pequeña',
                  11: 'machine screw', 12: 'short machine screw'}

def display_image(image):
    while (True):
        #opencv_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
        cv2.imshow('Prediction', image)#Mostramos el video en pantalla

        if cv2.waitKey(1) == 27:  # Cuando oprimamos "Escape" rompe el video
            break


def predict_crews(yolo_model, image_path):
    global CATEGORY_NAMES
    image_to_predict = tf.io.read_file(image_path)
    image_to_predict = tf.image.decode_jpeg(image_to_predict, channels=3)
    image_to_predict = tf.image.resize_with_pad(
        image_to_predict,
        1920,
        1920,
        method=tf.image.ResizeMethod.BILINEAR,
        antialias=False
    )

    inference_resizing = keras_cv.layers.Resizing(
        640, 640, pad_to_aspect_ratio=True, bounding_box_format="xywh"
    )
    image_batch = inference_resizing([image_to_predict])

    y_pred = yolo_model.predict(image_batch)
    result = {key: value for key, value in y_pred.items()}

    image_to_predict = tf.image.resize(
        image_to_predict,
        [640, 640],
        method=tf.image.ResizeMethod.BILINEAR,
        preserve_aspect_ratio=False,
        antialias=False,
        name=None
    )
    classes = result['classes'][0]
    scores = result['confidence'][0]
    boxes = result['boxes'][0]
    image_with_boxes = draw_boxes(
        image_to_predict.numpy(), boxes,
        classes, scores)
    #image_with_boxes.save(image_path)
    """ with open(image_path , 'wb+') as destination:
        for chunk in img.chunks():
            destination.write(chunk) """
    total_crews = []

    total_results = len(result['classes'][0])
    for index in range(total_results):
        value = classes[index]
        if value < 0:
            continue

        index_find = next((i for i, d in enumerate(total_crews)
                           if d['id'] == value
                           ), None)
        if index_find is None:
            category_name = CATEGORY_NAMES[value]
            total_crews.append({
                'id': value,
                'name': category_name,
                'total': 1,
                'boxes': [boxes[index]],
                'scores': [scores[index]]
            })
        else:
            total_crews[index_find]['total'] += 1
            total_crews[index_find]['boxes'].append(
                boxes[index]
            )
            total_crews[index_find]['scores'].append(
                scores[index]
            )

    return total_crews, image_with_boxes, image_to_predict


def draw_bounding_box_on_image(image,
                               y_min,
                               x_min,
                               y_max,
                               x_max,
                               color,
                               font,
                               thickness=4,
                               display_str_list=()):
    """Adds a bounding box to an image."""
    draw = ImageDraw.Draw(image)

    draw.line([(x_min, y_min), (x_min, y_max), (x_max, y_max), (x_max, y_min),
               (x_min, y_min)],
              width=thickness,
              fill=color)

    # If the total height of the display strings added to the top of the bounding
    # box exceeds the top of the image, stack the strings below the bounding box
    # instead of above.
    display_str_heights = [font.getsize(ds)[1] for ds in display_str_list]
    # Each display_str has a top and bottom margin of 0.05x.
    total_display_str_height = (1 + 2 * 0.05) * sum(display_str_heights)

    if y_min > total_display_str_height:
        text_bottom = y_min
    else:
        text_bottom = y_min + total_display_str_height
    # Reverse list and print from bottom to top.
    for display_str in display_str_list[::-1]:
        text_width, text_height = font.getsize(display_str)
        margin = np.ceil(0.05 * text_height)

        draw.rectangle([(x_min, text_bottom - text_height - 2 * margin), (x_min + text_width, text_bottom)],
                       fill=color)
        draw.text((x_min + margin, text_bottom - text_height - margin),
                  display_str,
                  fill="black",
                  font=font)
        text_bottom -= text_height - 2 * margin


def draw_boxes(image, boxes, classes, scores, max_boxes=1000, min_score=0.1):
    """Overlay labeled boxes on an image with formatted scores and label names."""
    global  CATEGORY_NAMES
    colors = list(ImageColor.colormap.values())

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Regular.ttf",
                                  25)
    except IOError:
        print("Font not found, using default font.")
        font = ImageFont.load_default()
    print("--------------Intento de dibujar las cajas----------------")
    for i in range(min(len(boxes), max_boxes)):
        if scores[i] >= min_score:
            x_min, y_min, x_max, y_max = tuple(boxes[i])
            class_number = classes[i]
            display_str = "{}: {}%".format(CATEGORY_NAMES[class_number],
                                           int(100 * scores[i]))
            color = colors[1]
            image_pil = Image.fromarray(np.uint8(image)).convert("RGB")
            draw_bounding_box_on_image(
                image_pil,
                y_min,
                x_min,
                y_max,
                x_max,
                color,
                font=font,
                display_str_list=[display_str])
            np.copyto(image, np.array(image_pil))
    return Image.fromarray(np.uint8(image)).convert("RGB")



