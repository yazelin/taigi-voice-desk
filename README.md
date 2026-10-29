# 台語配音確認台

替台語台詞配音時，一句一句聽、改唸法、標通過或重做，再把結果交回給 AI 重產。

確認頁：https://yazelin.github.io/taigi-voice-desk/

## 流程

1. 準備一個資料夾，放 `lines.json`（格式見 [SKILL.md](SKILL.md)，或看 `examples/ato/`）。
2. 產音：`python3 voice.py 資料夾`。台語漢字經[意傳](https://ithuan.tw/)轉成台羅，再合成成 `audio/<id>.mp3`。要換成角色的聲音就加 `--vc '換聲指令 {src} {dst}'`。
3. 開確認頁，按「開資料夾」：
   - 每個字上面標著意傳的讀音，唸錯一眼看得出是哪個字
   - 改台羅，按「照台羅試聽」當場聽
   - 鍵盤操作：方向鍵換句、空白鍵播、`1` 通過、`2` 重做、`N` 寫備註
4. 按「存回 lines.json」（Chrome、Edge 直接寫回資料夾，其他瀏覽器會下載），再按「複製給 AI」貼給 AI。AI 只重產標了重做的句子。

只用 Python 標準函式庫與 ffmpeg（換聲才需要），不用安裝套件。

## 給 AI

[SKILL.md](SKILL.md) 寫了 AI 該怎麼建 `lines.json`、怎麼處理作者的修改。Claude Code 可以裝成 skill：

```bash
git clone https://github.com/yazelin/taigi-voice-desk ~/taigi-voice-desk
ln -s ~/taigi-voice-desk ~/.claude/skills/taigi-voice-desk
```

Codex、Gemini 直接讀 `SKILL.md` 照做即可。

## 授權

程式 MIT © 林亞澤。範例台詞出自《餘燼》（[larch-ember](https://github.com/yazelin/larch-ember)，CC BY-NC 4.0）。

---

[GitHub](https://github.com/yazelin) · [Facebook](https://www.facebook.com/yaze.lin.gm) · [請亞澤喝咖啡](https://buymeacoffee.com/yazelin) · [亞澤的部落格](https://yazelin.github.io/)
