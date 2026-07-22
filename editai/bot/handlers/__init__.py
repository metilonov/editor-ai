from aiogram import Router
from editai.bot.handlers import admin,errors,jobs,media,settings,start


def build_router()->Router:
    root=Router(name="root")
    for router in (start.router,settings.router,jobs.router,admin.router,media.router,errors.router):root.include_router(router)
    return root
