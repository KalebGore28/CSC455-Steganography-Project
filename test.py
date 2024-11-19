import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from stegano import lsb

# Global variables
img = None
image_path = None

def select_image():
    global img, image_path
    image_path = filedialog.askopenfilename(
        title="Select an image that you would like to hide a message in",
        filetypes=[("", "*.png *.jpg *.jpeg")]
    )
    if image_path:
        load_image(image_path)

def load_image(path):
    image = Image.open(path)
    image.thumbnail((250, 250))  # Resizing the image to put on GUI
    img = ImageTk.PhotoImage(image) # Using ImageTK library to 
    img_display.config(image=img)
    img_display.image = img

def hide_message():
    if not image_path:
        messagebox.showerror("Error", "Please select an image first")
        return

    message = message_entry.get()
    if not message:
        messagebox.showerror("Error", "Please enter a message to hide")
        return

    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("", "*.png")])
    if save_path:
        try:
            secret = lsb.hide(image_path, message) # Hiding the message in the image using LSB method
            secret.save(save_path) # Saving the image file with the message hidden inside
            messagebox.showinfo("Success", "Message hidden and image saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the image: {e}")

def reveal_message():
    image_path = filedialog.askopenfilename(
        title="Select an Image File with Hidden Message",
        filetypes=[("", "*.png *.jpg *.jpeg")]
    )
    if image_path:
        try:
            revealed_message = lsb.reveal(image_path) # Extracting the message hidden in the image
            if revealed_message:
                messagebox.showinfo("Revealed Message", revealed_message)
            else:
                messagebox.showinfo("Result", "No message was hidden in the file")
        except Exception as e:
                messagebox.showinfo("Result", "No message was hidden in the file") # This error was called any time the selected file has no message

# Building the GUI
root = tk.Tk()
root.title("Steganography Project - Hide a Message Inside of an Image File using LSB Method")
root.geometry("500x500")
root.configure(bg="white")

style = ttk.Style()
style.configure("TButton", font=("Sans-serif", 10), padding=5)
style.configure("TLabel", background="white", font=("Sans-serif", 10))
style.configure("TEntry", padding=5)

ttk.Button(root, text="Select an Image", command=select_image).pack(pady=10)

img_display = ttk.Label(root)
img_display.pack(pady=10)

ttk.Label(root, text="Enter the message to hide:").pack(pady=5)
message_entry = ttk.Entry(root, width=50)
message_entry.pack(pady=5)

ttk.Button(root, text="Hide Message & Save", command=hide_message).pack(pady=10)
ttk.Button(root, text="Reveal a Message", command=reveal_message).pack(pady=10)

root.mainloop()
