#!/usr/bin/python

import os, sys, time, subprocess
import Image, ImageFont, ImageDraw
import utils1

if __name__ == '__main__':

    if len(sys.argv) < 2 :
        print "Usage: combine-all1.py screenshots [number]"
        exit(1)

    path = sys.argv[1]
    numberPerLine = 6

    start = time.time()

    package = None
    if len(sys.argv) == 3 : package = sys.argv[2]

    new_path = utils1.create_newpath(path, "all_combined")
    if os.path.exists(new_path) : utils1.rmdir(new_path)
    utils1.mkdir(new_path)

    languages = utils1.load_languages(path)
    print languages

    all = {}
    pkg = {}
    display = {}

    for l in languages:
        all[l] = {}
        files = utils1.traversal_by_ext(utils1.compose((path,l)), '.png')
        for file in files:
            p, f = utils1.filesplit(file)
            im = Image.open(utils1.compose((path,l,file)))
            all[l][file] = {"filename": f, "path": p, "resolution": im.size}
            if not display.has_key(im.size): display[im.size] = 0
            display[im.size] += 1
            if not pkg.has_key(p) : pkg[p] = {}
            pkg[p][f] = ''

    print display
    size = None
    if len(display) == 0 :
        print "No display"
        exit(3)
    elif len(display) == 1:
        print "Only one display resolution"
        size = display.keys()[0]
    else:
        print "More than one display resolution"
        size = utils1.find_min(display)
    print "Use display %s as standard" % str(size)

    number = len(languages)
    if number%numberPerLine == 0 :
    	total = (size[0]*numberPerLine, size[1]*(number/numberPerLine))
    else :
    	total = (size[0]*numberPerLine, size[1]*(number/numberPerLine+1))
    font = None
    try:
        font = ImageFont.truetype("DejaVuSansMono.ttf", 25)
    except:
        print "failed to load ImageFont!!"

    for p in pkg.keys():
        if package and package != p: continue
        print '%6d : %s' % (len(pkg[p].keys()), p)
        for file in pkg[p].keys():
            try:
                im = Image.new("RGB", total)
                n = 0
                for l in languages:
                    box = (size[0]*(n%numberPerLine),size[1]*(n/numberPerLine),size[0]*(n%numberPerLine+1),size[1]*(n/numberPerLine+1))
                    try:
                        pic = utils1.compose((path, l, p, file))
                        img = Image.open(pic).resize(size)
                        im.paste(img, box)
                    except:
                        print "failed to open pic %s" % (pic)
                    try:
                        draw = ImageDraw.Draw(im)
                        tsize = draw.textsize(l, font=font)
                        pos = (size[0]*(n%numberPerLine+1)-tsize[0],size[1]*(n/numberPerLine)+tsize[1])
                        draw.text(pos, l, font=font, fill="yellow")
                    except:
                        print "failed to draw text %s" % l
                    n += 1
                np = utils1.compose((new_path, p))
                utils1.mkdir(np)

                npf = utils1.compose((np, file))
                npf, ext = os.path.splitext(npf)
                npf = npf+".jpeg"

                im.save(npf, "JPEG")

            except:
                print "failed in saving: %s/%s/%s" % (new_path, p, file)

    print "Combination Done. Cost time: %ds" % (time.time()-start)
