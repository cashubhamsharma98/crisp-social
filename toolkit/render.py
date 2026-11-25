import sys, subprocess, numpy as np, io, os
from PIL import Image
from playwright.sync_api import sync_playwright
mode=sys.argv[1]; HTML=os.environ.get('HTML','reel.html')
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--allow-file-access-from-files'])
    pg=b.new_page(viewport={'width':1080,'height':1920})
    pg.goto('file:///home/claude/v3/'+HTML); pg.wait_for_timeout(800)
    dur=pg.evaluate('window.DURATION'); starts=pg.evaluate('window.VO_STARTS')
    def shot(t, q=None):
        pg.evaluate(f'window.seek({t})')
        return Image.open(io.BytesIO(pg.screenshot(type='jpeg',quality=95)))
    if mode=='stills':
        ts=[float(x) for x in sys.argv[2:]]
        ims=[shot(t).resize((360,640)) for t in ts]
        c=Image.new('RGB',(370*len(ims),640),'#777')
        for i,im in enumerate(ims): c.paste(im,(i*370,0))
        c.save('stills.png'); print(dur,starts)
    else:
        FPS=30; SUB=int(sys.argv[2]) if len(sys.argv)>2 else 2
        tmp='video.part.mp4'
        ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p',tmp],stdin=subprocess.PIPE)
        n=int(round(dur*FPS))
        for i in range(n):
            acc=None
            for s in range(SUB):
                a=np.asarray(shot(i/FPS + s/(FPS*SUB)*0.5).convert('RGB'),dtype=np.float32)
                acc=a if acc is None else acc+a
            ff.stdin.write((acc/SUB).astype(np.uint8).tobytes())
        ff.stdin.close(); ff.wait()
        if ff.returncode==0: os.rename(tmp,'video.mp4')
        print(dur,n)
    b.close()
