import skia
import os

def test_load_icon():
    current_dir = os.getcwd()
    icon_path = os.path.join(current_dir, 'neui', 'assets', 'neui.png')
    print(f"Trying to load: {icon_path}")
    
    if not os.path.exists(icon_path):
        print("File does not exist!")
        return

    try:
        data = skia.Data.MakeFromFileName(icon_path)
        print(f"Data created: {data}")
        if data.size() == 0:
            print("Data is empty!")
            return

        image = skia.Image.MakeFromEncoded(data)
        print(f"Image created: {image}")
        
        if image:
            print(f"Dimensions: {image.width()}x{image.height()}")
            w, h = image.width(), image.height()
            info = skia.ImageInfo.Make(
                w, h, 
                skia.kRGBA_8888_ColorType, 
                skia.kUnpremul_AlphaType
            )
            print(f"Methods: {dir(image)}")
            
            # Try Bitmap approach
            try:
                bitmap = skia.Bitmap()
                bitmap.allocPixels(skia.ImageInfo.MakeN32Premul(w, h))
                if image.readPixels(bitmap.info(), bitmap.getPixels(), bitmap.rowBytes(), 0, 0):
                    print("readPixels to bitmap success")
                    pixels = bitmap.tobytes()
                    print(f"Bitmap bytes length: {len(pixels)}")
                else:
                    print("readPixels to bitmap failed")
            except Exception as e:
                print(f"Bitmap approach failed: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_load_icon()
