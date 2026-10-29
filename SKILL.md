---
name: taigi-voice-desk
description: 台語配音的產音與人工確認流程。台語漢字經意傳轉台羅、合成音檔（可再換聲），作者在確認頁逐句聽、改台羅、標通過或重做、寫備註，存回 lines.json 給 AI 接著改。當要替遊戲、影片、有聲書做台語台詞配音，或作者說「台語唸錯」「幫我配台語」「確認台語配音」時使用。
---

# 台語配音確認台

一句台詞走三步：**台語漢字 → 台羅 → 音檔**。台羅決定怎麼唸，所以作者確認的單位是台羅，不是音檔。

- 確認頁：https://yazelin.github.io/taigi-voice-desk/ （也可以本機直接開 `index.html`）
- 產音：`python3 voice.py <資料夾>`
- AI 與作者之間只交換一個檔：`<資料夾>/lines.json`

## 資料夾長這樣

```
<資料夾>/
  lines.json
  audio/<id>.mp3     ← voice.py 產的，不進 git
```

`lines.json`：

```json
{"title": "《餘燼》阿桃姨",
 "lines": [{"id": "9039df8cf2", "speaker": "阿桃姨",
            "hanzi": "淑靜仔，遮嘛沖一下。", "zh": "淑靜，這裡也沖一下。",
            "kip": "", "seg": "", "status": "todo", "note": "", "audio": ""}]}
```

| 欄位 | 誰寫 | 意思 |
|---|---|---|
| `id` | AI | 固定不變，音檔檔名就是它。沿用遊戲裡的台詞 id |
| `speaker`、`zh` | AI | 誰說的、華語意思（給作者對照，不唸） |
| `hanzi` | AI，作者可改 | 台語漢字。作者改了，確認頁會清空 `kip` |
| `kip` | voice.py，作者可改 | 台羅。空白代表要重新轉 |
| `seg` | voice.py | 意傳分詞，確認頁拿來在每個字上標讀音 |
| `status` | 作者 | `todo` 待聽、`ok` 通過、`redo` 重做 |
| `note` | 作者 | 哪裡唸錯、想要什麼語氣 |
| `audio` | voice.py | 音檔相對路徑 |

## AI 的流程

1. **建 lines.json**：一句一筆，`hanzi` 寫台語漢字，括號裡的華語註解拆到 `zh`，不要留在 `hanzi`（會被唸出來）。華語台詞不要放進來。
2. **產音**：`python3 voice.py <資料夾>`。意傳是公開 demo，一分鐘大約 3 句，要用 `run_in_background` 跑，等完成通知，不要自己輪詢。
3. **請作者確認**：叫作者開確認頁，按「開資料夾」選這個資料夾。Chrome、Edge 能直接存回 `lines.json`；Firefox、Safari 會下載一份新的 `lines.json`，請作者放回資料夾。
4. **作者貼「複製給 AI」的內容，或說存好了**：重讀 `lines.json`，處理 `status: "redo"` 的句子：
   - `kip` 空白：作者改了漢字，直接重跑 voice.py，它會重新轉台羅。
   - `kip` 有值：作者改過台羅，照作者的台羅重跑 voice.py。**不要把作者的台羅換回意傳的結果。**
   - 只有 `note`：照備註改。通常是改漢字（換一個意傳唸得對的寫法）或直接改台羅，改完把 `status` 留在 `redo` 再跑 voice.py。
5. 重跑以後 voice.py 會把這些句子改回 `todo`，請作者只聽這幾句。全部 `ok` 才算確認完。

## 換聲

意傳只有一種聲音。要換成角色的聲音就加 `--vc`，指令裡的 `{src}`、`{dst}` 會換成 wav 路徑：

```bash
python3 voice.py <資料夾> --vc 'ssh ct@192.168.11.11 ...seed-vc inference... {src} {dst}'
```

Seed-VC 一定要開音高控制（`--f0-condition True --auto-f0-adjust True`），不開會把音高拉到 140 Hz 上下，小孩聽起來像男人。目前是一句載一次模型；句子多時可以參考 larch-ember 的 `src/taigi.py`，把同一個參考聲音的句子接成一段一起換，再照秒數切回。

## 已知的坑

- 意傳的 `GET /tau` 2026-10 起常回 500，voice.py 用 POST。
- 意傳 API 沒開 CORS，網頁讀不到台羅轉換結果，所以台羅只能由 voice.py 轉。網頁上的「照台羅試聽」是直接把 `<audio>` 指到合成網址，這條不受 CORS 擋，作者改完台羅可以當場聽。
- 「照台羅試聽」是意傳原聲，沒有換聲；確認唸法用它，確認聲音要聽產好的音檔。
- 音檔不進 git（意傳 demo 的產出，授權沒寫清楚）。
