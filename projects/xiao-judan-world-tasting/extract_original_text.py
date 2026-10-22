#!/usr/bin/env python3
"""Extract page 001's ORIGINAL raster lettering from its reference spread.

The hand-measured regions are for page 001 only, not general OCR. Extraction
uses transparent alpha masks; illustrations and typography remain separate.
"""
from pathlib import Path
import numpy as np
from PIL import Image

HERE=Path(__file__).resolve().parent
SOURCE=HERE/'assets/reference/001_original_spread.png'
OUT=HERE/'assets/text_original'
SIZE=(1086,1448)
PAGE_RECTS={'specimen':(23,15,751,945),'story':(785,15,1519,945)}
TEXT_RECTS={
    'specimen':[(95,151,628,245),(102,267,359,312),(102,330,359,375),
                (102,391,370,438),(103,480,468,504)],
    'story':[(591,1290,1032,1364)]
}

def main():
    im=Image.open(SOURCE).convert('RGB')
    OUT.mkdir(parents=True,exist_ok=True)
    for side,box in PAGE_RECTS.items():
        page=im.crop(box).resize(SIZE,Image.Resampling.LANCZOS)
        result=Image.new('RGBA',SIZE,(0,0,0,0))
        for rect in TEXT_RECTS[side]:
            data=np.asarray(page.crop(rect)).astype(np.float32)
            luminosity=.2126*data[:,:,0]+.7152*data[:,:,1]+.0722*data[:,:,2]
            alpha=np.clip((218-luminosity)*2.2,0,255).astype('uint8')
            alpha[alpha<21]=0
            crop=Image.fromarray(np.dstack([data.astype('uint8'),alpha]),'RGBA')
            result.alpha_composite(crop,dest=rect[:2])
        path=OUT/f'001_{side}.png'
        result.save(path)
        print('LETTERING',path)

if __name__=='__main__':main()
