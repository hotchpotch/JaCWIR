from pathlib import Path

from evaluator.args_parser import parse_args
from evaluator.load_data import load_df
from evaluator.logger import get_logger
from evaluator.reporter import compare_report, reporters
from evaluator.runner import runner

DEFAULT_CACHE_PATH = Path(__file__).parent / "data/eval_results"


def main():
    args = parse_args()
    logger = get_logger()
    if args["verbose"] or args["debug"]:
        logger.setLevel("DEBUG")
    n_samples = None
    if args["debug"]:
        n_samples = 20

    if args["no_cache"]:
        cache_path = None
    else:
        cache_path = DEFAULT_CACHE_PATH
        if args["debug"]:
            cache_path = cache_path / "debug"

    reporter = reporters[args["output_format"]]
    reranker_names = []
    for reranker_name in args["models"]:
        if isinstance(reranker_name, list):
            reranker_name = "".join(reranker_name)
        reranker_names.append(reranker_name)

    df = load_df()
    logger.info(f"Load: total -> {len(df)}")
    if n_samples is not None:
        df = df.head(n_samples)
        logger.info(f"Use {n_samples} samples for debug mode")

    qrel, runs = runner(
        reranker_names=reranker_names,
        df=df,
        cache_path=cache_path,
        kwargs=args["kwargs"],
    )

    report_metrics = args["report_metrics"].split(",")
    max_p = args["max_p_value"]
    report = compare_report(
        qrels=qrel,
        runs=runs,
        metrics=report_metrics,
        max_p=max_p,
    )

    report_text = reporter(report, reranker_names)
    print(report_text)


if __name__ == "__main__":
    main()
