"""Prépare les photos optimisées, les polices et les médias locaux."""
from pathlib import Path
import sys, re, urllib.request, subprocess, asyncio, json
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools/python-packages'))
from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageFilter
import imageio_ffmpeg
SOURCES = [
 ('Front_de_mer.JPEG','front-de-mer','Le front de mer'),
 ('jardin_essai_alger.JPEG','jardin-essai','Le Jardin d’Essai du Hamma'),
 ('monument_martyres.JPEG','monument-martyrs','Le Monument des Martyrs'),
 ('Notre_Dame_Afrique.JPEG','notre-dame-afrique','Notre-Dame d’Afrique'),
 ('alger_downtown.JPEG','centre-ville','Le centre-ville'),
 ('alger_nuit.JPEG','alger-nuit','Alger à la nuit tombée'),
 ('Rue_place_audin_nuit.JPEG','place-audin','Autour de la place Audin')
]
manifest=[]
for source,slug,title in SOURCES:
    with Image.open(ROOT.parent/'img'/source) as opened:
        im=ImageOps.exif_transpose(opened).convert('RGB')
        for width in [480,960,1600]+([2200] if slug=='front-de-mer' else []):
            copy=im.copy()
            copy.thumbnail((width,round(width*im.height/im.width)),Image.Resampling.LANCZOS)
            target=ROOT/'images'/f'{slug}-{width}.webp'
            copy.save(target,'WEBP',quality=82,method=6)
            manifest.append({'file':target.name,'width':copy.width,'height':copy.height,'bytes':target.stat().st_size})
(ROOT/'tools/image-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('Photos optimisées.',flush=True)
# Polices distribuées par Google Fonts, hébergées ici pour le mode hors ligne.
(ROOT/'fonts').mkdir(exist_ok=True)
url='https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=DM+Sans:wght@400;500;600&display=swap'
req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
css=urllib.request.urlopen(req,timeout=30).read().decode()
for index,remote in enumerate(dict.fromkeys(re.findall(r'url\((https[^)]+)\)',css))):
    extension=remote.split('?')[0].rsplit('.',1)[-1]
    name=f'google-font-{index}.{extension}'
    (ROOT/'fonts'/name).write_bytes(urllib.request.urlopen(remote,timeout=30).read())
    css=css.replace(remote,'../fonts/'+name)
(ROOT/'css/fonts.css').write_text('/* Google Fonts, auto-hébergées ; licences dans fonts/. */\n'+css,encoding='utf-8')
for family in ['dmsans','cormorantgaramond']:
    url=f'https://raw.githubusercontent.com/google/fonts/main/ofl/{family}/OFL.txt'
    (ROOT/'fonts'/f'{family}-OFL.txt').write_bytes(urllib.request.urlopen(url,timeout=30).read())
print('Polices locales prêtes.',flush=True)
# Film muet H.264 ; composition 16:9 préservant les photos verticales.
frames=ROOT/'tools/video-frames'
frames.mkdir(exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/georgia.ttf',36)
small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
vtt=['WEBVTT\n']
for index,(_,slug,title) in enumerate(SOURCES):
    with Image.open(ROOT/'images'/f'{slug}-1600.webp') as im:
        bg=ImageOps.fit(im,(1280,720)).filter(ImageFilter.GaussianBlur(28))
        overlay=Image.new('RGB',(1280,720),'#0f303c')
        bg=Image.blend(bg,overlay,.55)
        inset=ImageOps.contain(im,(1280,620))
        bg.paste(inset,((1280-inset.width)//2,0))
        draw=ImageDraw.Draw(bg)
        draw.rectangle((0,620,1280,720),fill='#133e4c')
        draw.text((38,639),title,font=font,fill='#f8f4ea')
        draw.text((1060,655),f'ALGER  /  0{index+1}',font=small,fill='#e9c88d')
        bg.save(frames/f'{index:02}.jpg',quality=88)
        a,b=index*4,(index+1)*4
        vtt.append(f'{index+1}\n00:00:{a:02}.000 --> 00:00:{b:02}.000\n{title}\n')
(ROOT/'video/alger-jour-nuit.vtt').write_text('\n'.join(vtt),encoding='utf-8')
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([ffmpeg,'-y','-loglevel','error','-framerate','1/4','-i',str(frames/'%02d.jpg'),'-c:v','libx264','-preset','medium','-crf','24','-pix_fmt','yuv420p','-r','24','-movflags','+faststart','-t','28',str(ROOT/'video/alger-jour-nuit.mp4')],check=True)
print('Vidéo 720p H.264 générée.',flush=True)
# Narration française à partir d'un texte original, sans donnée personnelle.
import edge_tts
async def narration():
    text=(ROOT/'audio/transcription.txt').read_text(encoding='utf-8')
    voice=edge_tts.Communicate(text,'fr-FR-DeniseNeural',rate='-8%')
    await voice.save(str(ROOT/'audio/bienvenue-alger.mp3'))
asyncio.run(narration())
print('Narration française générée.',flush=True)
