from deepeval.models.base_model import DeepEvalBaseLLM


class LangChainJudge(DeepEvalBaseLLM):

    def __init__(self, llm):
        self.llm = llm

    def load_model(self):
        return self.llm

    def generate(self, prompt: str) -> str:
        response = self.llm.invoke(prompt)

        content = response.content

        if isinstance(content, str):
            return content

        if isinstance(content, list):
            return "".join(
                block.get("text", "")
                for block in content
                if isinstance(block, dict)
                and block.get("type") == "text"
            )

        return str(content)

    async def a_generate(self, prompt: str) -> str:
        response = await self.llm.ainvoke(prompt)

        content = response.content

        if isinstance(content, str):
            return content

        if isinstance(content, list):
            return "".join(
                block.get("text", "")
                for block in content
                if isinstance(block, dict)
                and block.get("type") == "text"
            )

        return str(content)

    def get_model_name(self):
        return "LangChain Bedrock Judge"