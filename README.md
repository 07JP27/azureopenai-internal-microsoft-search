[English](./README_en.md)

# Microsoft Search API RAG サンプルアプリ

このサンプルは[Azure-Samples/azure-search-openai-demo](https://github.com/Azure-Samples/azure-search-openai-demo)をベースに開発されています。


## 概要
<!--ここにスクショを入れる-->

### 機能
- Microsoft 365内のドキュメントやサイト、Teamsの投稿などを基にしたLLMによるチャット形式の内部ナレッジ検索
- Microsoft 365でも使用されるMicrosoft Search APIを使用したシンプルかつ高精度なRAGアーキテクチャ
- [On-Behalf-Of フロー](https://learn.microsoft.com/ja-jp/entra/identity-platform/v2-oauth2-on-behalf-of-flow)を使用してユーザーの権限に応じた検索

### 技術概要
アーキテクチャ
![](./assets/overview_en.png)

シーケンス
![](./assets/sequence_en.png)


## セットアップ方法




https://learn.microsoft.com/ja-jp/graph/sdks/choose-authentication-providers?tabs=python#on-behalf-of-provider