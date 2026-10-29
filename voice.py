"""台語配音產音：lines.json 裡每一句台語漢字 → 意傳轉台羅 → 意傳合成 → audio/<id>.mp3。

python3 voice.py examples/ato              # 資料夾裡要有 lines.json
python3 voice.py examples/ato --vc 'cmd {src} {dst}'   # 合成後再換聲（例如 Seed-VC），{src} {dst} 是 wav 路徑

要重產的句子：
- 改了台語漢字、台羅清空 → 重新轉台羅、重新合成
- status 是 "redo" → 照現在的台羅重新合成
其餘有音檔的句子不動。產完 status 改回 "todo"，等人在確認頁聽。
意傳是公開 demo，一分鐘大約 3 句，限流時等 65 秒再試。
"""
import argparse, json, os, subprocess, sys, time, urllib.parse, urllib.request

UA = {'User-Agent': 'Mozilla/5.0 taigi-voice-desk'}
GAP = 21   # 意傳一分鐘約 3 句


def req(url, data=None, timeout=90):
    for _ in range(5):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, data=data, headers=UA), timeout=timeout).read()
        except Exception as e:  # noqa: BLE001  限流回 500
            print('  意傳忙，65 秒後再試', repr(e)[:60], flush=True)
            time.sleep(65)
    raise RuntimeError('意傳一直失敗：' + url[:80])


def tau(hanzi):
    """台語漢字 → (台羅, 分詞)。GET 2026-10 起常回 500，用 POST。"""
    r = json.loads(req('https://hokbu.ithuan.tw/tau', urllib.parse.urlencode({'taibun': hanzi}).encode(), 60))
    return r['KIP'], r.get('分詞', '')


def synth(kip, path):
    open(path, 'wb').write(req('https://hapsing.ithuan.tw/bangtsam?' + urllib.parse.urlencode({'taibun': kip})))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('dir')
    ap.add_argument('--vc', help="換聲指令，{src} {dst} 會換成 wav 路徑")
    a = ap.parse_args()
    f = os.path.join(a.dir, 'lines.json')
    doc = json.load(open(f, encoding='utf-8'))
    os.makedirs(os.path.join(a.dir, 'audio'), exist_ok=True)
    save = lambda: open(f, 'w', encoding='utf-8').write(json.dumps(doc, ensure_ascii=False, indent=1) + '\n')
    for ln in doc['lines']:
        mp3 = os.path.join(a.dir, 'audio', ln['id'] + '.mp3')
        if ln.get('kip') and ln.get('status') != 'redo' and os.path.exists(mp3):
            continue
        if not ln.get('kip'):
            ln['kip'], ln['seg'] = tau(ln['hanzi'])
            print(ln['id'], '台羅', ln['kip'], flush=True)
            time.sleep(GAP)
        synth(ln['kip'], mp3)
        if a.vc:   # ponytail: 一句載一次模型，句子多再改成整批接起來換
            wav, out = mp3[:-4] + '.src.wav', mp3[:-4] + '.vc.wav'
            subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', mp3, '-ar', '22050', '-ac', '1', wav], check=True)
            subprocess.run(a.vc.format(src=wav, dst=out), shell=True, check=True)
            subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', out, '-af', 'loudnorm=I=-18:TP=-2', '-b:a', '96k', mp3], check=True)
            os.remove(wav); os.remove(out)
        ln['status'] = 'todo'
        ln['audio'] = 'audio/' + ln['id'] + '.mp3'
        print(ln['id'], '合成好', flush=True)
        save()
        time.sleep(GAP)
    save()
    print('done')


if __name__ == '__main__':
    sys.exit(main())
