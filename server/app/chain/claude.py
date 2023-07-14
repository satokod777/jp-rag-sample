# Copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: LicenseRef-.amazon.com.-AmznSL-1.0
# Licensed under the Amazon Software License  http://aws.amazon.com/asl/
import os
from typing import List

from langchain.chains import LLMChain
from langchain.chat_models import ChatAnthropic
from langchain.prompts import PromptTemplate
from schemas import KendraDocument, LLMWithDocReqBody

ANTHROPIC_API_KEY: str = os.environ.get("ANTHROPIC_API_KEY", None)


def build_claude_chain():
    claude = ChatAnthropic(anthropic_api_key=ANTHROPIC_API_KEY)
    prompt = PromptTemplate(
        template="""Human: 資料:
{context}
上記の資料をもとに以下の質問に回答しなさい。[0]の形式で参考にした資料を示しなさい。また資料がないものは「わかりません」と答えなさい。\n質問: 
{question}

Assistant:""",
        input_variables=["context", "question"],
    )
    return LLMChain(llm=claude, prompt=prompt)


def build_claude_chain_without_doc():
    """context が与えられていない場合、 Contextを含めない Prompt とする Chain"""
    claude = ChatAnthropic(anthropic_api_key=ANTHROPIC_API_KEY)
    prompt = PromptTemplate(
        template="""Human: {question}

Assistant:""",
        input_variables=["question"],
    )
    return LLMChain(llm=claude, prompt=prompt)


def run_claude_chain(chain: LLMChain, body: LLMWithDocReqBody):
    return chain.run(
        context=_make_context_for_claude_from_docs(body.documents),
        question=body.userUtterance,
    )


def _make_context_for_claude_from_docs(documents: List[KendraDocument]):
    """与えられた Document 情報から claude のプロンプトに埋め込むための context 情報を作成する"""
    context: str = ""
    for doc_id, doc in enumerate(documents):
        context += f"[{doc_id}]{doc.title}\n{doc.excerpt}\n"
    return context
