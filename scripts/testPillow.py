from PIL import Image, ImageDraw
img = Image.new(mode='RGB', size=(120, 30), color=(0, 255, 255))
draw = ImageDraw.Draw(img, mode='RGB')
# img.show()
draw.text([0,0],'python',"red")
with open("test.png", "wb") as f:
    img.save(f, format="png")