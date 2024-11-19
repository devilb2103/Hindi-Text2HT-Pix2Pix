import os
MODEL_DIR = "./Models/gen.pth.tar"

font_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "Fonts\\Amiko-Regular.ttf"))
print(font_path)
print(os.path.normpath(os.path.join(os.getcwd(), MODEL_DIR)))