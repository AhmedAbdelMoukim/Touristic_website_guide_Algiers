"""Prépare l'archive finale sans les outils de fabrication."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import re,json
root=Path('alger-la-blanche').resolve()
# Aérer le HTML généré en conservant exactement les contenus et les attributs.
for path in root.glob('*.html'):
    source=path.read_text(encoding='utf-8-sig')
    source=re.sub(r'>[ \t]*<','>\n<',source)
    path.write_text(source,encoding='utf-8')
archive=root.parent/'alger-la-blanche-remise.zip'
allowed={'css','js','images','fonts','audio','video','vendor'}
included=[]
with ZipFile(archive,'w',ZIP_DEFLATED,compresslevel=7) as output:
    for file in sorted(root.rglob('*')):
        if not file.is_file():continue
        relative=file.relative_to(root)
        if len(relative.parts)==1 or relative.parts[0] in allowed:
            output.write(file,Path('alger-la-blanche')/relative)
            included.append(relative.as_posix())
with ZipFile(archive) as check:
    assert check.testzip() is None
    assert len([n for n in check.namelist() if n.endswith('.html')])==4
print(json.dumps({'archive':str(archive),'files':len(included),'size_mb':round(archive.stat().st_size/1e6,2)},indent=2))
