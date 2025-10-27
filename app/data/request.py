import asyncio

from app.data.models import (
    async_session,
    ImageDescription,
    Users,
    ProcessedImageDescriptions,
)
from sqlalchemy import select


DB_TIMEOUT = 10


async def get_user_by_id(user_id: int):
    """Выполняет запрос к БД для получения пользователя из базы по user_id."""
    try:
        async with async_session() as session:
            query = select(Users).where(Users.user_id == user_id)
            result = await asyncio.wait_for(session.execute(query), timeout=DB_TIMEOUT)
            return result.scalar_one_or_none()
    except asyncio.TimeoutError:
        print(f"Таймаут при получении пользователя {user_id}")
        return None
    except Exception as e:
        print(f"Ошибка получения пользователя: {e}")
        return None


async def add_user(user_id: int, username: str) -> None:
    """Добавляет пользователя в БД."""
    try:
        async with async_session() as session:
            user = Users(user_id=user_id, username=username)
            session.add(user)
            await asyncio.wait_for(session.commit(), timeout=DB_TIMEOUT)
    except asyncio.TimeoutError:
        print(f"Таймаут при добавлении пользователя {user_id}")
    except Exception as e:
        print(f"Ошибка добавления пользователя: {e}")


async def get_all_image_descriptions():
    """Получает все записи из ImageDescription"""
    try:
        async with async_session() as session:
            query = select(ImageDescription)
            result = await asyncio.wait_for(session.execute(query), timeout=DB_TIMEOUT)
            return result.scalars().all()
    except asyncio.TimeoutError:
        print("Таймаут при получении всех описаний")
        return []
    except Exception as e:
        print(f"Ошибка получения всех описаний: {e}")
        return []


async def get_processed_image_ids():
    """Получает ID уже обработанных записей"""
    try:
        async with async_session() as session:
            query = select(ProcessedImageDescriptions.id)
            result = await asyncio.wait_for(session.execute(query), timeout=DB_TIMEOUT)
            return [row[0] for row in result]
    except asyncio.TimeoutError:
        print("Таймаут при получении обработанных ID")
        return []
    except Exception as e:
        print(f"Ошибка получения обработанных ID: {e}")
        return []


async def add_processed_image_description(image_desc: ImageDescription):
    """Добавляет запись в ProcessedImageDescriptions"""
    try:
        async with async_session() as session:
            processed_record = ProcessedImageDescriptions(
                id=image_desc.id,
                name=image_desc.name,
                extension=image_desc.extension,
                description=image_desc.description,
            )
            session.add(processed_record)
            await asyncio.wait_for(session.commit(), timeout=DB_TIMEOUT)
    except asyncio.TimeoutError:
        print(f"Таймаут при добавлении описания {image_desc.id}")
    except Exception as e:
        print(f"Ошибка добавления в обработанные: {e}")
