from datasets import load_dataset

DATASET_NAME = "hotchpotch/JaCWIR"


def load_ds():
    return load_dataset(DATASET_NAME, "eval", split="eval"), load_dataset(
        DATASET_NAME, "collection", split="collection"
    )


def load_df():
    eval_ds, collection_ds = load_ds()
    collection_df = collection_ds.to_pandas()  # type: ignore
    collection_df = collection_df.rename(columns={"description": "text"})  # type: ignore
    collection_dict = collection_df.set_index("doc_id").to_dict(orient="index")

    def get_contents(doc_id):
        data = collection_dict[doc_id]
        return {
            "title": data["title"],
            "text": data["text"],
            "doc_id": doc_id,
        }

    def expand_eval(example):
        q_id = "q_id##" + example["positive"][0]
        question = example["query"][0]
        positive = example["positive"][0]
        negatives = example["negatives"][0]
        labels = [1] + [0] * len(negatives)
        q_ids = [q_id] * (1 + len(negatives))
        questions = [question] * (1 + len(negatives))
        positive_data = get_contents(positive)
        negatives_data = [get_contents(n) for n in negatives]
        return {
            "question": questions,
            "q_id": q_ids,
            "doc_id": [positive_data["doc_id"]] + [n["doc_id"] for n in negatives_data],
            "title": [positive_data["title"]] + [n["title"] for n in negatives_data],
            "text": [positive_data["text"]] + [n["text"] for n in negatives_data],
            "label": labels,
        }

    eval_ds = eval_ds.map(
        expand_eval,
        num_proc=4,  # type: ignore
        remove_columns=eval_ds.column_names,  # type: ignore
        batch_size=1,
        batched=True,
    )

    df_q_id = (
        eval_ds.to_pandas()  # type: ignore
        .groupby(["q_id", "question"])  # type: ignore
        .agg(  # type: ignore
            {"doc_id": list, "label": list, "text": list, "title": list}
        )
    )
    return df_q_id
