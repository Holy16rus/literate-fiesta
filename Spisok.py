from telethon.tl.types import Message  # type: ignore
from .. import loader, utils

@loader.tds
class ContentManager(loader.Module):
    """Module for managing content categories such as movies, series, anime, and manga."""

    strings = {
        "name": "ContentManager",
        "added": "💾 <b>Добавлено:</b>\n<code>{}</code>",
        "removed": "🗑️ <b>Удалено:</b>\n<code>{}</code>",
        "updated": "🔄 <b>Обновлено:</b>\n<code>{}</code>",
        "no_content": "🚫 <b>Не указано название контента.</b>",
        "no_item": "🚫 <b>Элемент не найден.</b>",
        "available_categories": "📂 <b>Доступные категории:</b>\n1. Фильм\n2. Дорама\n3. Аниме\n4. Манга\n5. Сериал",
        "all_items": "📜 <b>Все ваши элементы:</b>\n",
        "no_items": "😔 <b>У вас нет элементов.</b>",
        "deleted_all": "🗑️ <b>Все элементы в категории '{}</b> были удалены.",
        "confirm_delete_all": "🔄 <b>Вы уверены, что хотите удалить все элементы в категории '{}</b>? (Да/Нет)",
    }

    async def client_ready(self):
        self._items = self.get("items", {})  # {category: [titles]}

    async def add_content(self, category: str, title: str, season: str, episode: str):
        """Helper function to add content to a specified category."""
        full_title = f"<code>{title}</code> сезон: <code>{season}</code> серия: <code>{episode}</code>"

        if category not in self._items:
            self._items[category] = []

        # Добавляем новый элемент в начало списка
        self._items[category].insert(0, full_title)
        self.set("items", self._items)
        return full_title

    @loader.command(ru_doc=".фильм <title> [часть] - Добавить фильм")
    async def фильм(self, message: Message):
        """Add a movie to the list"""
        args = utils.get_args_raw(message).strip()
        parts = args.split(' ')

        if not parts:
            await utils.answer(message, self.strings("no_content"))
            return

        title = ' '.join(parts[:-1]).strip()  # Название фильма
        part = parts[-1].strip() if parts[-1].isdigit() else ""  # Последний элемент как часть, если это число

        full_title = f"<code>{title}</code>{' часть: <code>{}</code>'.format(part) if part else ''}"

        if part:
            full_title = f"<code>{title}</code> часть: <code>{part}</code>"

        await self.add_content("фильм", title, part or "1", part or "1")
        await utils.answer(message, self.strings("added").format(full_title))

    @loader.command(ru_doc=".аниме <title> <season> <episode> - Добавить аниме")
    async def аниме(self, message: Message):
        """Add anime to the list"""
        args = utils.get_args_raw(message).strip()
        parts = args.split(' ')

        if len(parts) < 3:
            await utils.answer(message, self.strings("no_content"))
            return

        title = ' '.join(parts[:-2]).strip()
        season = parts[-2].strip()
        episode = parts[-1].strip()

        full_title = await self.add_content("аниме", title, season, episode)
        await utils.answer(message, self.strings("added").format(full_title))

    @loader.command(ru_doc=".дорама <title> <season> <episode> - Добавить дораму")
    async def дорама(self, message: Message):
        """Add a drama to the list"""
        args = utils.get_args_raw(message).strip()
        parts = args.split(' ')

        if len(parts) < 3:
            await utils.answer(message, self.strings("no_content"))
            return

        title = ' '.join(parts[:-2]).strip()
        season = parts[-2].strip()
        episode = parts[-1].strip()

        full_title = await self.add_content("дорама", title, season, episode)
        await utils.answer(message, self.strings("added").format(full_title))

    @loader.command(ru_doc=".манга <title> <episode> - Добавить мангу")
    async def манга(self, message: Message):
        """Add manga to the list"""
        args = utils.get_args_raw(message).strip()
        parts = args.split(' ')

        if len(parts) < 2:
            await utils.answer(message, self.strings("no_content"))
            return

        title = ' '.join(parts[:-1]).strip()
        episode = parts[-1].strip()

        full_title = await self.add_content("манга", title, "1", episode)  # Сезон по умолчанию "1"
        await utils.answer(message, self.strings("added").format(full_title))

    @loader.command(ru_doc=".сериал <title> <season> <episode> - Добавить сериал")
    async def сериал(self, message: Message):
        """Add a series to the list"""
        args = utils.get_args_raw(message).strip()
        parts = args.split(' ')

        if len(parts) < 3:
            await utils.answer(message, self.strings("no_content"))
            return

        title = ' '.join(parts[:-2]).strip()
        season = parts[-2].strip()
        episode = parts[-1].strip()

        full_title = await self.add_content("сериал", title, season, episode)
        await utils.answer(message, self.strings("added").format(full_title))

    @loader.command(ru_doc="<category> <title> - Удалить контент из категории")
    async def removecontent(self, message: Message):
        """<category> <title> <season> <episode> - Remove content from a category"""
        args = utils.get_args_raw(message).strip()

        if not args:
            await utils.answer(message, self.strings("no_content"))
            return

        parts = args.split(' ')
        category = parts[0].strip().lower()
        title = ' '.join(parts[1:-2]).strip()  # Соединяем название
        season = parts[-2].strip()  # Число для сезона
        episode = parts[-1].strip()  # Число для номера серии

        if not title:
            await utils.answer(message, self.strings("no_content"))
            return

        full_title = f"<code>{title}</code> сезон: <code>{season}</code> серия: <code>{episode}</code>"

        if category in self._items and full_title in self._items[category]:
            self._items[category].remove(full_title)
            self.set("items", self._items)
            await utils.answer(message, self.strings("removed").format(full_title))
        else:
            await utils.answer(message, self.strings("no_item"))

    @loader.command(ru_doc="<category> - Удалить все элементы в категории")
    async def removeall(self, message: Message):
        """<category> - Remove all content from a category"""
        args = utils.get_args_raw(message).strip()

        if not args:
            await utils.answer(message, self.strings("no_content"))
            return

        category = args.strip().lower()

        if category in self._items:
            await utils.answer(message, self.strings("confirm_delete_all").format(category))
            del self._items[category]  # Удаляем все элементы в категории
            self.set("items", self._items)
            await utils.answer(message, self.strings("deleted_all").format(category))
        else:
            await utils.answer(message, "🚫 <b>Категория не найдена.</b>")

    @loader.command(ru_doc="Список всех доступных категорий контента")
    async def categories(self, message: Message):
        """List all available content categories"""
        await utils.answer(message, self.strings("available_categories"))

    @loader.command(ru_doc="Список всех элементов в категориях")
    async def listitems(self, message: Message):
        """List all items in categories"""
        result = self.strings("all_items")

        if not self._items:
            await utils.answer(message, self.strings("no_items"))
            return

        for category, titles in self._items.items():
            result += f"\n<b>{category.capitalize()}:</b>"
            for idx, title in enumerate(titles, start=1):
                result += f"\n{idx}. {title}"  # Нумерованный список

        await utils.answer(message, result)