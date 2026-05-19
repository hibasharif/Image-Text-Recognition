import sys
import os
import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading

# Import pytesseract and set the correct path
try:
    import pytesseract
    # IMPORTANT: Set your Tesseract path here
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\test\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    print("Please install pytesseract: pip install pytesseract")

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
        
        # Setup UI
        self.setup_ui()
        self.animate_background()
        self.check_dependencies()
    
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
                                  text="Powered by Tesseract OCR · Image Recognition",
                                  font=('Segoe UI', 11),
                                  bg=self.bg_dark,
                                  fg=self.text_dim)
        subtitle_label.pack(side=tk.LEFT, padx=(15, 0), pady=(10, 0))
        
        # Content area
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
        
        self.recognize_btn = self.create_modern_button(buttons_inner, "✨ Recognize Text", 
                                                        self.recognize_text, self.success_color)
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
    
    def check_dependencies(self):
        if not TESSERACT_AVAILABLE:
            self.results_text.insert(tk.END, "❌ pytesseract not installed!\n\nRun: pip install pytesseract\n\n")
            return
        
        # Check if Tesseract works with our path
        try:
            version = pytesseract.get_tesseract_version()
            self.results_text.insert(tk.END, f"✅ Tesseract OCR is ready! (Version {version})\n\n")
            self.results_text.insert(tk.END, "📝 How to use:\n")
            self.results_text.insert(tk.END, "1. Click 'Load Image' to select an image with text\n")
            self.results_text.insert(tk.END, "2. Click 'Recognize Text' to extract text\n")
            self.results_text.insert(tk.END, "3. Results will appear here\n\n")
            self.results_text.insert(tk.END, "💡 Tip: Use clear images with good contrast for best results!\n")
            self.status_label.config(text="OCR ready - Load an image with text")
        except Exception as e:
            self.results_text.insert(tk.END, f"⚠️ Tesseract found but error: {e}\n\n")
            self.results_text.insert(tk.END, "Check if the path is correct in the code.\n")
    
    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            self.display_image(file_path)
            self.status_label.config(text=f"Loaded: {os.path.basename(file_path)}")
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "✅ Image loaded!\nClick 'Recognize Text' to extract text.\n")
    
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
    
    def recognize_text(self):
        if not TESSERACT_AVAILABLE:
            messagebox.showerror("Error", "pytesseract not installed!\nRun: pip install pytesseract")
            return
        
        if self.current_cv_image is None:
            messagebox.showwarning("No Image", "Please load an image first.")
            return
        
        self.loading = True
        self.show_progress()
        self.recognize_btn.config(state=tk.DISABLED)
        
        thread = threading.Thread(target=self._perform_ocr)
        thread.daemon = True
        thread.start()
    
    def _perform_ocr(self):
        try:
            # Preprocess image for better OCR
            gray = cv2.cvtColor(self.current_cv_image, cv2.COLOR_BGR2GRAY)
            # Apply threshold to get black and white image
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
            # Optional: Denoise
            denoised = cv2.medianBlur(thresh, 1)
            
            # Perform OCR
            text = pytesseract.image_to_string(denoised)
            
            if text.strip():
                result = "📝 **OCR Results**\n" + "="*40 + "\n\n"
                result += text
                result += "\n\n" + "="*40 + "\n"
                word_count = len(text.split())
                char_count = len(text.strip())
                result += f"✅ Detected {word_count} words and {char_count} characters\n"
            else:
                result = "📝 **No text detected**\n\n"
                result += "Tips for better results:\n"
                result += "• Use images with clear, sharp text\n"
                result += "• Ensure good lighting and contrast\n"
                result += "• Try images with printed text (not handwritten)\n"
                result += "• Avoid blurry or low-resolution images\n"
            
            self.root.after(0, self.update_results, result)
        except Exception as e:
            error_msg = f"❌ OCR Error: {str(e)}\n\nMake sure Tesseract is properly configured."
            self.root.after(0, self.update_results, error_msg)
        finally:
            self.root.after(0, self.hide_progress)
            self.root.after(0, lambda: self.recognize_btn.config(state=tk.NORMAL))
            self.loading = False
    
    def update_results(self, text):
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, text)
        self.status_label.config(text="Recognition completed")
    
    def clear_all(self):
        self.current_cv_image = None
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