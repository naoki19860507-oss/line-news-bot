# 朝のニュース通知bot セットアップ手順

日経新聞・NewsPicks・ビジネスインサイダー・Yahoo!ニュース・ITmediaの最新記事リンクを、
平日朝8:00(JST)に自動でLINEへ送信します。

## 必要なもの
- GitHubアカウント（無料）
- LINE公式アカウントのチャネルアクセストークン（取得済み）
- 自分のLINEユーザーID（取得済み）

## セットアップ手順

### ① GitHubリポジトリを作成
1. https://github.com にログイン（アカウントがなければ新規登録・無料）
2. 右上「+」→「New repository」
3. リポジトリ名を入力（例: `line-news-bot`）→ 「Public」または「Private」どちらでもOK
4. 「Create repository」をクリック

### ② このフォルダの中身をアップロード
以下の3ファイルをリポジトリにアップロードしてください（GitHubの「Add file」→「Upload files」からドラッグ&ドロップで簡単にできます）。

- `news_notify.py`
- `.github/workflows/notify.yml`
- `README.md`

※ `.github/workflows/notify.yml` はフォルダ構造ごとアップロードする必要があります。GitHub上で直接「Create new file」を選び、ファイル名の欄に `.github/workflows/notify.yml` と入力すると、フォルダごと自動生成されます。

### ③ トークンとIDを安全に登録（GitHub Secrets）
1. リポジトリ画面上部の「Settings」タブを開く
2. 左メニュー「Secrets and variables」→「Actions」
3. 「New repository secret」を2回使って、以下を登録
   - Name: `LINE_CHANNEL_ACCESS_TOKEN` / Value: （取得したチャネルアクセストークン）
   - Name: `LINE_USER_ID` / Value: （取得した自分のユーザーID）

これでトークンはコードに直接書かれず、安全に保管されます。

### ④ 動作テスト
1. リポジトリの「Actions」タブを開く
2. 左メニューの「朝のニュース通知」をクリック
3. 右側の「Run workflow」ボタン→再度「Run workflow」で手動実行
4. 数十秒後、LINEに通知が届けば成功です

### ⑤ 自動実行の確認
設定後は、毎週月〜金曜日の朝8:00(JST)に自動で通知が届きます。追加の操作は不要です。

## カスタマイズ
- `news_notify.py` の `ARTICLES_PER_SOURCE` の数字を変えると、1サイトあたりの記事数を調整できます（初期値3）。
- `SOURCES` リストにサイトを追加・削除することも可能です。
