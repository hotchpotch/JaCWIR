
# JaCWIR: Japanese Casual Web IR - 日本語情報検索評価のための小規模でカジュアルなWebタイトルと概要のデータセット

近年、大規模言語モデル（LLM）の台頭により、一般的な日本語を用いた自然な検索クエリで質問するユースケースが増えています。しかしながら、多様なジャンルの Web 記事に対して、ユーザーの質問に適切に答えられるような情報検索システムを評価するための日本語データセットは十分ではありません。

JaCWIR は、5000の質問文と、約50万のWebページのタイトル・Webページ冒頭文もしくは概要(meta descriptionなど)で構成される短いデータの小規模な日本語の情報検索の評価データセットです。質問文は、50万Webページのどれかを元に作成しており、そのデータを質問文の正例としています。

データ元には日本最大級のソーシャルブックマークサービスである、[はてなブックマーク](https://b.hatena.ne.jp/)から収集した RSS 情報を元にフィルタリングし、様々な Web ジャンルの記事のタイトルや概要を含めています。それらの記事からサンプリングしたデータを元に ChatGPT 3.5 で質問文を作成し、日本語の情報検索評価用データセット "**JaCWIR** : Japanese Casual Web IR dataset" を構築しました。なお JaCWIR は「ジャクウィル」と読みます。

データセット自体は HuggingFace で、データセットの評価コード例などは GitHub で公開しています。

- 🤗 [JaCWIR](https://huggingface.co/datasets/hotchpotch/JaCWIR)
  - HuggingFace で公開している JaCWIR データセットです

- 🛠️ [JaCWIR GitHub リポジトリ](https://github.com/hotchpotch/JaCWIR/)
  - GitHub で、📈 [評価用コード](https://github.com/hotchpotch/JaCWIR/tree/main/evaluator) を公開しています。

## JaCWIR の特徴

JaCWIR は、Web の様々なジャンルの記事のタイトルや概要(description)を含む日本語のデータセットです。情報検索のための質問文は ChatGPT 3.5 を利用して作成されており、主に情報検索(IR)タスクでの評価利用を想定しています。

JaCWIR は、考え抜いてさまざまな視点で構築されたきちんとしたデータセットではなく、日本語のさまざまなWeb記事検索に対しての一つの評価指標の目安となるように作成したカジュアルなデータセットです。

データセットに含まれる title と description データは、collection url 先のデータに著作権が帰属します。また、query (質問文)のデータは ChatGPT 3.5 を利用して作成したため、OpenAI のコンペティションとなるモデル作成には利用できません。これらのことから、JaCWIR のデータは研究用・非商用として、情報検索の評価にご利用ください。

### 評価タスクと指標

JaCWIR は質問に対して、どの記事を元にその質問が作られたかを探す情報検索タスクです。全てのデータを使えば、50万件からのIRタスクとして評価できます。

また、もっと小規模な100件の IR / Rerank の評価用にと、データセットには各質問に対して正例 (positive) が1つと、BM25と文ベクトルモデルを使って hard-negative マイニングで抽出した誤った負例 (negatives) が99個含まれています。

Rerank タスクの評価指標としては、MAP@10 (Mean Average Precision at 10) を採用しています。MAP は、情報検索システムの評価でよく用いられる指標の一つで、ユーザーにとって重要な上位の結果の適合性を評価することに適しています。具体的には、各質問に対する上位10件の検索結果の適合性を平均することで、システム全体の性能を評価します。MAP を用いることで、単に正解が上位に来ているかだけでなく、上位の結果の順序も考慮した評価が可能になります。

また例として、簡単に評価できるスクリプトを [GitHub の evaluator]([https://github.com/hotchpotch/JaCWIR/tree/main/evaluator](https://github.com/hotchpotch/JaCWIR/tree/main/evaluator)) 以下に置いています。このスクリプトでは、一般的なインターフェイスを備えた検索モデルの評価が可能です。

## Rerank タスク評価

100件の Rerank タスクの評価は以下のとおりです。MAP@10の他に、参考までに HIT_RATE@10 も表示しています。

#### 密な文ベクトルモデル

| model_names                                                                     | map@10 | hit_rate@10 |
| :------------------------------------------------------------------------------ | -----: | ----------: |
| [text-embedding-3-small](https://platform.openai.com/docs/guides/embeddings)    | 0.8168 |      0.9506 |
| [unsup-simcse-ja-base](https://huggingface.co/cl-nagoya/unsup-simcse-ja-base)   | 0.4426 |       0.693 |
| [unsup-simcse-ja-large](https://huggingface.co/cl-nagoya/unsup-simcse-ja-large) | 0.4772 |      0.7188 |
| [sup-simcse-ja-base](https://huggingface.co/cl-nagoya/sup-simcse-ja-base)       | 0.5778 |      0.7976 |
| [sup-simcse-ja-large](https://huggingface.co/cl-nagoya/sup-simcse-ja-large)     | 0.4741 |      0.7164 |
| [GLuCoSE-base-ja](https://huggingface.co/pkshatech/GLuCoSE-base-ja)             | 0.6862 |      0.8706 |
| [GLuCoSE-base-ja-v2](https://huggingface.co/pkshatech/GLuCoSE-base-ja-v2)   |   0.8567 |        0.9676 |
| [fio-base-japanese-v0.1](https://huggingface.co/bclavie/fio-base-japanese-v0.1) | 0.6491 |      0.8544 |
| [bge-m3+dense](https://huggingface.co/BAAI/bge-m3)                              | 0.8642 |      0.9684 |
| [multilingual-e5-large](https://huggingface.co/intfloat/multilingual-e5-large)  | 0.8759 |      0.9726 |
| [multilingual-e5-small](https://huggingface.co/intfloat/multilingual-e5-small)  |  0.869 |        0.97 |
| [ruri-large](https://huggingface.co/cl-nagoya/ruri-large)                   |   0.8291 |        0.9594 |
| [ruri-base](https://huggingface.co/cl-nagoya/ruri-base)                     |   0.837  |        0.9584 |
| [ruri-small](https://huggingface.co/cl-nagoya/ruri-small)                   |   0.8428 |        0.9622 |
| [static-embedding-japanese](https://huggingface.co/hotchpotch/static-embedding-japanese) |   0.7642 |    0.9266 |


#### ColBERT モデル

| model_names                                               | map@10 | hit_rate@10 |
| :-------------------------------------------------------- | -----: | ----------: |
| [JaColBERTv2](https://huggingface.co/bclavie/JaColBERTv2) | 0.9185 |      0.9854 |
| [JaColBERT](https://huggingface.co/bclavie/JaColBERT)     | 0.9035 |      0.9772 |
| [bge-m3+colbert](https://huggingface.co/BAAI/bge-m3)      | 0.9064 |      0.9802 |

#### CrossEncoder モデル

| model_names                                                                                                              | map@10 | hit_rate@10 |
| :----------------------------------------------------------------------------------------------------------------------- | -----: | ----------: |
| [japanese-reranker-cross-encoder-xsmall-v1](https://huggingface.co/hotchpotch/japanese-reranker-cross-encoder-xsmall-v1) | 0.9376 |      0.9894 |
| [japanese-reranker-cross-encoder-small-v1](https://huggingface.co/hotchpotch/japanese-reranker-cross-encoder-small-v1)   |  0.939 |      0.9908 |
| [japanese-reranker-cross-encoder-base-v1](https://huggingface.co/hotchpotch/japanese-reranker-cross-encoder-base-v1)     | 0.9337 |      0.9878 |
| [japanese-reranker-cross-encoder-large-v1](https://huggingface.co/hotchpotch/japanese-reranker-cross-encoder-large-v1)   | 0.9364 |      0.9816 |
| [japanese-bge-reranker-v2-m3-v1](https://huggingface.co/hotchpotch/japanese-bge-reranker-v2-m3-v1)                       | 0.9372 |       0.992 |
| [bge-reranker-v2-m3](https://huggingface.co/BAAI/bge-reranker-v2-m3)                                                     | 0.9343 |      0.9914 |
| [shioriha-large-reranker](https://huggingface.co/cl-nagoya/shioriha-large-reranker)                                      | 0.8458 |      0.9562 |
| [bge-reranker-base](https://huggingface.co/BAAI/bge-reranker-base)                                                       | 0.4905 |      0.7334 |
| [bge-reranker-large](https://huggingface.co/BAAI/bge-reranker-large)                                                     | 0.7332 |      0.9314 |
| [cross-encoder-mmarco-mMiniLMv2-L12-H384-v1](https://huggingface.co/corrius/cross-encoder-mmarco-mMiniLMv2-L12-H384-v1)  | 0.9211 |       0.984 |
| [ruri-reranker-small](https://huggingface.co/cl-nagoya/cl-nagoya/ruri-reranker-small) |   0.93   |        0.982  |
| [ruri-reranker-base](https://huggingface.co/cl-nagoya/ruri-reranker-base)                         |   0.9388 |        0.9898 |
| [ruri-reranker-large](https://huggingface.co/cl-nagoya/ruri-reranker-large)                       |   0.9463 |        0.99   |

#### スパースベクトルモデル

| model_names                                         | map@10 | hit_rate@10 |
| :-------------------------------------------------- | -----: | ----------: |
| [japanese-splade-base-v1](https://huggingface.co/hotchpotch/japanese-splade-base-v1) |   0.9122 |        0.9854 |
| [bge-m3+sparse](https://huggingface.co/BAAI/bge-m3) | 0.8944 |      0.9778 |
| bm25                                                | 0.8408 |      0.9528 |


## ライセンス

JaCWIR データセットのライセンスは以下の通りです。

- eval の "query" の質問データ
	- [OpenAI のbusiness-terms(事業向け利用規約)]([https://openai.com/policies/business-terms](https://openai.com/policies/business-terms)) に従います
- collection の "title", "description" のデータ
	- ライセンスは collection の url に記載されている、Webページの制作者に帰属します

## おわりに〜謝辞

今回、JaCWIR データセットを構築しようと思ったのは、私が wikipedia の文章ばかりを学習させているモデルを作成している際、wikipedia の文章関連のタスクなら高スコアになるが、wikipediaドメイン外の文章になった途端にスコアが大きく落ちることに気づき、wikipediaを使っていないデータで評価したい、と思ったことがきっかけでした。そのため、wikipedia 以外のWebの多様な情報を活用した情報検索タスクを作って評価したい、と作成に着手しました。

結果、wikipedia に最適化しすぎないモデルも作成することができ、多様性や汎化性能の重要さに改めて気づくことができました。

なおデータ収集には、はてなブックマークが提供している RSS を利用させていただきました。このRSSがなければ、Webのさまざまな話題を収集する難易度が全く異なったことでしょう。有益なデータを公開してくださっている、株式会社はてなの皆様・はてなブックマークユーザーの皆様にお礼申し上げます。

---

## Citation

```
@misc{yuichi-tateno-2024-jacwir,
url={[https://huggingface.co/datasets/hotchpotch/JaCWIR](https://huggingface.co/datasets/hotchpotch/JaCWIR)},
title={JaCWIR: Japanese Casual Web IR - 日本語情報検索評価のための小規模でカジュアルなWebタイトルと概要のデータセット},
author={Yuichi Tateno}
}
```


