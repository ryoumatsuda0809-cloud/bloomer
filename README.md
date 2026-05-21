# bloomers-brain

Bloomer の知識投入パイプライン。

## セットアップ（初回のみ）

```bash
pip install -r requirements.txt
```

## 実行方法

```bash
# 環境変数をセット
export SUPABASE_URL=https://xxxx.supabase.co
export SUPABASE_SERVICE_ROLE_KEY=eyJxxx
export GEMINI_API_KEY=AIzaxxx

# 投入実行
python scripts/embed.py
```

## GitHub Actions の設定（初回のみ）

1. GitHub リポジトリの Settings → Secrets and variables → Actions を開く
2. 以下の3つの Secret を追加する：
   - `SUPABASE_URL`
   - `SUPABASE_SERVICE_ROLE_KEY`
   - `GEMINI_API_KEY`
3. 設定完了後は `knowledge/` に `.md` を追加して push するだけで自動投入される

## knowledge/ フォルダの書き方

knowledge/ 配下に .md ファイルを作成します。
1ファイルに複数チャンクを書く場合は --- で区切ります。

```markdown
## トリガー
下関・南風泊市場

## 表層知識
日本最大のフグ集積地。

## 深層知識
袋セリという口頭のみの手作業取引が残っており
デジタル記録が存在しない。

## クエストの種
袋セリのデジタル記録・通知 PWA

---

## トリガー
別のチャンク

## 表層知識
...
```
