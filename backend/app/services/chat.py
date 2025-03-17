from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma

from ..models.models import Chat, ChatMessage, Content
from ..schemas.chat import ChatCreate, ChatMessageCreate
from ..core.config import settings


class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=settings.OPENAI_MODEL,
            temperature=0.7
        )
        self.embeddings = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    def create_chat(self, chat_in: ChatCreate) -> Chat:
        chat = Chat(**chat_in.model_dump())
        self.db.add(chat)
        self.db.commit()
        self.db.refresh(chat)
        return chat

    def get_chat(self, chat_id: int) -> Optional[Chat]:
        return self.db.query(Chat).filter(Chat.id == chat_id).first()

    def create_message(self, message_in: ChatMessageCreate) -> ChatMessage:
        message = ChatMessage(**message_in.model_dump())
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    async def process_message(
        self, chat_id: int, user_message: str
    ) -> Dict[str, Any]:
        # Get relevant content from the database
        relevant_content = self._get_relevant_content(user_message)
        
        # Prepare conversation context
        context = self._prepare_context(relevant_content)
        
        # Create system message with context
        system_prompt = f"""You are Cindy, an AI learning assistant. Your role is to help students understand their learning materials.
        Use the following context to answer the student's question. If the context doesn't contain enough information,
        say so and try to provide general guidance based on the topic.
        
        Context:
        {context}
        """
        
        # Create chat prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}")
        ])
        
        # Generate response
        chain = prompt | self.llm
        response = await chain.ainvoke({"input": user_message})
        
        # Save user message
        user_msg = self.create_message(
            ChatMessageCreate(
                chat_id=chat_id,
                role="user",
                content=user_message
            )
        )
        
        # Save assistant response
        assistant_msg = self.create_message(
            ChatMessageCreate(
                chat_id=chat_id,
                role="assistant",
                content=response.content,
                content_metadata={"sources": [c.metadata for c in relevant_content]}
            )
        )
        
        return {
            "message": assistant_msg,
            "context": {"text": context} if context else None,
            "sources": [c.metadata for c in relevant_content]
        }

    def _get_relevant_content(self, query: str, top_k: int = 3) -> List[Document]:
        # Get only the most recently added content
        content = self.db.query(Content).order_by(Content.created_at.desc()).first()
        
        if not content:
            return []
        
        documents = []
        chunks = self.text_splitter.split_text(content.content_text)
        for chunk in chunks:
            documents.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "title": content.title,
                        "source_url": content.source_url,
                        "content_type": content.content_type,
                        **(content.content_metadata or {})
                    }
                )
            )
        
        vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            collection_name="content_chunks"
        )
        
        return vectorstore.similarity_search(query, k=top_k)

    def _prepare_context(self, relevant_docs: List[Document]) -> str:
        if not relevant_docs:
            return "No relevant context found."
        
        context_parts = []
        for i, doc in enumerate(relevant_docs, 1):
            context_parts.append(f"Source {i}:")
            context_parts.append(f"Title: {doc.metadata.get('title', 'Unknown')}")
            context_parts.append(f"Content: {doc.page_content}\n")
        
        return "\n".join(context_parts) 