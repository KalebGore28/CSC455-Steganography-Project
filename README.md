# CSC455-Steganography-Project

### Note: Potential Python Module

I found a potential Python module that we could use for this project. Have a look at [stegano 0.11.4](https://pypi.org/project/stegano/).

The full link: https://pypi.org/project/stegano/

### Setup Instructions

1. Ensure you have Python (Version 3 for this test) installed on your machine.
2. Install the `stegano` module using pip:
	```sh
	pip3 install stegano
	```

### Important Notes

- `stegano` doesn't support JPG files, or at least I couldn't get it to work with them.

### Running the Test

I have created a test file for you to try. Run the following command:
```sh
python3 test.py
```

You should see the following output:
```
Message hidden and image saved.
Revealed message: Hello World
```