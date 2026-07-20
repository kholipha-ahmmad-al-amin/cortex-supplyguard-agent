import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT_DIR = r"D:\all my projects\coco cli compitition\web"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Try loading a nice font, fallback to default if not found
try:
    font_large = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 90)
    font_medium = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 45)
    font_small = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 30)
    logo_font = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 300)
except IOError:
    font_large = ImageFont.load_default()
    font_medium = ImageFont.load_default()
    font_small = ImageFont.load_default()
    logo_font = ImageFont.load_default()

def draw_snowflake_icon(draw, center_x, center_y, size, color):
    # Draw a stylized snowflake/network node
    import math
    for i in range(6):
        angle = math.radians(i * 60)
        end_x = center_x + size * math.cos(angle)
        end_y = center_y + size * math.sin(angle)
        draw.line([(center_x, center_y), (end_x, end_y)], fill=color, width=max(2, int(size/10)))
        
        # Branch
        b_angle1 = angle + math.radians(45)
        b_angle2 = angle - math.radians(45)
        b_dist = size * 0.5
        b_start_x = center_x + b_dist * math.cos(angle)
        b_start_y = center_y + b_dist * math.sin(angle)
        
        b_end_x1 = b_start_x + (size*0.3) * math.cos(b_angle1)
        b_end_y1 = b_start_y + (size*0.3) * math.sin(b_angle1)
        b_end_x2 = b_start_x + (size*0.3) * math.cos(b_angle2)
        b_end_y2 = b_start_y + (size*0.3) * math.sin(b_angle2)
        
        draw.line([(b_start_x, b_start_y), (b_end_x1, b_end_y1)], fill=color, width=max(2, int(size/15)))
        draw.line([(b_start_x, b_start_y), (b_end_x2, b_end_y2)], fill=color, width=max(2, int(size/15)))
    
    # Center dot
    draw.ellipse([(center_x-size/5, center_y-size/5), (center_x+size/5, center_y+size/5)], fill="#ffffff")

def generate_og_image():
    width, height = 1200, 630
    # Background gradient
    img = Image.new("RGBA", (width, height), "#0B0F19")
    draw = ImageDraw.Draw(img)
    
    # Draw a subtle radial gradient or glow
    for r in range(400, 0, -10):
        alpha = int((1 - r/400) * 50)
        draw.ellipse([(width/2 - r, height/2 - r), (width/2 + r, height/2 + r)], fill=(41, 128, 185, alpha))

    # Add decorative tech lines
    draw.line([(0, height - 100), (width, height - 100)], fill=(255, 255, 255, 30), width=2)
    draw.line([(width - 200, 0), (width - 200, height)], fill=(255, 255, 255, 30), width=2)

    # Draw icon
    draw_snowflake_icon(draw, 150, 150, 60, "#3498db")

    # Text content
    draw.text((100, 250), "Cortex SupplyGuard", fill="#ffffff", font=font_large)
    draw.text((100, 360), "Autonomous Enterprise Resilience Hub", fill="#8bb9fe", font=font_medium)
    draw.text((100, 480), "Powered by Snowflake CoCo CLI | Agentic Workflow | Real-Time Mitigation", fill="#a0aab2", font=font_small)

    # Convert to RGB to save as PNG properly without alpha issues if any
    img = img.convert("RGB")
    
    out_path = os.path.join(OUTPUT_DIR, "og-image.png")
    img.save(out_path, quality=95)
    print(f"OG Image generated: {out_path}")

def generate_logo_and_favicon():
    # Logo
    width, height = 512, 512
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0)) # transparent background
    draw = ImageDraw.Draw(img)
    
    # Draw a circular background for logo
    draw.ellipse([(10, 10), (width-10, height-10)], fill="#0B0F19", outline="#3498db", width=15)
    
    # Draw stylized icon
    draw_snowflake_icon(draw, width/2, height/2, 160, "#3498db")
    
    logo_path = os.path.join(OUTPUT_DIR, "logo.png")
    img.save(logo_path)
    print(f"Logo generated: {logo_path}")
    
    # Favicon (scale down logo)
    icon_sizes = [(32, 32), (64, 64)]
    favicon_path = os.path.join(OUTPUT_DIR, "favicon.ico")
    img.save(favicon_path, format="ICO", sizes=icon_sizes)
    print(f"Favicon generated: {favicon_path}")

if __name__ == "__main__":
    generate_og_image()
    generate_logo_and_favicon()
