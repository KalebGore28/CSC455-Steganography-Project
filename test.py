from stegano import lsb

# Hide the message
secret = lsb.hide("./test.png", "Hello World")
secret.save("./test-secret.png")
print("Message hidden and image saved.")

# Reveal the message
clear_message = lsb.reveal("./test-secret.png")
print("Revealed message:", clear_message)