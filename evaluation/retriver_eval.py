from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    ContextualRecallMetric,
    ContextualPrecisionMetric,
)

from app.rag.retrieve import vector_search,bm25_search
from app.llm.chat_model import get_chat_model
from app.llm.wrapper_evaluation import LangChainJudge

from evaluation.harness import (
    summarize_by_metric,
    print_summary,
)

import json


GOLDEN_DATA_PATH = (
    "/home/rajan/PROJECT_RAG/"
    "golden_dataset/rag_eval_golden_data.json.json"
)

THRESHOLD = 0.7
USER = "6aa19c3ef8275109cf7e1528"


llm = get_chat_model()
judge_llm = LangChainJudge(llm)


def run_test():

    # --------------------------------
    # Load golden dataset
    # --------------------------------

    with open(GOLDEN_DATA_PATH, "r", encoding="utf-8") as f:
        golden_data = json.load(f)

    print(f"Golden dataset size: {len(golden_data)}")

    test_cases = []

    # --------------------------------
    # Build test cases
    # --------------------------------

    for g in golden_data:

        retrieved = bm25_search(
            query=g["query"],
            user_id=USER,
        )

        retrieved_context = [
            ret["content"]
            for ret in retrieved
        ]

        print(
            f"Query: {g['query'][:60]} | "
            f"Retrieved: {len(retrieved_context)}"
        )

        test_cases.append(
            LLMTestCase(
                input=g["query"],
                actual_output="",
                expected_output=g["ideal_answer"],
                retrieval_context=retrieved_context,
            )
        )

    print(f"Total test cases: {len(test_cases)}")

    # --------------------------------
    # Metrics
    # --------------------------------

    metrics = [
        ContextualRecallMetric(
            threshold=THRESHOLD,
            model=judge_llm,
            include_reason=True,
        ),

        ContextualPrecisionMetric(
            threshold=THRESHOLD,
            model=judge_llm,
            include_reason=True,
        ),
    ]

    # --------------------------------
    # Evaluate ALL test cases
    # --------------------------------

    result = evaluate(
        test_cases=test_cases,
        metrics=metrics,
        hyperparameters={
            "retriever": "bm25_search",
            "embedding_model": "amazon.titan-embed-text-v2:0",
            "chunk_size": 1500,
            "chunk_overlap": 300,
            "top_k": 5,
            "judge_model": "LangChain Bedrock Judge",
            "golden_set": GOLDEN_DATA_PATH,
        },
    )

    # --------------------------------
    # Summarize
    # --------------------------------

    return summarize_by_metric(result)


def run_local():
    return run_test()


if __name__ == "__main__":
    print_summary(
        "retriever",
        run_local(),
    )