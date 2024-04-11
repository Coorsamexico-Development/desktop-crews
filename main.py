import tkinter as tk
from tkinter import ttk
from pathlib import Path
import cv2
import tensorflow as tf
from PIL import Image, ImageTk
from yolov8 import predict_crews, draw_boxes
import os
from filesystems import authenticate_implicit_with_adc

app = tk.Tk()
app.title("Detección de Tornillos")
app.bind('<Escape>', lambda e: app.quit())
# Dimesiones Anchura x Altura
app.geometry("800x600")
app.minsize(600, 500)
app.attributes('-alpha', 0.8)
# tk.Wm.wm_title(app, "Title")

model_selected = tk.StringVar(app)
camara_selected = 0
entrada = tk.StringVar(app)
MODELS_TF = {}
result_predict = []
image_to_predict = None

frame_header = tk.Frame(
    app,
)
frame_header.pack(
    expand=True,
    fill=tk.BOTH,
)
frame_form = tk.LabelFrame(
    frame_header,
    text="Configuración",
    padx=5,
    pady=2,
)

frame_form.pack(
    side="left",
    fill=tk.BOTH,
    expand=True,
)

frame_camera = tk.Frame(
    frame_header,
    height=128,
    width=128,
)

frame_camera.pack(
    side="left",
    fill=tk.BOTH,
    expand=True,
)

frame_body = tk.Frame(
    app,
    bg="#00a8e8",
)
frame_body.pack(
    expand=True,
    fill=tk.BOTH
)

label_model = tk.Label(frame_form, text="MODELO:", font=("Arial", 8), background="white", )
label_model.grid(
    pady=2,
    padx=10,
    row=0,
    column=0
)
# widget model
models_combobox = ttk.Combobox(frame_form,
                               values=(),
                               textvariable=model_selected,
                               width=20,
                               font=("Arial", 12),
                               state="readonly",
                               foreground="blue",
                               background="white", )
models_combobox.grid(
    pady=2,
    row=0,
    column=1
)

label_model = tk.Label(frame_form, text="CAMARA:", font=("Arial", 8), bg="white", )
label_model.grid(
    pady=2,
    padx=10,
    row=1,
    column=0,
)


def change_camara(_):
    global cap
    cap.release()
    cap = cv2.VideoCapture(combobox_camara.current())  # Elegimos la camara con la que vamos a hacer la deteccion


# widget model


combobox_camara = ttk.Combobox(frame_form,
                               values=[],
                               width=20,
                               state="readonly",
                               font=("Arial", 12),
                               foreground="blue",
                               background="white")

combobox_camara.bind("<<ComboboxSelected>>", change_camara)

combobox_camara.grid(
    pady=2,
    row=1,
    column=1,
)


def count_cameras():
    global combobox_camara
    camaras = []

    for i in range(10):
        cap = cv2.VideoCapture(i)
        if not cap.read()[0]:
            break
        camaras.append(i)
        cap.release()
    combobox_camara["values"] = [f"Camará {c}" for c in camaras]

    if len(camaras) > 0:
        combobox_camara.current(0)


count_cameras()
cap = cv2.VideoCapture(0)
width, height = 128, 128
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# widget button
button_predict = tk.Button(
    frame_form,
    text="Predecir",
    font=("Arial", 14),
    bg="#00a8e8",

    fg="white",
    justify='center'

)

button_predict.grid(
    pady=5,
    row=2,
    column=1,
)

# camara widget
label_camera = tk.Label(frame_camera, background="black", foreground="white")
label_camera.pack(
    fill=tk.BOTH,
    expand=True,
)

table = ttk.Treeview(frame_body, columns=('num', 'tornillos', 'cant'),
                     show='headings', )
table.heading('num', text="Num.", )
table.heading('tornillos', text="Tornillos", )
table.heading('cant', text="Cantidad")

label_predict = tk.Label(frame_body, text="Image predict", width="300", height="300", borderwidth="1")

# inset values into a table

table.pack(
    side="left",
    fill=tk.BOTH,
    expand=True,
)


def select_table(_):
    global result_predict
    boxes = []
    classes = []
    scores = []
    if len(table.selection()) > 0:
        for item in table.selection():
            index = table.item(item)['values'][0] - 1
            screw_class = result_predict[index]
            for j in range(len(screw_class['scores'])):
                boxes.append(screw_class['boxes'][j])
                classes.append(screw_class['id'])
                scores.append(screw_class['scores'][j])
    else:
        for index, screw_class in enumerate(result_predict):
            for j in range(len(screw_class['scores'])):
                boxes.append(screw_class['boxes'][j])
                classes.append(screw_class['id'])
                scores.append(screw_class['scores'][j])

    image_with_boxes = draw_boxes(
                    image_to_predict.numpy(), boxes,
                    classes, scores)
    predict_image = image_with_boxes.resize((300, 300))
    # Convert captured image to photoimage
    predict_image = ImageTk.PhotoImage(image=predict_image)
    label_predict.photo_image = predict_image
    label_predict.configure(image=predict_image)


table.bind("<<TreeviewSelect>>", select_table)

label_predict.pack(
    side="right",
    fill=tk.BOTH,
    expand=True,
)


def predict_model():
    global result_predict, image_to_predict
    _, frame = cap.read()
    image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'objeto.jpg')
    cv2.imwrite(image_path, frame)
    for i in table.get_children():
        table.delete(i)


    result_predict, img, image_to_predict = predict_crews(yolo_model=MODELS_TF[model_selected.get()],
                                                          image_path=image_path)

    for index, d in enumerate(result_predict):
        table.insert(parent='', index=index, values=(index+1, d['name'], d['total']))

    predict_image = img.resize((300, 300))
    # Convert captured image to photoimage
    predict_image = ImageTk.PhotoImage(image=predict_image)

    # Displaying photoimage in the label
    label_predict.photo_image = predict_image

    # Configure image in the label
    label_predict.configure(image=predict_image)


def load_models_keras(models):
    global MODELS_TF
    for model in models:
        model_path = model["path"]
        model_name = model["name"]
        model = tf.keras.models.load_model(model_path, compile=False, safe_mode=False)
        MODELS_TF[model_name] = model


def load_models():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saved_model")

    models = [{"name": f"Red Neuronal {directory.name}",
               "path": os.path.join(path, directory.name)} for directory in Path(path).iterdir() if directory.is_dir()]
    models_path = [path_model["name"] for path_model in models]

    models_combobox["values"] = models_path
    if len(models) > 0:
        model_selected.set(models[0]["name"])
        models_combobox.current(0)

    load_models_keras(models)
    capture_camera()


def capture_camera():
    global cap

    ref, frame = cap.read()
    if not ref:
        captured_image = Image.open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "image_not_available.png"))
        captured_image = captured_image.resize((128, 128))
        photo_image = ImageTk.PhotoImage(captured_image)

        # Displaying photoimage in the label
        label_camera.photo_image = photo_image

        # Configure image in the label
        label_camera.configure(image=photo_image)

        app.after(100, capture_camera)
        return
    # Convert image from one color space to other
    opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

    # Capture the latest frame and transform to image
    captured_image = Image.fromarray(opencv_image)
    captured_image = captured_image.resize((128, 128))
    # Convert captured image to photoimage
    photo_image = ImageTk.PhotoImage(captured_image, size=(128, 128))
    # label_camera.config(text=photo_image)
    # Displaying photoimage in the label
    label_camera.photo_image = photo_image

    # Configure image in the label
    label_camera.configure(image=photo_image)

    # Repeat the same process after every 10 seconds
    app.after(10, capture_camera)


app.after(10, load_models)

button_predict.config(command=predict_model)
# palabra.trace("w",lambda p:print("Hola") )
# authenticate_implicit_with_adc()

if __name__ == '__main__':
    app.mainloop()
