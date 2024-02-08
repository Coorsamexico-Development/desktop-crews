import tkinter as tk
from tkinter import ttk
from pathlib import Path
import cv2
import tensorflow as tf
from PIL import Image, ImageTk
from yolov8 import prodect_creews

app = tk.Tk()
app.title("Detección de Tornillos")
app.bind('<Escape>', lambda e: app.quit())
# Dimesiones Anchura x Altura
app.geometry("600x600")
app.minsize(600, 500)
app.configure(background="black")
app.attributes('-alpha', 0.8)
# tk.Wm.wm_title(app, "Title")

model_selected = tk.StringVar(app)
camara_selected = 0
entrada = tk.StringVar(app)
MODELS_TF = {}





frame_header = tk.Frame(
    app,
)
frame_header.pack(
    fill=tk.BOTH,
)
frame_form = tk.LabelFrame(
    frame_header,
    text="Configuración",
    background="blue",
    padx=5,
    pady=2,
)

frame_form.pack(
    expand=True,
    side="left",
    fill=tk.BOTH,
)

frame_camera = tk.Frame(
    frame_header,
    background="blue"
)

frame_camera.pack(
    expand=True,
    fill=tk.BOTH,
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
                               values=[],
                               textvariable=model_selected,
                               width=20,
                               font=("Arial", 12),
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


def change_camara():
    global cap
    cap.release()
    cap = cv2.VideoCapture(combobox_camara.current())# Elegimos la camara con la que vamos a hacer la deteccion
# widget model


combobox_camara = ttk.Combobox(frame_form,
                               values=[],
                               width=20,
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
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
s = ttk.Style()
s.configure(
    "MyButton.TButton",
    foreground="#ff0000",
    background="#000000",
    padding=20,
    font=("Times", 12),
    anchor="w"
)
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
    pady=10,
    row=2,
    column=1,
)

# camara widget
label_camera = tk.Label(frame_camera)
label_camera.pack(
    expand=True,
    fill=tk.BOTH,
)


table = ttk.Treeview(frame_body, columns=('tornillos', 'cant'), show='headings')
table.heading('tornillos', text="Tornillos", )
table.heading('cant', text="Cantidad" )

#inset values into a table

table.pack(
    side="left",
    fill=tk.BOTH,
    expand=True,
)

label_predict = tk.Label(frame_body, text="Image predict", width="300", height="300", borderwidth="1")
label_predict.pack(
    side="right",
    fill=tk.BOTH,
    expand=True,
)


def predict_model():
    _, frame = cap.read()
    cv2.imwrite('objeto.jpg', frame)
    total_creews, img = prodect_creews(yolo_model=MODELS_TF[model_selected.get()], image_path='objeto.jpg')

    predict_image = img.resize((300,300))
    # Convert captured image to photoimage
    predict_image = ImageTk.PhotoImage(image=predict_image)

    # Displaying photoimage in the label
    label_predict.photo_image = predict_image

    # Configure image in the label
    label_predict.configure(image=predict_image)

    for key, value in total_creews.items():
        table.insert(parent='', index=0, values=(key, value))


def load_models_keras(models):
    global MODELS_TF
    for model in models:
        model_path = model["path"]
        model_name = model["name"]
        model = tf.keras.models.load_model('model', compile=False, safe_mode=False)
        MODELS_TF[model_name] = model


def load_models():
    path = "saved_model"
    models = [{"name": f"Red Neuronal {directory.name}", "path": f"{path}/{directory.name}"} for directory in
              Path(path).iterdir() if directory.is_dir()]
    models_path = [path_model["name"] for path_model in models]
    if len(models) > 0:
        model_selected.set(models[0]["name"])
    models_combobox["values"] = models_path
    load_models_keras(models)


def capture_camera():
    _, frame = cap.read()
    # Convert image from one color space to other
    opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

    # Capture the latest frame and transform to image
    captured_image = Image.fromarray(opencv_image)
    # Convert captured image to photoimage
    photo_image = ImageTk.PhotoImage(image=captured_image)

    # Displaying photoimage in the label
    label_camera.photo_image = photo_image

    # Configure image in the label
    label_camera.configure(image=photo_image)

    # Repeat the same process after every 10 seconds
    app.after(10, capture_camera)


load_models()
capture_camera()
button_predict.config(command=predict_model)
# palabra.trace("w",lambda p:print("Hola") )

if __name__ == '__main__':
    app.mainloop()
