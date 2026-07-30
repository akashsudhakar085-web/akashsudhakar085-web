import os
import base64
from PIL import Image, ImageEnhance, ImageDraw

def generate_headers():
    headers = {
        "about": "👨‍💻 About Me",
        "experience": "💼 Experience",
        "projects": "💻 Engineering Projects",
        "skills": "⚡ Tech Stack",
        "achievements": "🏆 Achievements",
        "education": "🎓 Education",
        "contact": "📫 Contact"
    }

    os.makedirs("assets", exist_ok=True)

    for key, title in headers.items():
        svg_content = f"""<svg width="600" height="60" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#58A6FF" />
      <stop offset="50%" stop-color="#1F6FEB" />
      <stop offset="100%" stop-color="#0D1117" />
    </linearGradient>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@700&amp;display=swap');
      .title {{ font-family: 'Inter', sans-serif; font-size: 26px; font-weight: 700; fill: #c9d1d9; letter-spacing: 0.5px; }}
      .line {{
        stroke-dasharray: 400;
        stroke-dashoffset: 400;
        animation: draw 2s cubic-bezier(0.4, 0, 0.2, 1) forwards;
      }}
      @keyframes draw {{
        to {{ stroke-dashoffset: 0; }}
      }}
      .glow {{
        filter: drop-shadow(0px 0px 4px rgba(88, 166, 255, 0.4));
      }}
    </style>
  </defs>
  <text x="0" y="35" class="title glow">{title}</text>
  <rect x="0" y="48" width="400" height="2" fill="url(#grad)" class="line" />
</svg>"""
        with open(f"assets/header-{key}.svg", "w", encoding="utf-8") as f:
            f.write(svg_content)
    print("Headers generated.")

def generate_avatar():
    input_image = "assets/portrait.png"
    output_svg = "assets/premium-avatar.svg"
    
    # If the user hasn't provided portrait.jpg yet, generate a placeholder
    if not os.path.exists(input_image):
        print("portrait.jpg not found. Generating a placeholder avatar SVG.")
        base64_str = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=" # transparent pixel
    else:
        print("Processing portrait.jpg...")
        try:
            img = Image.open(input_image).convert("RGBA")
            
            # 1. Enhance
            img = ImageEnhance.Contrast(img).enhance(1.1)
            img = ImageEnhance.Sharpness(img).enhance(1.2)
            img = ImageEnhance.Color(img).enhance(1.05)
            
            # 2. Crop to Circle
            size = min(img.size)
            left = (img.size[0] - size) / 2
            top = (img.size[1] - size) / 2
            img = img.crop((left, top, left + size, top + size))
            img = img.resize((400, 400), Image.Resampling.LANCZOS)
            
            mask = Image.new("L", (400, 400), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, 400, 400), fill=255)
            
            img.putalpha(mask)
            
            # Save temporarily to base64
            img.save("temp_avatar.png", "PNG")
            with open("temp_avatar.png", "rb") as f:
                base64_str = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
            os.remove("temp_avatar.png")
            print("Image processed successfully.")
        except Exception as e:
            print(f"Error processing image: {e}")
            return

    # Generate Premium SVG
    svg_content = f"""<svg width="450" height="450" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="glow" cx="50%" cy="50%" r="50%">
      <stop offset="80%" stop-color="#58A6FF" stop-opacity="0.1" />
      <stop offset="100%" stop-color="#0D1117" stop-opacity="0" />
    </radialGradient>
    <linearGradient id="neon-ring" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#58A6FF" />
      <stop offset="50%" stop-color="#1F6FEB" />
      <stop offset="100%" stop-color="#388BFD" />
    </linearGradient>
    
    <filter id="blur-glow">
      <feGaussianBlur stdDeviation="8" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    
    <style>
      .breathing {{
        animation: breath 4s ease-in-out infinite alternate;
      }}
      .spin {{
        animation: rotate 8s linear infinite;
        transform-origin: center;
      }}
      .particles {{
        animation: float 6s infinite ease-in-out alternate;
      }}
      .particles2 {{
        animation: float2 7s infinite ease-in-out alternate-reverse;
      }}
      
      @keyframes breath {{
        0% {{ filter: drop-shadow(0 0 10px rgba(88, 166, 255, 0.3)); transform: scale(0.98); }}
        100% {{ filter: drop-shadow(0 0 25px rgba(88, 166, 255, 0.7)); transform: scale(1.02); }}
      }}
      
      @keyframes rotate {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
      }}
      
      @keyframes float {{
        0% {{ transform: translateY(0px) translateX(0px); opacity: 0.3; }}
        100% {{ transform: translateY(-20px) translateX(10px); opacity: 0.8; }}
      }}
      
      @keyframes float2 {{
        0% {{ transform: translateY(0px) translateX(0px); opacity: 0.4; }}
        100% {{ transform: translateY(20px) translateX(-15px); opacity: 0.9; }}
      }}
    </style>
  </defs>

  <!-- Ambient Glow -->
  <circle cx="225" cy="225" r="215" fill="url(#glow)" class="breathing" />

  <!-- Outer Spinning Ring -->
  <circle cx="225" cy="225" r="205" fill="none" stroke="url(#neon-ring)" stroke-width="2" stroke-dasharray="300 100 100 50" class="spin" filter="url(#blur-glow)" />
  
  <!-- Inner Premium Ring -->
  <circle cx="225" cy="225" r="200" fill="none" stroke="#30363d" stroke-width="4" />
  <circle cx="225" cy="225" r="200" fill="none" stroke="#58A6FF" stroke-width="2" stroke-dasharray="600" stroke-dashoffset="600">
    <animate attributeName="stroke-dashoffset" values="600;0" dur="2s" fill="freeze" />
  </circle>

  <!-- The Avatar Image -->
  <g class="breathing" style="transform-origin: center;">
    <clipPath id="circle-clip">
      <circle cx="225" cy="225" r="195" />
    </clipPath>
    <image x="30" y="30" width="390" height="390" preserveAspectRatio="xMidYMid slice" xlink:href="{base64_str}" clip-path="url(#circle-clip)" />
  </g>

  <!-- Floating Particles -->
  <circle cx="50" cy="100" r="3" fill="#58A6FF" class="particles" filter="url(#blur-glow)" />
  <circle cx="380" cy="80" r="4" fill="#1F6FEB" class="particles2" filter="url(#blur-glow)" />
  <circle cx="80" cy="350" r="2" fill="#388BFD" class="particles2" filter="url(#blur-glow)" />
  <circle cx="390" cy="360" r="3" fill="#58A6FF" class="particles" filter="url(#blur-glow)" />

</svg>"""
    with open(output_svg, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print("Premium Avatar SVG generated.")

def generate_thumbnails():
    projects = [
        {"id": "cater", "name": "Cater Connect", "color1": "#58A6FF", "color2": "#1F6FEB"},
        {"id": "portfolio", "name": "Portfolio", "color1": "#8957E5", "color2": "#D2A8FF"},
        {"id": "task", "name": "Task Manager", "color1": "#238636", "color2": "#2EA043"},
        {"id": "qa", "name": "QA Checker", "color1": "#F78166", "color2": "#FF7B72"},
        {"id": "routing", "name": "Routing Engine", "color1": "#E3B341", "color2": "#F2CC60"},
        {"id": "ai", "name": "AI Report Gen", "color1": "#A371F7", "color2": "#BC8CFF"}
    ]
    for p in projects:
        svg = f"""<svg width="400" height="150" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad_{p['id']}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{p['color1']}" stop-opacity="0.2" />
      <stop offset="100%" stop-color="{p['color2']}" stop-opacity="0.05" />
    </linearGradient>
    <linearGradient id="line_{p['id']}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{p['color1']}" />
      <stop offset="100%" stop-color="{p['color2']}" stop-opacity="0" />
    </linearGradient>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@700&amp;display=swap');
      .title {{ font-family: 'Inter', sans-serif; font-size: 20px; font-weight: 700; fill: #c9d1d9; }}
      .box {{ rx: 8px; ry: 8px; }}
    </style>
  </defs>
  <rect width="400" height="150" fill="url(#grad_{p['id']})" class="box" stroke="#30363d" stroke-width="1"/>
  <rect width="400" height="2" fill="url(#line_{p['id']})" class="box" />
  <circle cx="200" cy="65" r="25" fill="none" stroke="{p['color1']}" stroke-width="2" opacity="0.6"/>
  <circle cx="200" cy="65" r="15" fill="{p['color2']}" opacity="0.4"/>
  <text x="200" y="120" class="title" text-anchor="middle">{p['name']}</text>
</svg>"""
        with open(f"assets/thumb-{p['id']}.svg", "w", encoding="utf-8") as f:
            f.write(svg)
    print("Project thumbnails generated.")

def generate_footer_divider():
    svg = """<svg width="800" height="20" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0D1117" />
      <stop offset="50%" stop-color="#58A6FF" />
      <stop offset="100%" stop-color="#0D1117" />
    </linearGradient>
    <style>
      .glow { filter: drop-shadow(0px 0px 4px rgba(88, 166, 255, 0.5)); }
      .moving {
        stroke-dasharray: 800;
        animation: slide 3s ease-in-out infinite alternate;
      }
      @keyframes slide {
        0% { stroke-dashoffset: 800; }
        100% { stroke-dashoffset: 0; }
      }
    </style>
  </defs>
  <rect x="0" y="8" width="800" height="1" fill="#30363d" />
  <rect x="0" y="8" width="800" height="2" fill="url(#grad)" class="moving glow" />
  <circle cx="400" cy="9" r="3" fill="#58A6FF" class="glow" />
</svg>"""
    with open("assets/footer-divider.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("Footer divider generated.")

if __name__ == "__main__":
    generate_headers()
    generate_avatar()
    generate_thumbnails()
    generate_footer_divider()
