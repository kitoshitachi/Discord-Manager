from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont
from pilmoji import Pilmoji
import io
from cores.fantasy import Character, Stat

@dataclass(eq=False, repr=False)
class _BaseCard:
    avatar_size = (270, 270)
    avatar_offset = (540,50)

    progress_x, progress_y = 50, 200
    progress_width = 410
    progress_height = 40

    remaining_progress = 0.5
    red_color = (255, 0, 0)

    stat_x = 120
    stat_y = 345
    offset_x = 410
    offset_y = 65

    card = Image.open('assets\RankCard\card.png')
    title_font = ImageFont.truetype('assets\Font\ConcertOne-Regular.ttf', 43)
    font = ImageFont.truetype('assets\Font\ConcertOne-Regular.ttf', 20)
    full_card = Image.new('RGBA', card.size, (255, 255, 255, 255))


class Card(_BaseCard):
    @staticmethod    
    def new_bar(draw:ImageDraw.ImageDraw, x, y, width, height, progress, bg=(129, 66, 97), fg=(255,0,0), fg2=(179,174,174)) -> ImageDraw.ImageDraw:
        # Draw the background
        draw.rectangle((x+(height/2), y, x+width+(height/2), y+height), fill=fg2, width=10)
        draw.ellipse((x+width, y, x+height+width, y+height), fill=fg2)
        draw.ellipse((x, y, x+height, y+height), fill=fg2)
        width = int(width*progress)
        # Draw the part of the progress bar that is actually filled
        draw.rectangle((x+(height/2), y, x+width+(height/2), y+height), fill=fg, width=10)
        draw.ellipse((x+width, y, x+height+width, y+height), fill=fg)
        draw.ellipse((x, y, x+height, y+height), fill=fg)
        return draw

    @staticmethod
    def get_offset_stat(column, row):
        return Card.stat_x + Card.offset_x * column, Card.stat_y + Card.offset_y * row

    @staticmethod
    def image(name, character:Character, mode, avatar = None):
        #define
        draw_text = Pilmoji(Card.card)
        draw = ImageDraw.Draw(Card.card)
        current_xp = character.infor.xp
        total_xp = character.infor.total_xp
        progress = current_xp / total_xp

        current_stat:Stat = getattr(character, mode)
        stat_fields = [
            [current_stat.HP, current_stat.MP, current_stat.AGI],
            [current_stat.STR, current_stat.PR, current_stat.CR]
        ]

        if mode == 'display_stat':
            max_len = len(str(current_stat.HP))
        else:
            max_len = 4
            current_stat = current_stat.round()


        if avatar is None:
            avatar = Image.new('RGBA', Card.avatar_size, (255, 255, 255, 255))
        else:
            avatar = io.BytesIO(avatar)
            avatar = Image.open(avatar)
            avatar = avatar.resize(Card.avatar_size)
        #draw
        draw_text.text((65, 55), name, font=Card.title_font, fill=Card.red_color)
        draw_text.text((145, 125), f"{current_xp}/{total_xp}", font=Card.title_font, fill=Card.red_color)
        
        draw = Card.new_bar(
            draw, Card.progress_x, Card.progress_y, 
            Card.progress_width, Card.progress_height, 
            progress
        )
        draw_text.text((Card.stat_x, 277), str(character.infor.spirit), font=Card.title_font, fill=Card.red_color)

        draw_text.text((630,540), 'Powered by Vampire', font=Card.font, fill=Card.red_color)

        for column, list_stat in enumerate(stat_fields):
            for row, stat in enumerate(list_stat):
                draw_text.text(Card.get_offset_stat(column, row), f"{stat:0>{max_len}}", font=Card.title_font, fill=Card.red_color)


        Card.full_card.paste(Card.card)
        Card.full_card.paste(avatar, Card.avatar_offset)
        
        return Card.full_card