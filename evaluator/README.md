# JaQIR 評価用コード

JaQIR の評価を行うためのサンプルコードです。

## 評価の実行方法

`main.py` を実行することで、各種モデルの評価を行うことができます。初回の実行前は、必要なライブラリのインストールが必要です。

```
pip install -r requirements.txt
```

### 実行例

実行例は以下です。`-m` オプション以下に、モデルを指定することで評価できます。なお、一回実行した結果のデータは `data/eval_results/runs/` 以下に保存され、このデータを 2 回目からは利用します。データの再利用をしたく無い場合は、`--no_cache` オプションをつけて実行ください。

```
python main.py -m \
    BAAI/bge-m3+all \
    BAAI/bge-m3+colbert \
    bclavie/JaColBERTv2 \
    bm25 \
    cl-nagoya/sup-simcse-ja-base \
    corrius/cross-encoder-mmarco-mMiniLMv2-L12-H384-v1 \
    intfloat/multilingual-e5-large \
    pkshatech/GLuCoSE-base-ja \
    text-embedding-3-small
```

### オプション

`-r` で指標メトリクスの指定ができます。内部で検索ランキング評価ライブラリの[ranx](https://github.com/amenra/ranx)を使っているため、[ranx のメトリクス](https://amenra.github.io/ranx/metrics/) の指定が可能です。

例:

```
python main.py -r "map@20,hit_rate@20" -m \
    BAAI/bge-m3+all \
    intfloat/multilingual-e5-large
```

`-f` で出力フォーマットの指定ができます。標準は table です。csv や markdown, markdown_with_links 等々、コピペに便利な出力も指定できます。

```
python main.py -f csv -m \
    BAAI/bge-m3+all \
    intfloat/multilingual-e5-large
```

`-d` で、件数を 20 件に絞ってデバッグ用に実行することもできます。新しいモデルを試す際などにご利用ください。なお、通常実行した結果が保存され残ってしまうので、とりわけデバッグ時には `--no_cache` をつけてご利用ください。

```
python main.py -d -m bm25 --no_cache
```

その他のオプションは `-h` をご覧ください

## ライセンス

この評価コードのライセンスは [./LICENSE](./LICENSE) の通りの MIT License となっています。
