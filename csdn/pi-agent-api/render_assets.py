"""Render the three explanatory figures for the Pi Agent article."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).parent / "assets" / "_candidates"
ROOT.mkdir(parents=True, exist_ok=True)
FONT = Path(r"C:\Windows\Fonts\Noto Sans SC (TrueType).otf")
BOLD = Path(r"C:\Windows\Fonts\Noto Sans SC Bold (TrueType).otf")
BG = "#F7FAFF"
NAVY = "#163258"
BLUE = "#1677FF"
MID = "#526A88"
PALE = "#EAF3FF"
LINE = "#C8DDF7"
WHITE = "#FFFFFF"


def font(size, bold=False):
    return ImageFont.truetype(str(BOLD if bold else FONT), size)


def canvas(height):
    im = Image.new("RGB", (1600, height), BG)
    return im, ImageDraw.Draw(im)


def rr(d, box, fill=WHITE, outline=LINE, radius=28, width=3):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def txt(d, xy, value, size=36, fill=NAVY, bold=False, anchor="lt"):
    d.text(xy, value, font=font(size, bold), fill=fill, anchor=anchor)


def arrow(d, start, end, fill=BLUE, width=8):
    d.line((start, end), fill=fill, width=width)
    x1, y1 = start
    x2, y2 = end
    if x2 > x1:
        pts = [(x2, y2), (x2 - 19, y2 - 12), (x2 - 19, y2 + 12)]
    elif y2 > y1:
        pts = [(x2, y2), (x2 - 12, y2 - 19), (x2 + 12, y2 - 19)]
    else:
        pts = [(x2, y2), (x2 - 12, y2 + 19), (x2 + 12, y2 + 19)]
    d.polygon(pts, fill=fill)


def save(im, name):
    path = ROOT / name
    im.save(path, optimize=True)
    im.resize((800, round(im.height / 2)), Image.Resampling.LANCZOS).save(
        ROOT / name.replace(".png", "-800.png"), optimize=True
    )


def cover():
    im, d = canvas(900)
    d.rounded_rectangle((65, 70, 1535, 830), radius=42, fill=WHITE, outline=LINE, width=4)
    d.rounded_rectangle((110, 112, 410, 170), radius=20, fill=PALE)
    txt(d, (260, 141), "Pi Agent · 核心 API", 30, BLUE, True, "mm")
    txt(d, (110, 225), "第一个 Agent，究竟怎么跑起来？", 73, NAVY, True)
    txt(d, (110, 345), "几行代码，串起配置、运行与观察", 42, MID)
    labels = [
        ("01", "模型就绪", "ModelRuntime"),
        ("02", "创建会话", "createAgentSession"),
        ("03", "接收事件", "subscribe"),
        ("04", "完成回复", "prompt"),
    ]
    w = 315
    gap = 34
    for i, (n, title, code) in enumerate(labels):
        x = 110 + i * (w + gap)
        rr(d, (x, 520, x + w, 720), fill=PALE, outline=LINE)
        txt(d, (x + 28, 546), n, 29, BLUE, True)
        txt(d, (x + 28, 600), title, 41, NAVY, True)
        txt(d, (x + 28, 662), code, 25, MID)
        if i < 3:
            arrow(d, (x + w + 5, 620), (x + w + gap - 7, 620), BLUE, 6)
    save(im, "pi-agent-cover-v1.png")


def layers():
    im, d = canvas(1050)
    txt(d, (80, 68), "三层职责：交互、支撑、执行", 64, NAVY, True)
    txt(d, (80, 155), "ExtensionRuntime 是运行时中的扩展机制", 34, MID)

    blocks = [
        (235, "Session", "发消息 · 接事件 · 结束会话", "prompt()   subscribe()   dispose()", "#EAF3FF"),
        (465, "Runtime", "提供模型、资源、会话历史和设置", "ModelRuntime   ResourceLoader   SessionManager   SettingsManager", "#EFF6FF"),
        (765, "Tool", "按需执行外部操作", "read   bash   edit   write   + 扩展工具", "#EAF3FF"),
    ]
    for y, title, line, detail, fill in blocks:
        h = 185 if title != "Runtime" else 250
        rr(d, (80, y, 1520, y + h), fill=fill, radius=32)
        d.rounded_rectangle((80, y, 330, y + h), radius=32, fill=BLUE)
        txt(d, (205, y + h / 2), title, 45, WHITE, True, "mm")
        txt(d, (375, y + 36), line, 39, NAVY, True)
        txt(d, (375, y + 105), detail, 27, MID)
        if title == "Runtime":
            d.rounded_rectangle((375, y + 164, 1430, y + 225), radius=19, fill=WHITE, outline=LINE, width=2)
            txt(d, (403, y + 178), "扩展机制：ExtensionRuntime 注册工具、挂事件钩子", 29, BLUE, True)
    txt(d, (110, 988), "职责关系：Runtime 配置 Session；Session 驱动已启用的 Tool。", 29, MID)
    save(im, "pi-agent-layers-v1.png")


def events():
    im, d = canvas(1000)
    txt(d, (80, 62), "一次提问中，谁负责启动？谁负责观察？", 60, NAVY, True)
    txt(d, (80, 145), "工具调用是可选分支；事件顺序以实际运行输出为准", 31, MID)
    steps = [
        (235, "1", "subscribe()", "注册回调，等待事件", "只负责观察"),
        (390, "2", "await prompt()", "提交问题，启动 Agent", "等待完成"),
        (545, "3", "message_update", "模型生成文字或提出工具调用", "按类型过滤"),
        (700, "4", "tool_execution_*", "需要工具时执行，再继续生成", "可选"),
        (855, "5", "本次运行结束", "正常完成或抛出错误", "await 结束"),
    ]
    for y, num, name, desc, note in steps:
        rr(d, (90, y, 1510, y + 118), fill=WHITE)
        d.ellipse((115, y + 21, 190, y + 96), fill=BLUE)
        txt(d, (152, y + 58), num, 36, WHITE, True, "mm")
        txt(d, (225, y + 24), name, 37, NAVY, True)
        txt(d, (695, y + 28), desc, 31, MID)
        d.rounded_rectangle((1280, y + 31, 1460, y + 87), radius=18, fill=PALE)
        txt(d, (1370, y + 58), note, 25, BLUE, True, "mm")
        if num != "5":
            arrow(d, (800, y + 122), (800, y + 148), BLUE, 5)
    save(im, "pi-agent-events-v1.png")


cover()
layers()
events()
