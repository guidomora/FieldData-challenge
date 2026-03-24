import asyncio

from app.core.database import SessionFactory
from app.seeds import seed_demo_data


async def main() -> None:
    async with SessionFactory() as session:
        await seed_demo_data(session)


if __name__ == "__main__":
    asyncio.run(main())

