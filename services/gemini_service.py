from google import genai
from google.genai import types
from core.config import settings
from typing import List

class GeminiService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GeminiAPIKey)
        self.model_id = settings.Gemini.TextModel
        self.embedding_model_id = settings.Gemini.EmbeddingModel

    async def get_embedding(self, text: str) -> List[float]:
        # google-genai SDK embedding call
        response = self.client.models.embed_content(
            model=self.embedding_model_id,
            contents=text,
            config=types.EmbedContentConfig(output_dimensionality=768)
        )
        return response.embeddings[0].values

    async def generate_score(self, question: str, answer: str, context: str) -> str:
        system_instruction = """
        你是一个专业的老师，请根据提供的参考知识库内容对学生的回答进行评分（0-100分）。
        请给出评分，并给出简短的评语。返回格式必须为有效的 JSON: {"score": 85, "reason": "..."}
        如果参考知识库内容不足以支持评分，请基于你的通用知识进行评分，并在评语中注明。
        """
        
        prompt = f"""
        【试题内容】：
        {question}
        
        【参考知识库】：
        {context}
        
        【学生回答】：
        {answer}
        """
        
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction
            )
        )
        return response.text

gemini_service = GeminiService()
