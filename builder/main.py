import logging
import click
import requests
from rich.console import Console
from rich.logging import RichHandler
import pyfiglet
from PIL import Image, ImageDraw, ImageFont

from util.build import Build
from util.config import Config
from util.makeenv import MakeEnv
from util.obfuscate import DoObfuscate
from util.writeconfig import WriteConfig

def render_text_with_vandal(text, font_path, font_size=100):
    font = ImageFont.truetype(font_path, font_size)
    bbox = font.getbbox(text)
    width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font, fill=(0, 0, 0))
    return image

def main():

    logging.basicConfig(
        level="NOTSET",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, tracebacks_suppress=[click])]
    )

    logging.getLogger("rich")
    console = Console()

    vandal_font_path = r"C:\Users\PC\OneDrive\Desktop\BLK token\font\Vandal.ttf"  # مسیر فایل فونت Vandal

    # Render text with Vandal font and convert to ASCII art using pyfiglet
    figlet = pyfiglet.Figlet(font='standard')  # استفاده از فونت استاندارد pyfiglet
    ascii_art = figlet.renderText("BLK")

    console.print(ascii_art,
                  justify="center", highlight=False, style="red", overflow="ignore")
    # Modify the print statement since stars and forks are removed
    console.print(f"MD By BLK/hyperkiller.\n",
                  justify="center", highlight=False, style="bold red", overflow="ignore")

    config = Config()
    config_data = config.get_config()

    make_env = MakeEnv()
    make_env.make_env()
    make_env.get_src()

    write_config = WriteConfig(config_data)
    write_config.write_config()

    do_obfuscate = DoObfuscate()
    do_obfuscate.run()

    build = Build()
    build.get_pyinstaller()
    build.get_upx()
    build.build()

if __name__ == "__main__":
    main()
