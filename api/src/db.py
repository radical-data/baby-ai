from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, Text, DateTime, func
from sqlalchemy.sql import text
from contextlib import asynccontextmanager


Base = declarative_base()


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    message = Column(Text, nullable=False)


DATABASE_URL = "sqlite+aiosqlite:///./messages.db"
engine = create_async_engine(DATABASE_URL, echo=True)

async_session_maker = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def get_session():
    async with async_session_maker() as session:
        yield session


async def add_message(message_text: str):
    async with get_session() as session:
        message = Message(message=message_text)
        session.add(message)
        await session.commit()


async def get_all_messages():
    async with get_session() as session:
        result = await session.execute(text("SELECT * FROM messages"))
        messages = result.fetchall()
        return [
            {"id": row.id, "timestamp": row.timestamp, "message": row.message}
            for row in messages
        ]


async def clear_messages():
    async with get_session() as session:
        await session.execute("DELETE FROM messages")
        await session.commit()
