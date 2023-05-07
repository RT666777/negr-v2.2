from aiogram import Dispatcher
from aiogram.dispatcher import filters

from handlers.anonChat import *
from handlers.cmdCall import *
from handlers.cmdModerator import *
from handlers.cmdStart import *


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start_private, filters.ChatTypeFilter(types.ChatType.PRIVATE), commands=['start'])
    dp.register_message_handler(cmd_start_public,
                                filters.ChatTypeFilter([types.ChatType.GROUP,
                                                        types.ChatType.SUPERGROUP]),
                                commands=['start'])
    dp.register_message_handler(cmd_call_all, filters.ChatTypeFilter([types.ChatType.GROUP, types.ChatType.SUPERGROUP]),
                                commands=['callall'])
    dp.register_message_handler(cmd_kick,
                                filters.ChatTypeFilter([types.ChatType.GROUP,
                                                        types.ChatType.SUPERGROUP]),
                                filters.IsReplyFilter(True),
                                commands=['kick'])
    dp.register_message_handler(cmd_kick_without_reply,
                                filters.ChatTypeFilter([types.ChatType.GROUP,
                                                        types.ChatType.SUPERGROUP]),
                                filters.IsReplyFilter(False),
                                commands=['kick'])
    dp.register_message_handler(cmd_help, commands=['help'])
    dp.register_message_handler(cmd_search,
                                filters.ChatTypeFilter(types.ChatType.PRIVATE),
                                text=['👾 Поиск собеседника'])
    dp.register_message_handler(cmd_stop_dialog, filters.ChatTypeFilter(types.ChatType.PRIVATE), commands=['stop'])
    dp.register_message_handler(cmd_forward_message,
                                filters.ChatTypeFilter(types.ChatType.PRIVATE))
