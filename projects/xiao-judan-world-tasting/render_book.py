#!/usr/bin/env python3
"""Render page 001 with original raster lettering or YAML-controlled live SVG text.

Run: python render_book.py                 # original lettering (faithful, not editable)
     python render_book.py --text-mode editable
     python render_book.py --no-preview

Outputs SVG masters with separate Inkscape layers, individual PNG previews, and a
single PNG spread preview. Images are linked by relative paths to avoid duplication.
"""
from __future__ import annotations

import argparse
import copy
import shutil
import subprocess
from pathlib import Path
from xml.etree import ElementTree as ET

import yaml
from PIL import Image

HERE = Path(__file__).resolve().parent
SVG = 'http://www.w3.org/2000/svg'
INK = 'http://www.inkscape.org/namespaces/inkscape'
XLINK = 'http://www.w3.org/1999/xlink'
ET.register_namespace('', SVG)
ET.register_namespace('inkscape', INK)
ET.register_namespace('xlink', XLINK)


def el(parent, name, attrs=None, text=None):
    obj = ET.SubElement(parent, '{%s}%s' % (SVG,name), {str(k):str(v) for k,v in (attrs or {}).items()})
    if text is not None:
        obj.text = text
    return obj


def layer(svg, identifier, label):
    return el(svg,'g',{'id':identifier,'{%s}groupmode'%INK:'layer','{%s}label'%INK:label})


def merge(base, overrides):
    result=copy.deepcopy(base)
    for k,v in overrides.items():
        result[k] = merge(result[k],v) if isinstance(v,dict) and isinstance(result.get(k),dict) else v
    return result


def add_image(layer_node, name, path, dst, width, height):
    """Relative links keep image assets individually replaceable in vector editors."""
    import os
    if not path.is_file():
        raise FileNotFoundError(path)
    el(layer_node,'image',{'id':name,'x':'0','y':'0','width':width,'height':height,
       '{%s}href'%XLINK:os.path.relpath(path,dst.parent)})


def text(parent, contents, style, font, key, y):
    el(parent,'text',{
        'id':key, 'x':style['x'], 'y':y,
        'font-family':"'%s', '%s'" % (font['family'],font['fallback']),
        'font-size':style['size'], 'font-weight':style.get('weight','normal'),
        'letter-spacing':style.get('letter_spacing',0), 'fill':font['color'],
        'xml:space':'preserve'
    }, contents)


def make_svg(page, side, design, dest, mode):
    d=merge(design,page.get('layout',{}))
    w,h=d['canvas']['width'],d['canvas']['height']
    root=ET.Element('{%s}svg'%SVG,{'version':'1.1','width':str(w),'height':str(h),
        'viewBox':f'0 0 {w} {h}', 'role':'img','aria-label':f"{page['id']} {side}"})
    el(root,'title',text=f"{page['id']} {side} — {mode}")
    art=layer(root,'illustration-layer','01 · Illustration')
    add_image(art,'illustration',HERE/page['art'][side],dest,w,h)
    decorations=layer(root,'decorations-layer','02 · Divider and rules')
    typography=layer(root,'typography-layer',
        '03 · Original lettering (raster)' if mode=='original' else '03 · Live editable text')
    if mode=='original':
        if side not in page.get('original_text',{}):
            raise ValueError(f"{page['id']} has no original lettering asset for {side}")
        add_image(typography,'original-lettering',HERE/page['original_text'][side],dest,w,h)
    elif side=='specimen':
        spec=d['specimen']
        text(typography,page['specimen']['title'],spec['title'],d['font'],'title',spec['title']['y'])
        p=spec['facts']
        for idx,fact in enumerate(page['specimen'].get('facts',[])):
            text(typography,fact,p,d['font'],f'fact-{idx+1}',p['first_baseline']+idx*p['line_gap'])
        rule=spec.get('divider')
        if rule:
            el(decorations,'line',{'id':'divider','x1':rule['x1'],'x2':rule['x2'],
                'y1':rule['y'],'y2':rule['y'],'stroke':rule['stroke'],
                'stroke-width':rule['stroke_width'],'opacity':rule.get('opacity',1)})
    else:
        p=d['story']['text']
        for idx,line in enumerate(page['story']['lines']):
            text(typography,line,p,d['font'],f'story-line-{idx+1}',p['first_baseline']+idx*p['line_gap'])
    dest.parent.mkdir(parents=True,exist_ok=True)
    ET.ElementTree(root).write(dest,encoding='utf-8',xml_declaration=True)


def rasterize(svg,png):
    inkscape=shutil.which('inkscape')
    if inkscape:
        subprocess.run([inkscape,str(svg),'--export-area-page',f'--export-filename={png}'],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        import cairosvg
        cairosvg.svg2png(url=str(svg),write_to=str(png))


def spread(spec,story,target):
    with Image.open(spec) as l,Image.open(story) as r:
        w,h=l.size
        margin,gutter=20,28
        canvas=Image.new('RGB',(2*w+2*margin+gutter,h+2*margin),(248,246,239))
        canvas.paste(l.convert('RGB'),(margin,margin))
        canvas.paste(r.convert('RGB'),(margin+w+gutter,margin))
        canvas.save(target)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--text-mode',choices=['original','editable'],default='original')
    p.add_argument('--pages',nargs='*',help='Select pages: 001 002 etc')
    p.add_argument('--no-preview',action='store_true')
    args=p.parse_args()
    book=yaml.safe_load((HERE/'book.yaml').read_text(encoding='utf-8'))
    design=yaml.safe_load((HERE/'design.yaml').read_text(encoding='utf-8'))
    target=HERE/'generated'/(('editable') if args.text_mode=='editable' else '')
    target.mkdir(parents=True,exist_ok=True)
    for page in book['pages']:
        pid=str(page['id']).zfill(3)
        if args.pages and pid not in args.pages:continue
        previews={}
        for side in ('specimen','story'):
            svg=target/f'{pid}_{side}.svg'
            make_svg(page,side,design,svg,args.text_mode)
            print('SVG',svg)
            if not args.no_preview:
                img=target/f'{pid}_{side}_preview.png'
                rasterize(svg,img)
                previews[side]=img
                print('PNG',img)
        if not args.no_preview:
            out=target/f'{pid}_spread_preview.png'
            spread(previews['specimen'],previews['story'],out)
            print('SPREAD',out)

if __name__=='__main__':main()
