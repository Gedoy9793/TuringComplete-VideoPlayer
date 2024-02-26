from PIL import Image

width = 128
height = 96

block_x = 16
block_y = 16

frames = 594

def read_a_img(id):
    img = Image.open("../imgs/img" + str(id).zfill(len(str(frames))) + ".png")
    data = [[] for _ in range(block_y)]
    for block in range(block_y):
        for y in range(6):
            for x in range(width):
                pixel = img.getpixel((x, block * 6 + y))
                data[block].append(pixel[2])
                data[block].append(pixel[1])
                data[block].append(pixel[0])
                data[block].append(0)
    img.close()
    return data

data = [[] for _ in range(block_y)]
for i in range(frames):
    frame = read_a_img(i)
    for j in range(block_y):
        data[j] += frame[j]

for i in range(block_y):
    with open(f"data{str(i).zfill(len(str(block_y)))}.bin", "wb") as f:
        f.write(bytes(data[i]))

address = []
for line in range(6):
    for block in range(block_x - 1, -1, -1):
        for pixel in range(8):
            address += (1 << (7 - pixel + 8 * line)).to_bytes(length=6, byteorder='little', signed=False)
            address += block.to_bytes(length=2, byteorder='little', signed=False)
address[-1] = 1

with open("address.bin", "wb") as f:
    f.write(bytes(address) * frames)
