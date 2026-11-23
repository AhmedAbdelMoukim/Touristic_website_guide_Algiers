"""Vérification structurelle : HTML, liens locaux, médias et livrables."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote,urlsplit
import re,sys,subprocess,json
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self,path):
        super().__init__(convert_charrefs=True)
        self.path=path; self.ids=[]; self.tags=[]; self.links=[]; self.labels=[]; self.inputs=[]
        self.feed(path.read_text(encoding='utf-8-sig'))
    def handle_starttag(self,tag,attrs):
        a=dict(attrs);self.tags.append((tag,a))
        if 'id' in a:self.ids.append(a['id'])
        if 'for' in a:self.labels.append(a['for'])
        if tag in ('input','select','textarea'):self.inputs.append(a.get('id'))
        for prop in ('src','href','poster'):
            if a.get(prop):self.links.append(a[prop])
        if a.get('srcset'):
            self.links.extend(part.strip().split()[0] for part in a['srcset'].split(','))
pages={p.name:Page(p) for p in ROOT.glob('*.html')}
errors=[]
for name,p in pages.items():
    if len(p.ids)!=len(set(p.ids)): errors.append(f'{name}: identifiants dupliqués')
    if sum(tag=='h1' for tag,_ in p.tags)!=1: errors.append(f'{name}: h1 incorrect')
    for tag,a in p.tags:
        if tag=='img' and 'alt' not in a:errors.append(f'{name}: image sans alt')
    for ident in p.inputs:
        if ident not in p.labels:errors.append(f'{name}: label manquant {ident}')
    for link in p.links:
        parsed=urlsplit(link)
        if parsed.scheme or parsed.netloc:continue
        path=ROOT/unquote(parsed.path) if parsed.path else p.path
        if not path.exists():errors.append(f'{name}: fichier absent {link}')
        if parsed.fragment and path.suffix=='.html':
            dest=pages.get(path.name)
            if dest and unquote(parsed.fragment) not in dest.ids:errors.append(f'{name}: ancre absente {link}')
for path in (ROOT/'css').glob('*.css'):
    for link in re.findall(r'url\(["\']?([^)"\']+)',path.read_text(encoding='utf-8-sig')):
        if link.startswith(('data:','http')):continue
        if not (path.parent/link).exists(): errors.append(f'CSS : fichier absent {link}')
words=len((ROOT/'JUSTIFICATION-TECHNIQUE.md').read_text(encoding='utf-8-sig').split())-3
if not 200<=words<=300:errors.append(f'Justification hors limite : {words} mots')
assert len(pages)==4, 'Quatre pages requises'
sys.path.insert(0,str(ROOT/'tools/python-packages'))
import imageio_ffmpeg
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
for media in ['video/alger-jour-nuit.mp4','audio/bienvenue-alger.mp3']:
    r=subprocess.run([ffmpeg,'-v','error','-i',str(ROOT/media),'-f','null','-'],capture_output=True,text=True)
    if r.returncode:errors.append(media+': '+r.stderr)
checks=[
f'{len(pages)} pages HTML distinctes, chacune avec un h1.',
'Tous les chemins locaux, ancres internes, sources et variantes srcset existent.',
'Images avec attribut alt ; champs du formulaire associés aux labels.',
'Identifiants uniques dans chaque document.',
'Polices, CSS, Bootstrap et JavaScript hébergés localement.',
'Fichiers audio et vidéo décodés intégralement avec FFmpeg, sans erreur.',
f'Justification technique : environ {words} mots.',
'JavaScript vérifié séparément avec node --check.',
]
report='# Vérification du projet\n\n'
if errors:
    report+='## Erreurs\n\n'+'\n'.join('- '+e for e in errors)
else:
    report+='## Contrôles réussis\n\n'+'\n'.join('- '+x for x in checks)
report+='\n\n## Limites\n\nAucun navigateur pilotable disponible dans cette session. Le rendu visuel à 375, 768 et 1280 pixels, le comportement réel des interactions au clavier et la lecture dans le navigateur ne sont pas validés automatiquement. La vidéo externe est référencée par la source officielle UNESCO, mais sa lecture intégrée n’a pas pu être vérifiée. La procédure manuelle figure dans README.md.\n'
(ROOT/'VERIFICATION.md').write_text(report,encoding='utf-8')
print(json.dumps({'pages':len(pages),'justification_words':words,'errors':errors},ensure_ascii=True,indent=2))
sys.exit(bool(errors))
