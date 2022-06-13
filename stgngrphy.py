from PIL import Image
import json
import base64
from requests.api import post

def genData(data):
    newd = []

    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd
def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):
        pix = [value for value in imdata.__next__()[:3] +
               imdata.__next__()[:3] +
               imdata.__next__()[:3]]

        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                pix[j] -= 1
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if (pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1

        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if (pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1
            pix = tuple(pix)
            yield pix[0:3]
            yield pix[3:6]
            yield pix[6:9]


def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

def encode():
    imgbb_api_key = '9f40d0bfccaae6cbd59cf834824335c8'
    imgbb_api_url = 'https://api.imgbb.com/1/upload'

    img = input("<<Enter Image Name (image/png)>> : ")
    image = Image.open(img, 'r')

    data = input("Enter data to be encoded : ")
    if (len(data) == 0):
        raise ValueError('Data is empty')

    encode64 = base64.b64encode(data.encode())
    newimg = image.copy()
    encode_enc(newimg, encode64.decode())

    new_img_name = input("<<Enter New Image Name(with extension) : ")
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

    image_to_upload = new_img_name.encode()
    new_img_name = new_img_name.partition('.')[0]
    open_file = open(image_to_upload, 'rb')
    image_to_send = open_file.read()

    data = {
        'key': imgbb_api_key,
        'image': base64.b64encode(image_to_send),
        'name': f'injected-image_{new_img_name}'
    }

    upload_to_imgbb = post(url=imgbb_api_url, data=data)
    data = json.loads(upload_to_imgbb.text)
    print(f"Link: {data['data']['url']}")

def decode():
    img = input("<<Enter Image Name(image/png) : ")
    image = Image.open(img, 'r')

    data = ''
    imgdata = iter(image.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                  imgdata.__next__()[:3] +
                  imgdata.__next__()[:3]]

        binstr = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            og_data = base64.b64decode(data)
            return(og_data.decode())

def main():
    a = int(input("= = = = = Steganography = = = = =\n"
                  "1. Encode\n2. Decode\n"))
    if (a == 1):
        encode()

    elif (a == 2):
        print("Decoded Word :  " + decode())
    else:
        raise Exception("Enter correct input")

if __name__ == '__main__':
    main()