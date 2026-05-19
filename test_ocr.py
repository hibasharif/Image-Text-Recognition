import sys
import os
import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import urllib.request

# Try importing OCR libraries
try:
    import pytesseract
    # Set Tesseract path
    tesseract_paths = [
        r'C:\Users\test\AppData\Local\Programs\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    ]
    for path in tesseract_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            break
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

# For object detection without PyTorch - using OpenCV DNN
try:
    import cv2.dnn
    OPENCV_DNN_AVAILABLE = True
except:
    OPENCV_DNN_AVAILABLE = False

class ModernRecognizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VisionAI - Image & Text Recognition Suite")
        self.root.geometry("1400x800")
        self.root.minsize(1200, 700)
        
        # Set modern colors
        self.bg_dark = "#0f0f13"
        self.bg_card = "#1a1a2e"
        self.accent_primary = "#6c63ff"
        self.accent_secondary = "#ff6584"
        self.text_light = "#ffffff"
        self.text_dim = "#a0a0b0"
        self.success_color = "#00d26a"
        
        self.root.configure(bg=self.bg_dark)
        
        # Animation variables
        self.animation_angle = 0
        self.loading = False
        
        # Current image display
        self.current_cv_image = None
        self.current_image_path = None
        
        # Object detection model
        self.net = None
        self.classes = None
        
        # Setup UI
        self.setup_ui()
        self.animate_background()
        
        # Initialize object detection in background
        self.root.after(100, self.init_object_detection)
        self.root.after(100, self.check_dependencies)
    
    def setup_ui(self):
        main_container = tk.Frame(self.root, bg=self.bg_dark)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_container, bg=self.bg_dark)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(header_frame, 
                               text="VisionAI Recognition Suite",
                               font=('Segoe UI', 28, 'bold'),
                               bg=self.bg_dark,
                               fg=self.text_light)
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = tk.Label(header_frame,
                                  text="OCR + Object Detection · AI Powered",
                                  font=('Segoe UI', 11),
                                  bg=self.bg_dark,
                                  fg=self.text_dim)
        subtitle_label.pack(side=tk.LEFT, padx=(15, 0), pady=(10, 0))
        
        # Mode selection -放在顶部
        mode_frame = tk.Frame(main_container, bg=self.bg_dark)
        mode_frame.pack(fill=tk.X, pady=(0, 20))
        
        mode_label = tk.Label(mode_frame, text="Select Mode:", 
                             font=('Segoe UI', 12, 'bold'),
                             bg=self.bg_dark, fg=self.text_light)
        mode_label.pack(side=tk.LEFT, padx=(0, 15))
        
        self.mode_var = tk.StringVar(value="ocr")
        
        self.ocr_radio = tk.Radiobutton(mode_frame, text="📝 Text Recognition (OCR)", 
                                        variable=self.mode_var, value="ocr",
                                        bg=self.bg_dark, fg=self.text_light,
                                        selectcolor=self.bg_dark,
                                        font=('Segoe UI', 10))
        self.ocr_radio.pack(side=tk.LEFT, padx=10)
        
        self.detection_radio = tk.Radiobutton(mode_frame, text="🔍 Object Detection", 
                                              variable=self.mode_var, value="detection",
                                              bg=self.bg_dark, fg=self.text_light,
                                              selectcolor=self.bg_dark,
                                              font=('Segoe UI', 10))
        self.detection_radio.pack(side=tk.LEFT, padx=10)
        
        # Content area - two columns
        content_frame = tk.Frame(main_container, bg=self.bg_dark)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left column - Image area
        left_column = tk.Frame(content_frame, bg=self.bg_dark)
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.image_card = tk.Frame(left_column, bg=self.bg_card, relief=tk.FLAT, bd=0)
        self.image_card.pack(fill=tk.BOTH, expand=True)
        
        img_header = tk.Frame(self.image_card, bg=self.bg_card)
        img_header.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        img_title = tk.Label(img_header, text="📷 Image Input", 
                            font=('Segoe UI', 14, 'bold'),
                            bg=self.bg_card, fg=self.text_light)
        img_title.pack(side=tk.LEFT)
        
        self.image_display = tk.Label(self.image_card, 
                                      text="No image loaded\n\nClick 'Load Image' to begin",
                                      font=('Segoe UI', 12),
                                      bg=self.bg_card,
                                      fg=self.text_dim,
                                      height=20,
                                      width=50)
        self.image_display.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Right column
        right_column = tk.Frame(content_frame, bg=self.bg_dark, width=400)
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        right_column.pack_propagate(False)
        
        # Buttons card
        buttons_card = tk.Frame(right_column, bg=self.bg_card, relief=tk.FLAT, bd=0)
        buttons_card.pack(fill=tk.X, pady=(0, 15))
        
        buttons_inner = tk.Frame(buttons_card, bg=self.bg_card)
        buttons_inner.pack(padx=15, pady=15)
        
        self.load_btn = self.create_modern_button(buttons_inner, "📂 Load Image", 
                                                   self.load_image, self.accent_primary)
        self.load_btn.pack(fill=tk.X, pady=5)
        
        self.recognize_btn = self.create_modern_button(buttons_inner, "✨ Recognize", 
                                                        self.recognize, self.success_color)
        self.recognize_btn.pack(fill=tk.X, pady=5)
        
        self.clear_btn = self.create_modern_button(buttons_inner, "🗑️ Clear", 
                                                    self.clear_all, "#ff4757")
        self.clear_btn.pack(fill=tk.X, pady=5)
        
        # Results card
        results_card = tk.Frame(right_column, bg=self.bg_card, relief=tk.FLAT, bd=0)
        results_card.pack(fill=tk.BOTH, expand=True)
        
        results_header = tk.Label(results_card, text="📊 Recognition Results",
                                 font=('Segoe UI', 12, 'bold'),
                                 bg=self.bg_card, fg=self.text_light)
        results_header.pack(anchor=tk.W, padx=15, pady=(15, 10))
        
        results_frame = tk.Frame(results_card, bg=self.bg_card)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        self.results_text = tk.Text(results_frame, 
                                    bg="#0d0d1a",
                                    fg=self.text_dim,
                                    font=('Consolas', 10),
                                    wrap=tk.WORD,
                                    relief=tk.FLAT,
                                    bd=0,
                                    height=12)
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(results_frame, command=self.results_text.yview,
                                bg=self.bg_card, troughcolor=self.bg_card)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.config(yscrollcommand=scrollbar.set)
        
        self.progress = ttk.Progressbar(right_column, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(0, 15))
        self.progress.pack_forget()
        
        self.status_label = tk.Label(main_container,
                                     text="Ready - Load an image to begin",
                                     font=('Segoe UI', 9),
                                     bg=self.bg_dark,
                                     fg=self.text_dim)
        self.status_label.pack(fill=tk.X, pady=(15, 0))
    
    def create_modern_button(self, parent, text, command, color):
        btn = tk.Button(parent, text=text, command=command,
                       bg=color, fg=self.text_light,
                       font=('Segoe UI', 10, 'bold'),
                       relief=tk.FLAT, bd=0,
                       padx=15, pady=10,
                       cursor="hand2",
                       activebackground=self.accent_secondary,
                       activeforeground=self.text_light)
        
        def on_enter(e):
            btn.config(bg=self.accent_secondary)
        def on_leave(e):
            btn.config(bg=color)
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn
    
    def init_object_detection(self):
        """Initialize YOLO object detection using OpenCV DNN"""
        try:
            # Create models directory
            os.makedirs("models", exist_ok=True)
            
            # Download configuration and weights files if not exist
            config_path = "models/yolov3.cfg"
            weights_path = "models/yolov3.weights"
            classes_path = "models/coco.names"
            
            # Download class names
            if not os.path.exists(classes_path):
                self.status_label.config(text="Downloading model files...")
                urllib.request.urlretrieve(
                    "https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names",
                    classes_path
                )
            
            # Download config file
            if not os.path.exists(config_path):
                urllib.request.urlretrieve(
                    "https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg",
                    config_path
                )
            
            # Download weights (this is large, ~240MB - only if not exists)
            if not os.path.exists(weights_path):
                self.status_label.config(text="Downloading YOLO weights (240MB)... This may take a while")
                # Use a faster mirror or skip if too large
                # For now, show message to download manually
                self.results_text.insert(tk.END, "⚠️ YOLO weights not found.\n")
                self.results_text.insert(tk.END, "For object detection, please download manually:\n")
                self.results_text.insert(tk.END, "https://pjreddie.com/media/files/yolov3.weights\n")
                self.results_text.insert(tk.END, "Place in 'models/yolov3.weights'\n\n")
                self.results_text.insert(tk.END, "Or use a lightweight alternative (coming soon)\n")
                return
            
            # Load model
            self.net = cv2.dnn.readNet(weights_path, config_path)
            with open(classes_path, 'r') as f:
                self.classes = [line.strip() for line in f.readlines()]
            
            self.status_label.config(text="Object detection ready!")
            self.results_text.insert(tk.END, "✅ Object detection model loaded!\n\n")
            
        except Exception as e:
            self.results_text.insert(tk.END, f"⚠️ Object detection init: {e}\n")
            self.results_text.insert(tk.END, "Will use alternative method.\n\n")
    
    def check_dependencies(self):
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "🔧 **System Status**\n" + "="*40 + "\n\n")
        
        if TESSERACT_AVAILABLE:
            try:
                version = pytesseract.get_tesseract_version()
                self.results_text.insert(tk.END, f"✅ Tesseract OCR: Available (v{version})\n")
            except:
                self.results_text.insert(tk.END, "✅ Tesseract OCR: Installed\n")
        else:
            self.results_text.insert(tk.END, "❌ Tesseract OCR: Not installed\n")
            self.results_text.insert(tk.END, "   Run: pip install pytesseract\n")
        
        if self.net is not None:
            self.results_text.insert(tk.END, "✅ Object Detection: Ready (YOLOv3)\n")
        else:
            self.results_text.insert(tk.END, "⚠️ Object Detection: Model not loaded\n")
            self.results_text.insert(tk.END, "   Will use contour-based detection\n\n")
        
        self.results_text.insert(tk.END, "\n" + "="*40 + "\n")
        self.results_text.insert(tk.END, "📝 Ready! Load an image and select a mode.\n")
    
    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            self.current_image_path = file_path
            self.display_image(file_path)
            self.status_label.config(text=f"Loaded: {os.path.basename(file_path)}")
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "✅ Image loaded!\nClick 'Recognize' to start analysis.\n")
    
    def display_image(self, path):
        try:
            img = Image.open(path)
            img.thumbnail((600, 400))
            photo = ImageTk.PhotoImage(img)
            self.image_display.config(image=photo, text="")
            self.image_display.image = photo
            self.current_cv_image = cv2.imread(path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def recognize(self):
        if self.current_cv_image is None:
            messagebox.showwarning("No Image", "Please load an image first.")
            return
        
        mode = self.mode_var.get()
        
        self.loading = True
        self.show_progress()
        self.recognize_btn.config(state=tk.DISABLED)
        
        thread = threading.Thread(target=self._perform_recognition, args=(mode,))
        thread.daemon = True
        thread.start()
    
    def _perform_recognition(self, mode):
        if mode == "ocr":
            result = self.recognize_text()
        else:
            result = self.detect_objects()
        
        self.root.after(0, self.update_results, result)
        self.root.after(0, self.hide_progress)
        self.root.after(0, lambda: self.recognize_btn.config(state=tk.NORMAL))
        self.loading = False
    
    def recognize_text(self):
        if not TESSERACT_AVAILABLE:
            return "❌ OCR not available. Install: pip install pytesseract"
        
        try:
            # Preprocess image
            gray = cv2.cvtColor(self.current_cv_image, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
            
            # Perform OCR
            text = pytesseract.image_to_string(thresh)
            
            if text.strip():
                result = "📝 **OCR Results**\n" + "="*40 + "\n\n"
                result += text
                result += "\n\n" + "="*40 + "\n"
                result += f"✅ Detected {len(text.split())} words, {len(text.strip())} characters"
            else:
                result = "📝 No text detected.\n\nTips: Use clear images with good contrast"
            
            return result
        except Exception as e:
            return f"❌ OCR Error: {str(e)}"
    
    def detect_objects(self):
        """Simple object detection using contour analysis (no deep learning)"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(self.current_cv_image, cv2.COLOR_BGR2GRAY)
            
            # Blur and threshold
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh = cv2.threshold(blurred, 120, 255, cv2.THRESH_BINARY)
            
            # Find contours
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Filter contours by area
            min_area = 500
            detected_objects = [c for c in contours if cv2.contourArea(c) > min_area]
            
            # Draw bounding boxes on image
            result_image = self.current_cv_image.copy()
            for i, contour in enumerate(detected_objects):
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(result_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(result_image, f"Object {i+1}", (x, y-5), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Update display
            result_rgb = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(result_rgb)
            pil_img.thumbnail((600, 400))
            photo = ImageTk.PhotoImage(pil_img)
            self.root.after(0, lambda: self.update_image_display(photo))
            
            # Format results
            result = "🔍 **Object Detection Results**\n" + "="*40 + "\n\n"
            result += f"Found {len(detected_objects)} objects/regions:\n\n"
            
            for i, contour in enumerate(detected_objects[:10]):  # Show first 10
                area = cv2.contourArea(contour)
                x, y, w, h = cv2.boundingRect(contour)
                result += f"• Object {i+1}: Area={area:.0f}px, Position=({x},{y})\n"
            
            if len(detected_objects) > 10:
                result += f"\n... and {len(detected_objects)-10} more objects\n"
            
            result += "\n" + "="*40 + "\n"
            result += "💡 Note: This is contour-based detection.\n"
            result += "For AI-powered detection (YOLO), download model files.\n"
            
            return result
            
        except Exception as e:
            return f"❌ Detection Error: {str(e)}"
    
    def update_image_display(self, photo):
        self.image_display.config(image=photo)
        self.image_display.image = photo
    
    def update_results(self, text):
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, text)
        self.status_label.config(text="Recognition completed")
    
    def clear_all(self):
        self.current_cv_image = None
        self.current_image_path = None
        self.image_display.config(image="", text="No image loaded\n\nClick 'Load Image' to begin")
        self.results_text.delete(1.0, tk.END)
        self.status_label.config(text="Cleared - Ready for new image")
        self.check_dependencies()
    
    def show_progress(self):
        self.progress.pack(fill=tk.X, pady=(0, 15))
        self.progress.start(10)
    
    def hide_progress(self):
        self.progress.stop()
        self.progress.pack_forget()
    
    def animate_background(self):
        self.animation_angle = (self.animation_angle + 1) % 360
        if hasattr(self, 'status_label') and not self.loading:
            dim_intensity = int(160 + 20 * np.sin(np.radians(self.animation_angle * 2)))
            self.status_label.config(fg=f"#{dim_intensity:02x}{dim_intensity:02x}{dim_intensity+20:02x}")
        self.root.after(100, self.animate_background)

def main():
    root = tk.Tk()
    app = ModernRecognizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()