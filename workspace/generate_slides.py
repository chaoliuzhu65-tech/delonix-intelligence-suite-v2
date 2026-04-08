#!/usr/bin/env python3
"""Generate slide images for podcast video"""
from PIL import Image, ImageDraw, ImageFont
import os

# Slide dimensions
WIDTH = 1920
HEIGHT = 1080

def get_font(size):
    """Try to get a Chinese font"""
    fonts = [
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc", 
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    for f in fonts:
        if os.path.exists(f):
            try:
                return ImageFont.truetype(f, size)
            except:
                continue
    return ImageFont.load_default()

def create_slide(title, subtitle="", bg_color=(26, 26, 46), text_color=(255, 255, 255), accent_color=(233, 69, 96)):
    """Create a slide image"""
    img = Image.new('RGB', (WIDTH, HEIGHT), bg_color)
    draw = ImageDraw.Draw(img)
    font_title = get_font(80)
    font_subtitle = get_font(48)
    font_small = get_font(36)
    
    # Title
    if title:
        bbox = draw.textbbox((0, 0), title, font=font_title)
        text_width = bbox[2] - bbox[0]
        x = (WIDTH - text_width) // 2
        draw.text((x, 300), title, fill=text_color, font=font_title)
    
    # Subtitle
    if subtitle:
        bbox = draw.textbbox((0, 0), subtitle, font=font_subtitle)
        text_width = bbox[2] - bbox[0]
        x = (WIDTH - text_width) // 2
        draw.text((x, 450), subtitle, fill=(150, 150, 150), font=font_subtitle)
    
    return img

def create_data_slide(title, items, highlight_idx=None):
    """Create a data display slide"""
    img = Image.new('RGB', (WIDTH, HEIGHT), (15, 52, 96))
    draw = ImageDraw.Draw(img)
    font_title = get_font(72)
    font_value = get_font(96)
    font_label = get_font(36)
    
    # Title
    bbox = draw.textbbox((0, 0), title, font=font_title)
    text_width = bbox[2] - bbox[0]
    x = (WIDTH - text_width) // 2
    draw.text((x, 100), title, fill=(255, 255, 255), font=font_title)
    
    # Items
    item_width = WIDTH // len(items)
    for i, (value, label) in enumerate(items):
        x = item_width * i + item_width // 2
        # Value
        bbox = draw.textbbox((0, 0), value, font=font_value)
        text_width = bbox[2] - bbox[0]
        draw.text((x - text_width // 2, 350), value, fill=(233, 69, 96), font=font_value)
        # Label
        bbox = draw.textbbox((0, 0), label, font=font_label)
        text_width = bbox[2] - bbox[0]
        draw.text((x - text_width // 2, 500), label, fill=(150, 150, 150), font=font_label)
    
    return img

def create_quote_slide(quote):
    """Create a quote slide"""
    img = Image.new('RGB', (WIDTH, HEIGHT), (15, 52, 96))
    draw = ImageDraw.Draw(img)
    font = get_font(56)
    
    # Quote box background
    draw.rectangle([100, 300, WIDTH - 100, 700], fill=(233, 69, 96, 30))
    draw.rectangle([100, 300, 120, 700], fill=(233, 69, 96))
    
    # Quote text
    lines = quote.split('\n')
    y = 380
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (WIDTH - text_width) // 2
        draw.text((x, y), line, fill=(255, 255, 255), font=font)
        y += 80
    
    return img

# Generate slides
os.makedirs('/home/gem/workspace/agent/workspace/slides', exist_ok=True)

# Slide 1: Title
slide = create_slide("德胧AI虫洞落地实践分享", "天津瑞湾开元名都酒店 | 晁留柱 | 2026年4月")
slide.save('/home/gem/workspace/agent/workspace/slides/slide_01.png')

# Slide 2: Quote
slide = create_quote_slide("让AI成为宾客与酒店之间\n永远开着的那条信道")
slide.save('/home/gem/workspace/agent/workspace/slides/slide_02.png')

# Slide 3: Process
slide = create_slide("神灯AI完整服务闭环", "需求感知 → 智能调度 → 人力执行 → 数据回流", bg_color=(248, 249, 250), text_color=(26, 26, 46))
slide.save('/home/gem/workspace/agent/workspace/slides/slide_03.png')

# Slide 4: Data
slide = create_data_slide("关键效率数据", [
    ("83%", "报修效率提升"),
    ("98%", "竞对分析提升"),
    ("500%", "知识库填充")
])
slide.save('/home/gem/workspace/agent/workspace/slides/slide_04.png')

# Slide 5: Comparison
slide = create_slide("入住效率革命", "15分钟 → 10秒", bg_color=(248, 249, 250), text_color=(26, 26, 46))
slide.save('/home/gem/workspace/agent/workspace/slides/slide_05.png')

# Slide 6: Work orders
slide = create_data_slide("工单类型分布", [
    ("46.5%", "送物类"),
    ("24.8%", "酒店咨询"),
    ("10.3%", "维修类")
])
slide.save('/home/gem/workspace/agent/workspace/slides/slide_06.png')

# Slide 7: ROI
slide = create_data_slide("投入产出分析", [
    ("2.5万", "年投入"),
    ("9万+", "年收益"),
    ("948%", "投资回报率")
], bg_color=(248, 249, 250))
slide.save('/home/gem/workspace/agent/workspace/slides/slide_07.png')

# Slide 8: Growth
slide = create_slide("AI成长历程", "2023懵懂期 → 2024觉醒期 → 2025深水期 → 2026现在")
slide.save('/home/gem/workspace/agent/workspace/slides/slide_08.png')

# Slide 9: Tips
slide = create_slide("三点心得", "1.不要等准备好了再开始\n2.AI是每个酒店人都能用好的工具\n3.未来酒店竞争是AI能力的竞争", bg_color=(248, 249, 250), text_color=(26, 26, 46))
slide.save('/home/gem/workspace/agent/workspace/slides/slide_09.png')

# Slide 10: End
slide = create_slide("谢谢！", "louis.chao@delonixmail.com")
slide.save('/home/gem/workspace/agent/workspace/slides/slide_10.png')

print("Generated 10 slides!")
