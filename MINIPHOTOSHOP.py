import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk # This is the bridge

# Global variables
original_img = None
current_img = None

def display_in_app(img_to_show):
    global img_display
    # Convert OpenCV BGR format to RGB for Tkinter
    if len(img_to_show.shape) == 3:
        img_rgb = cv2.cvtColor(img_to_show, cv2.COLOR_BGR2RGB)
    else: # If it's already grayscale
        img_rgb = img_to_show
        
    # Resize image to fit the window nicely
    img_pil = Image.fromarray(img_rgb)
    img_pil.thumbnail((400, 400)) 
    
    img_display = ImageTk.PhotoImage(image=img_pil)
    canvas.create_image(200, 200, image=img_display)

def load_image():
    global original_img, current_img
    path = filedialog.askopenfilename()
    if path:
        original_img = cv2.imread(path)
        current_img = original_img.copy()
        display_in_app(current_img)

def apply_filter(filter_type):
    global current_img
    if original_img is None: return
    
    if filter_type == "gray":
        current_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    elif filter_type == "blur":
        current_img = cv2.GaussianBlur(original_img, (15, 15), 0)
    elif filter_type == "edge":
        current_img = cv2.Canny(original_img, 100, 200)
        
    display_in_app(current_img)

def save_image():
    if current_img is not None:
        path = filedialog.asksaveasfilename(defaultextension=".jpg")
        if path:
            cv2.imwrite(path, current_img)
            messagebox.showinfo("Saved", "Success!")

# --- UI Setup ---
root = tk.Tk()
root.title("CTM Mini Photoshop")
root.geometry("600x500") # Made it wider to fit the image

# Left Side: Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(side="left", padx=20, fill="y")

tk.Button(btn_frame, text="1. Load Image", command=load_image, bg="lightblue", width=15).pack(pady=10)
tk.Button(btn_frame, text="Grayscale", command=lambda: apply_filter("gray"), width=15).pack(pady=5)
tk.Button(btn_frame, text="Blur", command=lambda: apply_filter("blur"), width=15).pack(pady=5)
tk.Button(btn_frame, text="Edges", command=lambda: apply_filter("edge"), width=15).pack(pady=5)
tk.Button(btn_frame, text="Save Image", command=save_image, bg="lightgreen", width=15).pack(pady=20)

# Right Side: The Image Area
canvas = tk.Canvas(root, width=400, height=400, bg="gray")
canvas.pack(side="right", padx=20, pady=20)

root.mainloop()
