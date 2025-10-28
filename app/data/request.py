import asyncio

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError

from app.data.models import (
    ImageDescription,
    ProcessedImageDescriptions,
    Users,
    async_session,
)

DB_TIMEOUT = 10


async def get_user_by_id(user_id: int):
    """Выполняет запрос к БД для получения пользователя из базы по user_id."""
    try:
        async with async_session() as session:
            query = select(Users).where(Users.user_id == user_id)
            result = await asyncio.wait_for(session.execute(query), timeout=DB_TIMEOUT)
            return result.scalar_one_or_none()
    except TimeoutError:
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
    except TimeoutError:
        print(f"Таймаут при добавлении пользователя {user_id}")
    except Exception as e:
        print(f"Ошибка добавления пользователя: {e}")


async def get_all_image_descriptions():
    """Получает все записи из ImageDescription"""
    try:
        async with async_session() as session:
            query = select(ImageDescription)
            result = await asyncio.wait_for(session.execute(query), timeout=60)
            return result.scalars().all()
    except TimeoutError:
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
            result = await asyncio.wait_for(session.execute(query), timeout=60)
            return set([row[0] for row in result])
    except TimeoutError:
        print("Таймаут при получении обработанных ID")
        return set()
    except Exception as e:
        print(f"Ошибка получения обработанных ID: {e}")
        return set()


async def add_processed_image_description(image_desc: ImageDescription):
    """Добавляет запись в ProcessedImageDescriptions"""
    try:
        async with async_session() as session:
            processed_record = ProcessedImageDescriptions(
                id=image_desc.id,
                name=image_desc.name,
                description=image_desc.description,
            )
            session.add(processed_record)
            await asyncio.wait_for(session.commit(), timeout=DB_TIMEOUT)
    except TimeoutError:
        print(f"Таймаут при добавлении описания {image_desc.id}")
    except Exception as e:
        print(f"Ошибка добавления в обработанные: {e}")


async def create_image_description(name: str, description: str) -> bool:
    """Вставляет новую запись в таблицу image_descriptions."""
    try:
        async with async_session() as session:
            new_record = ImageDescription(name=name, description=description)
            session.add(new_record)
            await asyncio.wait_for(session.commit(), timeout=DB_TIMEOUT)
            return True

    except TimeoutError:
        print(f"Ошибка: Превышено время ожидания ({DB_TIMEOUT} секунд) при сохранении в БД")
        return False

    except SQLAlchemyError as e:
        print(f"Ошибка базы данных при сохранении описания для {name}: {e}")
        return False

    except Exception as e:
        print(f"Неожиданная ошибка при сохранении описания для {name}: {e}")
        return False


async def add_image_description_with_id(name: str, description: str) -> bool:
    """Добавляет новую запись в таблицу image_descriptions с защитой от дублей по ID.

    Получает максимальный ID из таблицы, добавляет 1 и вставляет запись с новым ID.
    """
    try:
        async with async_session() as session:
            query = select(func.max(ImageDescription.id))
            result = await asyncio.wait_for(session.execute(query), timeout=DB_TIMEOUT)
            max_id = result.scalar()
            new_id = (max_id + 1) if max_id else 1

            new_record = ImageDescription(id=new_id, name=name, description=description)
            session.add(new_record)
            await asyncio.wait_for(session.commit(), timeout=DB_TIMEOUT)
            return True

    except TimeoutError:
        print(f"Ошибка: Превышено время ожидания ({DB_TIMEOUT} секунд) при сохранении в БД")
        return False

    except SQLAlchemyError as e:
        print(f"Ошибка базы данных при сохранении описания для {name}: {e}")
        return False

    except Exception as e:
        print(f"Неожиданная ошибка при сохранении описания для {name}: {e}")
        return False
