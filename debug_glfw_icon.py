import glfw
import skia
import os

def test_glfw_icon():
    if not glfw.init():
        print("GLFW init failed")
        return

    window = glfw.create_window(400, 300, "Icon Test", None, None)
    if not window:
        print("Window creation failed")
        glfw.terminate()
        return

    current_dir = os.getcwd()
    icon_path = os.path.join(current_dir, 'neui', 'assets', 'neui.png')
    
    try:
        image = skia.Image.MakeFromEncoded(skia.Data.MakeFromFileName(icon_path))
        if image:
            w, h = image.width(), image.height()
            bitmap = skia.Bitmap()
            bitmap.allocPixels(skia.ImageInfo.Make(
                w, h, 
                skia.kRGBA_8888_ColorType, 
                skia.kUnpremul_AlphaType
            ))
            if image.readPixels(bitmap.info(), bitmap.getPixels(), bitmap.rowBytes(), 0, 0):
                pixels = bitmap.tobytes()
                print(f"Pixels type: {type(pixels)}")
                print(f"Pixels len: {len(pixels)}")
                
                try:
                    # Try ctypes bypass
                    import ctypes
                    class GLFWimage(ctypes.Structure):
                        _fields_ = [("width", ctypes.c_int),
                                    ("height", ctypes.c_int),
                                    ("pixels", ctypes.POINTER(ctypes.c_ubyte))]

                    # Create image struct
                    img = GLFWimage()
                    img.width = w
                    img.height = h
                    # Create buffer from bytes
                    img.pixels = ctypes.cast(ctypes.create_string_buffer(pixels), ctypes.POINTER(ctypes.c_ubyte))

                    # Create array of images (size 1)
                    images_array = (GLFWimage * 1)(img)

                    # Call C function
                    # We need to find where the lib is loaded. 
                    # glfw package usually exposes 'lib' or we can load it.
                    # But glfw package uses 'glfw._glfw' or similar.
                    
                    # Check if we can access the library
                    if hasattr(glfw, 'lib'):
                        glfw.lib.glfwSetWindowIcon(window, 1, images_array)
                        print("ctypes set_window_icon success")
                    else:
                        # Try to find it
                        print(f"glfw dir: {dir(glfw)}")
                        # It might be hidden.
                        # But we can try to use the wrapper's internal lib if exposed.
                        pass

                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    print(f"ctypes approach failed: {e}")
    except Exception as e:
        print(f"Error: {e}")

    glfw.destroy_window(window)
    glfw.terminate()

if __name__ == "__main__":
    test_glfw_icon()
