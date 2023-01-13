import zipfile
from PIL import Image, ImageDraw
import pytesseract
import cv2 as cv

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')

# the rest is up to you!

images = []

def draw_contact_sheet(images):
    first_image=images[0]
    contact_sheet= Image.new(first_image.mode, (first_image.width*5,first_image.height*2))
    x=0
    y=0
    draw = ImageDraw.Draw(contact_sheet)

    for i, img in enumerate(images):
        img = img.resize((first_image.width,first_image.height), Image.LANCZOS)
        contact_sheet.paste(img, (x, y) )
        if x+first_image.width == contact_sheet.width:
            x=0
            y=y+first_image.height
        else:
            x=x+first_image.width

    contact_sheet = contact_sheet.resize((int(contact_sheet.width/2),int(contact_sheet.height/2) ))
    display(contact_sheet)
    


with zipfile.ZipFile('readonly/small_img.zip') as myzip:
    for file in myzip.namelist():
        x = myzip.extract(file)
        im=Image.open(x)        
        im = im.convert('RGB')
        im.save('readonly/small_img1.png')
        text = pytesseract.image_to_string(im)
        
        if "Christopher" in text:     
            cv_img = cv.imread('readonly/small_img1.png')
            gray = cv.cvtColor(cv_img, cv.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3,5)
            
            if len(faces) > 0:                
                print(f'Results found in file {file}')
                
                for a,b,c,d in faces:
                # Now we just need to draw our box
                    cropped = im.crop((a,b,a+c,b+d))
                    images.append(cropped)
                draw_contact_sheet(images)
                images = []
                
            else:
                print(f'''Results found in file {file}
                But there were no faces in that file!''')