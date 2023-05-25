"""Build utilities of SageMaker endpoint usage
for LangChain
"""
import json
import os
from typing import Dict, Optional, Tuple

from langchain import SagemakerEndpoint
from langchain.llms.sagemaker_endpoint import LLMContentHandler


class ContentHandler(LLMContentHandler):
    content_type = "application/json"
    accepts = "application/json"

    def transform_input(self, prompt: str, model_kwargs: dict) -> bytes:
        input_str = json.dumps(
            {
                "instruction": "与えられたドキュメントの情報をベースとして、質問内容に対する詳細な回答を生成してください。ドキュメントの中に情報が存在しなければ、「わかりません」と回答してください。",
                "input": prompt,
                **model_kwargs,
            }
        )
        print("prompt: ", prompt)
        return input_str.encode("utf-8")

    def transform_output(self, output: bytes) -> str:
        response_json = json.loads(output.read().decode("utf-8"))
        return response_json.replace("<NL>", "\n")


def make_sagemaker_backed_llm(
    endpoint_name: str, aws_region: str, model_kwargs: Optional[Dict[str, float]]
) -> SagemakerEndpoint:
    """return sagemaker backed llm"""
    if not model_kwargs:
        model_kwargs = {}
    content_handler = ContentHandler()
    llm = SagemakerEndpoint(
        endpoint_name=endpoint_name,
        region_name=aws_region,
        model_kwargs=model_kwargs,
        content_handler=content_handler,
    )
    return llm
