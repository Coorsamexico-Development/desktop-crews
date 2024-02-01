import matplotlib.pyplot as plt
import tensorflow as tf
import keras_cv
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
import numpy as np


def display_image(image):
    fig = plt.figure(figsize=(640, 640))
    plt.grid(False)
    plt.imshow(image)


def prodect_creews(yolo_model, image_path):
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
    category_names = {6: 'nut', 2: 'wood screw', 1: 'lag wood screw', 7: 'bolt',
                      5: 'black oxide screw', 4: 'shiny screw', 3: 'short wood screw',
                      0: 'long lag screw', 8: 'large nut', 10: 'nut', 9: 'nut',
                      11: 'machine screw', 12: 'short machine screw'}

    result = {key: value for key, value in y_pred.items()}

    image_to_predict = tf.image.resize(
        image_to_predict,
        [640, 640],
        method=tf.image.ResizeMethod.BILINEAR,
        preserve_aspect_ratio=False,
        antialias=False,
        name=None
    )
    image_with_boxes = draw_boxes(
        image_to_predict.numpy(), result["boxes"],
        result["classes"],
        category_names, result["confidence"])
    url_image = '/' + image_path
    # img = Image.fromarray(np.frombuffer(image_with_boxes, np.uint8))
    img = Image.fromarray(np.uint8(image_with_boxes)).convert("RGB")
    img.save(image_path)
    """ with open(image_path , 'wb+') as destination:
        for chunk in img.chunks():
            destination.write(chunk) """
    total_creews = {}
    classes = result['classes'][0]
    total_results = len(result['classes'][0])
    for index in range(total_results):
        value = classes[index]
        if value < 0:
            continue
        category_name = category_names[value]
        if category_name in total_creews:
            pass
        else:
            total_creews[category_name] = 0
        total_creews[category_name] = total_creews[category_name] + 1

    return {
        'result': result,
        'total_creews': total_creews
    }


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


def draw_boxes(image, boxes, classes, class_names, scores, max_boxes=1000, min_score=0.1):
    """Overlay labeled boxes on an image with formatted scores and label names."""
    colors = list(ImageColor.colormap.values())

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Regular.ttf",
                                  25)
    except IOError:
        print("Font not found, using default font.")
        font = ImageFont.load_default()
    print("--------------Intento de dibujar las cajas----------------")
    for i in range(min(boxes.shape[1], max_boxes)):
        if scores[0][i] >= min_score:
            x_min, y_min, weight, heigth = tuple(boxes[0][i])
            y_max = y_min + heigth
            x_max = x_min + weight
            class_number = classes[0][i]
            display_str = "{}: {}%".format(class_names[class_number],
                                           int(100 * scores[0][i]))
            color = colors[1]
            print(color)
            image_pil = Image.fromarray(np.uint8(image)).convert("RGB")
            draw_bounding_box_on_image(
                image_pil,
                y_min,
                x_min,
                y_max,
                x_max,
                color,
                font,
                display_str_list=[display_str])
            np.copyto(image, np.array(image_pil))
    return image
