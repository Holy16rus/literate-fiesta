# meta developer: @holy16rus

from telethon.tl.types import Message 
from .. import loader, utils

@loader.tds
class Holilist(loader.Module):
    """A module that allows you to create a list of movies, TV series, anime, and manga."""

    strings = {
        "name": "Holilist",
        "added": "💾 <b>Добавлено:</b>\n<code>{}</code>",
        "removed": "🗑️ <b>Удалено:</b>\n<code>{}</code>",
        "no_content": "🚫 <b>Не указано название контента.</b>",
        "no_item": "🚫 <b>Элемент не найден.</b>",
        "available_categories": "📂 <b>Доступные категории:</b>\n1. Фильмы\n2. Дорамы\n3. Аниме\n4. Манги\n5. Сериалы",
        "all_items": "🌐 <b>Все ваши элементы:</b>\n",
        "no_items": "😔 <b>У вас нет элементов.</b>",
        "deleted_all": "🗑️ <b>Все элементы в категории '{}</b> были удалены.",
        "confirm_delete_all": "🔄 <b>Вы уверены, что хотите удалить все элементы в категории '{}</b>? (Да/Нет)",
    }

    async def client_ready(self):
        self._items = self.get("items", {})

    async def add_content(self, category: str, title: str, part: str):
        if part:
            full_title = f"<code> {title} часть:{part} </code>"
        else:
            full_title = f"<code>{title}</code>"

        if category not in self._items:
            self._items[category] = []

        self._items[category].insert(0, full_title)
        self.set("items", self._items)
        return full_title

    @loader.command(ru_doc="<title> [часть] - Добавить фильм")
    async def фильм(self, message: Message):
        args = utils.get_args_raw(message).strip()
        parts = args.split(' ')

        if not parts:
            await utils.answer(message, self.strings("no_content"))
            return

        if parts[-1].isdigit():
            title = ' '.join(parts[:-1]).strip()
            part = parts[-1].strip()
        else:
            title = ' '.join(parts).strip()
            part = ""

        full_title = await self.add_content("фильм", title, part)
        await utils.answer(message, self.strings("added").format(full_title))

    @loader.command(ru_doc="<title> <season> <episode> - Добавить аниме")
    async def аниме(self, message: Message):
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

    @loader.command(ru_doc="<title> <season> <episode> - Добавить дораму")
    async def дорама(self, message: Message):
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

    @loader.command(ru_doc="<title> <episode> - Добавить мангу")
    async def манга(self, message: Message):
        args = utils.get_args_raw(message).strip()
        parts = args.split(' ')

        if len(parts) < 2:
            await utils.answer(message, self.strings("no_content"))
            return

        title = ' '.join(parts[:-1]).strip()
        episode = parts[-1].strip()

        full_title = await self.add_content("манга", title, "1", episode)
        await utils.answer(message, self.strings("added").format(full_title))

    @loader.command(ru_doc="<title> <season> <episode> - Добавить сериал")
    async def сериал(self, message: Message):
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
        args = utils.get_args_raw(message).strip()

        if not args:
            await utils.answer(message, self.strings("no_content"))
            return

        parts = args.split(' ')
        category = parts[0].strip().lower()
        title = ' '.join(parts[1:-2]).strip()
        season = parts[-2].strip()
        episode = parts[-1].strip()

        if not title:
            await utils.answer(message, self.strings("no_content"))
            return

        full_title = f"<code> {title} сезон: {season} серия: {episode}</code>"

        if category in self._items and full_title in self._items[category]:
            self._items[category].remove(full_title)
            self.set("items", self._items)
            await utils.answer(message, self.strings("removed").format(full_title))
        else:
            await utils.answer(message, self.strings("no_item"))

    @loader.command(ru_doc="<category> - Удалить все элементы в категории")
    async def removeall(self, message: Message):
        args = utils.get_args_raw(message).strip()

        if not args:
            await utils.answer(message, self.strings("no_content"))
            return

        category = args.strip().lower()

        if category in self._items:
            await utils.answer(message, self.strings("confirm_delete_all").format(category))
            del self._items[category]
            self.set("items", self._items)
            await utils.answer(message, self.strings("deleted_all").format(category))
        else:
            await utils.answer(message, "🚫 <b>Категория не найдена.</b>")

    @loader.command(ru_doc="Список всех доступных категорий контента")
    async def categories(self, message: Message):
        await utils.answer(message, self.strings("available_categories"))

    @loader.command(ru_doc="Список всех элементов в категориях")
    async def listitems(self, message: Message):
        result = self.strings("all_items")

        if not self._items:
            await utils.answer(message, self.strings("no_items"))
            return

        for category, titles in self._items.items():
            result += f"\n<b>{category.capitalize()}:</b>"
            for idx, title in enumerate(titles, start=1):
                result += f"\n{idx}. {title}"

        await utils.answer(message, result)
