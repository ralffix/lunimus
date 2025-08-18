# =========================
# IMPORTS
# =========================
import cv2, tkinter as tk, time, colorsys, numpy as np, pyvirtualcam
from threading import Thread

# =========================
# GLOBAL STATE
# =========================
cap = cv2.VideoCapture(0)
mode = "normal"
flash_interval = 0.1
rgb_alpha = 0.8
_flash_on = False
_last_flip = time.time()
_hue = 0.0
flip_camera = False


# =========================
# VIDEO FUNCTIONS
# =========================
def set_mode(new_mode):
    global mode, _flash_on, _last_flip
    mode = new_mode
    mode_label.config(text=f"Mode: {mode.capitalize()}")
    if new_mode == "flashbang":
        _flash_on = True
        _last_flip = time.time()

def toggle_torch(): set_mode("normal" if mode=="torch" else "torch")
def toggle_flashbang(): set_mode("normal" if mode=="flashbang" else "flashbang")
def toggle_rgb(): set_mode("normal" if mode=="rgb" else "rgb")
def update_flash_interval(val):
    global flash_interval
    flash_interval = float(val)
    flash_label.config(text=f"{flash_interval:.2f}s")
def update_rgb_alpha(val):
    global rgb_alpha
    rgb_alpha = float(val)
    rgb_label.config(text=f"{rgb_alpha:.2f}")
def quit_all():
    try: root.destroy()
    except: pass
def toggle_flip():
    global flip_camera
    flip_camera = not flip_camera
    mode_label.config(text=f"Mode: {mode.capitalize()} | Flip: {'On' if flip_camera else 'Off'}")
def rgb_overlay(frame, alpha=0.8):
    global _hue
    _hue = (_hue + 0.01) % 1.0
    r,g,b = colorsys.hsv_to_rgb(_hue,1.0,1.0)
    color_bgr = (int(b*255),int(g*255),int(r*255))
    overlay = np.full_like(frame, color_bgr, dtype=np.uint8)
    return cv2.addWeighted(overlay, alpha, frame, 1.0-alpha, 0)

def video_loop():
    global _flash_on, _last_flip
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  or 640
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 480
    fps    = int(cap.get(cv2.CAP_PROP_FPS)) or 30

    with pyvirtualcam.Camera(width=width,height=height,fps=fps,print_fps=False) as cam:
        print(f"Virtual camera started at {width}x{height} @ {fps}fps")
        while True:
            ret, frame = cap.read()
            if not ret: break
            
            # Add this:
            if flip_camera:
                frame = cv2.flip(frame, 0)  # 0 = vertical flip
            if mode=="torch": frame[:]=255
            elif mode=="flashbang":
                now=time.time()
                if now-_last_flip>=flash_interval: _flash_on=not _flash_on; _last_flip=now
                if _flash_on: frame[:]=255
            elif mode=="rgb": frame=rgb_overlay(frame, alpha=rgb_alpha)

            cv2.imshow("PrankCam Preview (press Q to quit)", frame)
            cam.send(frame[:,:,::-1])
            cam.sleep_until_next_frame()
            if cv2.waitKey(1)&0xFF==ord('q'): break

    cap.release()
    cv2.destroyAllWindows()
    quit_all()

# =========================
# GUI
# =========================
root = tk.Tk()
root.title("PrankCam")
root.resizable(False,False)

# Mode label
mode_label = tk.Label(root,text=f"Mode: {mode.capitalize()}", font=("Arial",12))
mode_label.grid(row=0,column=0,columnspan=3,pady=5)

# Torch
btn_torch = tk.Button(root,text="Toggle Torch",width=15,height=2,command=toggle_torch)
btn_torch.grid(row=1,column=0,padx=6,pady=6)

# Flashbang + interval
btn_flash = tk.Button(root,text="Toggle Flashbang",width=15,height=2,command=toggle_flashbang)
btn_flash.grid(row=2,column=0,padx=6,pady=6)
flash_spin = tk.Spinbox(root,from_=0.1,to=2.0,increment=0.1,width=5,command=lambda:update_flash_interval(flash_spin.get()))
flash_spin.delete(0,"end"); flash_spin.insert(0,str(flash_interval))
flash_spin.grid(row=2,column=1,padx=6)
flash_label = tk.Label(root,text=f"{flash_interval:.2f}s")
flash_label.grid(row=2,column=2,padx=6)

# RGB + alpha
btn_rgb = tk.Button(root,text="Toggle RGB Mode",width=15,height=2,command=toggle_rgb)
btn_rgb.grid(row=3,column=0,padx=6,pady=6)
rgb_scale = tk.Scale(root,from_=0.1,to=1.0,resolution=0.05,orient="horizontal",length=100,command=update_rgb_alpha)
rgb_scale.set(rgb_alpha)
rgb_scale.grid(row=3,column=1,padx=6)
rgb_label = tk.Label(root,text=f"{rgb_alpha:.2f}")
rgb_label.grid(row=3,column=2,padx=6)

btn_flip = tk.Button(root, text="Flip Camera", width=15, height=2, command=toggle_flip)
btn_flip.grid(row=1, column=1, padx=6, pady=6)
# Quit
btn_quit = tk.Button(root,text="Quit",width=15,height=2,command=quit_all)
btn_quit.grid(row=5,column=0,columnspan=3,pady=10)

# Start video thread
thread = Thread(target=video_loop,daemon=True)
thread.start()
root.mainloop()

