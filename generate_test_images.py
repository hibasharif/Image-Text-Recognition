import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

def create_text_test_images():
    """Create test images for OCR testing"""
    
    # Create directory for test images
    os.makedirs("test_images", exist_ok=True)
    
    # Test Image 1: Business Card Style
    img1 = Image.new('RGB', (800, 400), color='white')
    draw = ImageDraw.Draw(img1)
    
    # Try to use a nice font, fallback to default
    try:
        font_title = ImageFont.truetype("arial.ttf", 36)
        font_text = ImageFont.truetype("arial.ttf", 24)
        font_small = ImageFont.truetype("arial.ttf", 18)
    except:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Draw text
    draw.text((50, 50), "VISIONAI CORPORATION", fill='black', font=font_title)
    draw.text((50, 120), "123 AI Boulevard, Tech Valley, CA 94025", fill='gray', font=font_text)
    draw.text((50, 160), "Phone: (555) 123-4567", fill='gray', font=font_text)
    draw.text((50, 200), "Email: contact@visionai.com", fill='gray', font=font_text)
    draw.text((50, 240), "Website: www.visionai.com", fill='gray', font=font_text)
    
    img1.save("test_images/business_card.png")
    print("✅ Created: test_images/business_card.png")
    
    # Test Image 2: Menu/Restaurant Style
    img2 = Image.new('RGB', (600, 500), color='#f5f5dc')  # Beige color
    draw = ImageDraw.Draw(img2)
    
    draw.text((200, 30), "CAFE MENU", fill='brown', font=font_title)
    draw.text((50, 100), "1. Latte - $4.50", fill='black', font=font_text)
    draw.text((50, 140), "2. Cappuccino - $4.50", fill='black', font=font_text)
    draw.text((50, 180), "3. Espresso - $3.00", fill='black', font=font_text)
    draw.text((50, 220), "4. Americano - $3.50", fill='black', font=font_text)
    draw.text((50, 260), "5. Croissant - $3.00", fill='black', font=font_text)
    draw.text((50, 300), "6. Blueberry Muffin - $3.50", fill='black', font=font_text)
    
    img2.save("test_images/menu.png")
    print("✅ Created: test_images/menu.png")
    
    # Test Image 3: Quote/Inspirational
    img3 = Image.new('RGB', (800, 300), color='#e6f3ff')
    draw = ImageDraw.Draw(img3)
    
    draw.text((100, 80), "The future of AI is", fill='navy', font=font_title)
    draw.text((100, 140), "not just about intelligence,", fill='navy', font=font_title)
    draw.text((100, 200), "but about understanding.", fill='navy', font=font_title)
    draw.text((550, 260), "- VisionAI Team", fill='gray', font=font_small)
    
    img3.save("test_images/quote.png")
    print("✅ Created: test_images/quote.png")
    
    # Test Image 4: Product Labels
    img4 = Image.new('RGB', (600, 400), color='white')
    draw = ImageDraw.Draw(img4)
    
    # Draw product boxes
    draw.rectangle([50, 50, 250, 200], outline='black', width=2)
    draw.text((80, 100), "PRODUCT A", fill='red', font=font_text)
    draw.text((80, 140), "SKU: 12345", fill='black', font=font_small)
    draw.text((80, 170), "$29.99", fill='green', font=font_text)
    
    draw.rectangle([320, 50, 520, 200], outline='black', width=2)
    draw.text((350, 100), "PRODUCT B", fill='blue', font=font_text)
    draw.text((350, 140), "SKU: 67890", fill='black', font=font_small)
    draw.text((350, 170), "$49.99", fill='green', font=font_text)
    
    img4.save("test_images/products.png")
    print("✅ Created: test_images/products.png")
    
    # Test Image 5: Receipt
    img5 = Image.new('RGB', (400, 600), color='white')
    draw = ImageDraw.Draw(img5)
    
    draw.text((120, 30), "STORE #42", fill='black', font=font_text)
    draw.text((100, 60), "Date: 2024-01-15", fill='black', font=font_small)
    draw.text((100, 90), "Time: 14:30:22", fill='black', font=font_small)
    draw.line([50, 110, 350, 110], fill='black', width=1)
    
    items = [
        ("Item 1", "2", "$10.00"),
        ("Item 2", "1", "$25.00"),
        ("Item 3", "3", "$15.00"),
        ("Item 4", "1", "$5.99"),
    ]
    
    y = 130
    for item, qty, price in items:
        draw.text((50, y), f"{item}", fill='black', font=font_small)
        draw.text((250, y), f"x{qty}", fill='black', font=font_small)
        draw.text((320, y), price, fill='black', font=font_small)
        y += 30
    
    draw.line([50, y+10, 350, y+10], fill='black', width=1)
    draw.text((250, y+20), "TOTAL:", fill='black', font=font_text)
    draw.text((320, y+20), "$55.99", fill='black', font=font_text)
    
    img5.save("test_images/receipt.png")
    print("✅ Created: test_images/receipt.png")
    
    print("\n📁 All test images saved in 'test_images' folder!")
    print("Load these images in VisionAI to test OCR recognition.")

def create_object_detection_test_images():
    """Create simple images for object detection testing"""
    
    os.makedirs("test_images", exist_ok=True)
    
    # Create synthetic test images with basic shapes (for testing)
    for i in range(3):
        img = np.ones((400, 600, 3), dtype=np.uint8) * 255
        
        # Draw some shapes
        cv2.rectangle(img, (50, 50), (150, 150), (0, 255, 0), 3)
        cv2.putText(img, "Square", (60, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        
        cv2.circle(img, (300, 100), 50, (255, 0, 0), 3)
        cv2.putText(img, "Circle", (270, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        
        cv2.line(img, (450, 50), (550, 150), (0, 0, 255), 3)
        cv2.putText(img, "Line", (470, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        
        cv2.imwrite(f"test_images/shapes_{i+1}.png", img)
    
    print("✅ Created shape test images for object detection")
    
    # Create a collage with text labels
    img = np.ones((500, 800, 3), dtype=np.uint8) * 240
    
    # Add text
    cv2.putText(img, "TEST OBJECTS", (300, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)
    cv2.putText(img, "Laptop", (100, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(img, "Bottle", (100, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(img, "Book", (100, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(img, "Phone", (100, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    # Draw placeholder boxes
    cv2.rectangle(img, (300, 120), (450, 180), (0, 255, 0), 2)
    cv2.rectangle(img, (300, 220), (450, 280), (0, 255, 0), 2)
    cv2.rectangle(img, (300, 320), (450, 380), (0, 255, 0), 2)
    cv2.rectangle(img, (300, 420), (450, 480), (0, 255, 0), 2)
    
    cv2.imwrite("test_images/object_labels.png", img)
    print("✅ Created: test_images/object_labels.png")

if __name__ == "__main__":
    print("🎨 Generating test images for VisionAI...")
    print("="*50)
    
    # Create text test images
    create_text_test_images()
    
    print("\n" + "="*50)
    
    # Create object detection test images
    create_object_detection_test_images()
    
    print("\n" + "="*50)
    print("✨ All test images generated successfully!")
    print("\n📋 Instructions:")
    print("1. Open VisionAI application")
    print("2. Click 'Load Image' and select an image from 'test_images' folder")
    print("3. Select recognition mode (OCR or Object Detection)")
    print("4. Click 'Recognize'")
    print("\n🎯 Recommended test order:")
    print("   - For OCR: business_card.png, menu.png, or receipt.png")
    print("   - For Object Detection: Use real photos (YOLO works best with real objects)")