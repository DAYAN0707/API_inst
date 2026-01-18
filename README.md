# FastAPI基礎セットアップ課題

FastAPIの学習用として、データの受け渡しや入力チェックの基本を実装したAPIです。<br>
現在はSwagger UIを通じて、データのやり取りが正しく行われることを確認する段階です。

## 実施内容

1. **基本エンドポイント**: GETリクエストによるハローワールドの実装
2. **クエリパラメータ**: `limit` や `active` を用いたデータのフィルタリング
3. **PydanticモデルによるPOSTリクエスト**: リクエストボディのバリデーション
4. **エラーハンドリング**: `HTTPException` を使用したカスタムエラーメッセージ（400 Bad Request）の実装
5. **詳細なバリデーション**: `Query` を使用した文字数制限（min_length/max_length）や数値範囲制限（ge/le）の実装

## 使用技術
* Python 3.x
* FastAPI
* Uvicorn (ASGI サーバー)
* Pydantic (データバリデーション)

## セットアップと起動方法

このプロジェクトをローカル環境で実行する手順です。

1. **リポジトリをクローンまたはダウンロードする**

2. **仮想環境を作成し、有効化する**
    ```bash
    python -m venv fastapi-env
    # Windowsの場合
    fastapi-env\Scripts\activate
    uvicorn main:app --reload
    
