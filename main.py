#adapted from https://itnext.io/steganography-101-lsb-introduction-with-python-4c4803e08041
from PIL import Image


def main():
  print("Welcome to LSB stego! Would you like to encode or decode a message?")
  choice = input()
  if choice.lower() == "encode":  # .lower() makes the string lowercase!
    encoder()
  elif choice.lower() == "decode":
    decoder()
  else:
    print("Invalid choice.")


def encoder():
  print("Enter the name of the image you would like to encode:")
  original = input()  # input image name
  print("Enter your secret message:")
  message = input()  # your secret message
  print("What would you like to name the encoded image?")
  output = input()  # output image name
  i = 0  # counter for how many bits we've encoded

  binary = ""  # string to store the binary version of our message
  for c in message:
    binary += format(ord(c), "08b")  # format each character as 8 bit binary

  with Image.open(original) as img:
    width, height = img.size
    for y in range(height):  # loop row by row
      for x in range(width):  # for each pixel in the row
        pixel = list(img.getpixel(
            (x, y)))  # create a 3 element list: [R, G, B]
        for n in range(3):
          if (i < len(binary)):
            # bitwise AND with 11111110, bitwise OR with message bit
            # in other words: clear last bit, replace with message bit
            pixel[n] = pixel[n] & ~1 | int(binary[i])
            i += 1
        img.putpixel((x, y), tuple(pixel))  # place our pixel in the new image

    img.save(output, "PNG")  # save the new image


def decoder():
  print("Enter the name of the image you would like to decode:")
  src = input()

  binary = ""  # string to store extracted bits
  with Image.open(src) as img:
    width, height = img.size
    byte = []
    for y in range(height):  # loop row by row
      for x in range(width):  # for each pixel in the row
        pixel = list(img.getpixel(
            (x, y)))  # create a 3 element list: [R, G, B]
        for n in range(3):
          binary += str(pixel[n] & 1)  # extract the LSB from each R, G, B

  message = ""
  for i in range(0, len(binary),
                 8):  # loop through the binary list in steps of 8
    byte = binary[i:i + 8]  # get the next 8 bits
    message += chr(int(byte, 2))  # convert byte to a character, add to message

  print(message)


if __name__ == "__main__":
  main()