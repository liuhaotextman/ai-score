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
        # Use GradeResponse schema for controlled generation
        from schemas.grading import GradeResponse
        
        system_instruction = """
        你是一个专业的阅卷老师。你的任务是根据提供的【参考知识库】对【学生回答】进行评分（0-100分）。
        请仔细阅读 <question>、<context> 和 <answer> 标签中的内容，并给出客观的评分和理由。
        如果参考知识库不足以支持评分，请基于你的通用知识进行补充。
        """
        
        prompt = f"""
        <question>{question}</question>
        <context>{context}</context>
        <answer>{answer}</answer>
        """
        
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=GradeResponse
            )
        )
        # In JSON mode, response.text is guaranteed to be a valid JSON string
        return response.text

gemini_service = GeminiService()
