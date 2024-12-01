import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

# Helper functions

def gen_data(data):
    """Converts the input data (string) to binary form using ASCII value of characters."""
    new_data = [format(ord(char), '08b') for char in data]  # Convert each character to 8-bit binary
    return new_data

def modify_pixel(pix, data):
    """Modifies pixels according to the binary data to encode it."""
    datalist = gen_data(data)
    lendata = len(datalist)
    imdata = iter(pix)  # Create an iterator for the pixel data
    
    for i in range(lendata):
        # Extracting 9 pixels at a time; each pixel has 3 RGB values
        pixels = [value for value in imdata.__next__()[:3] +
                                    imdata.__next__()[:3] +
                                    imdata.__next__()[:3]]

        original_bits = [format(value, '08b') for value in pixels[:8]]
        modified_bits = []

        # Modify the first 8 pixels according to the binary data
        for j in range(8):
            bit_modified = pixels[j]
            if (datalist[i][j] == '0' and bit_modified % 2 != 0):  # If the bit is 0, make the pixel value even
                pixels[j] -= 1
            elif (datalist[i][j] == '1' and bit_modified % 2 == 0):  # If the bit is 1, make the pixel value odd
                if bit_modified != 0:
                    pixels[j] -= 1
                else:
                    pixels[j] += 1
            modified_bits.append(format(pixels[j], '08b'))

        # Print the original and modified bits for the first 8 pixels
        for orig, mod in zip(original_bits, modified_bits):
            print(f"{orig} -> {mod}")

        # Handle the 9th pixel to use it as a marker for the end of the data
        if i == lendata - 1:
            if pixels[-1] % 2 == 0:  # Ensure the last pixel is odd to indicate the end of data
                if pixels[-1] != 0:
                    pixels[-1] -= 1
                else:
                    pixels[-1] += 1
        else:
            if pixels[-1] % 2 != 0:  # Make it even if not the last bit of data
                pixels[-1] -= 1

        yield tuple(pixels[0:3])  # Return a tuple of the first three modified pixels
        yield tuple(pixels[3:6])  # Return the next three modified pixels
        yield tuple(pixels[6:9])  # Return the last three modified pixels

def encode_image(image, data):
    new_image = image.copy()  # Create a copy of the original image
    w = new_image.size[0]  # Get the width of the image
    (x, y) = (0, 0)  # Initialize the x and y coordinates

    for pixel in modify_pixel(new_image.getdata(), data):  # Modify pixels based on the data
        new_image.putpixel((x, y), pixel)  # Place the modified pixel in the new image
        if (x == w - 1):  # If the end of the width is reached, go to the next row
            x = 0
            y += 1
        else:
            x += 1  # Move to the next pixel in the row
    
    return new_image  # Return the image with encoded data

def decode_image(image):
    data = ''
    imgdata = iter(image.getdata())  # Create an iterator for the pixel data

    while True:
        pixels = [value for value in imgdata.__next__()[:3] +
                                imgdata.__next__()[:3] +
                                imgdata.__next__()[:3]]
        binstr = ''  # Initialize a string to hold a binary representation

        for i in pixels[:8]:
            if i % 2 == 0:  # Append '0' if even
                binstr += '0'
            else:  # Append '1' if odd
                binstr += '1'

        data += chr(int(binstr, 2))  # Convert binary to string character
        if pixels[-1] % 2 != 0:  # Check the 9th pixel to see if it's odd, marking the end
            return data

# GUI functions

def select_image():
    global image_path
    image_path = filedialog.askopenfilename(title="Select an image",
                                            filetypes=[("PNG files", "*.png"),
                                                       ("JPEG files", "*.jpg;*.jpeg")])
    if image_path:  # If an image is selected, load it
        load_image(image_path)

def load_image(path):
    """Loads and displays an image in the GUI."""
    image = Image.open(path)
    image.thumbnail((250, 250))  # Resize image to fit the display area
    img = ImageTk.PhotoImage(image)
    img_display.config(image=img)
    img_display.image = img  # Keep a reference to avoid garbage collection

def hide_message():
    """Encodes and saves the message entered in the GUI into the selected image."""
    if not image_path:  # If no image is selected, show error
        messagebox.showerror("Error", "Please select an image first")
        return

    message = message_entry.get()  # Get the message from the entry widget
    if not message:  # If no message is entered, show error
        messagebox.showerror("Error", "Please enter a message to hide")
        return

    try:
        image = Image.open(image_path)  # Open the selected image
        new_image = encode_image(image, message)  # Encode the message into the image
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("", "*.png")])
        if save_path:  # If a path is specified, save the new image
            new_image.save(save_path)
            messagebox.showinfo("Success", "Message hidden and image saved successfully.")
    except Exception as e:  # Handle any exception during the process
        messagebox.showerror("Error", f"An error occurred: {e}")

def reveal_message():
    """Decodes and displays the hidden message from the selected image."""
    image_path = filedialog.askopenfilename(title="Select an image with a hidden message",
                                            filetypes=[("PNG files", "*.png"),
                                                       ("JPEG files", "*.jpg;*.jpeg")])
    if image_path:  # If an image is selected, proceed to decode
        try:
            image = Image.open(image_path)  # Open the image
            hidden_message = decode_image(image)  # Decode the hidden message
            if hidden_message:
                messagebox.showinfo("Revealed Message", hidden_message)  # Show the hidden message
            else:
                messagebox.showinfo("Result", "No message was found in the file")  # No message found
        except Exception as e:  # Handle any exception during the process
            messagebox.showerror("Error", f"An error occurred: {e}")

# Building the GUI
root = tk.Tk()
root.title("Steganography - Hide and Reveal Messages")
root.geometry("500x500")
root.configure(bg="white")

style = ttk.Style()
style.configure("TButton", font=("Sans-serif", 12), padding=5)
style.configure("TLabel", background="white", font=("Sans-serif", 12))
style.configure("TEntry", padding=5)

ttk.Button(root, text="Select an Image", command=select_image).pack(pady=15)

img_display = ttk.Label(root)
img_display.pack(pady=20)

ttk.Label(root, text="Enter the message to hide:").pack(pady=10)
message_entry = ttk.Entry(root, width=60)
message_entry.pack(pady=10)

ttk.Button(root, text="Hide Message & Save", command=hide_message).pack(pady=20)
ttk.Button(root, text="Reveal a Message", command=reveal_message).pack(pady=20)

root.mainloop()
