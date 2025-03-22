from handlers import (close_bot_menu, echo, id_media, menu, start, user_block_bot,
                      photo_gallery, create_product, categories, album, slideshow)

if __name__ == "__main__":
    from data.loader import dp, bot, on_startup, on_shutdown

    from keyboards import set_main_menu
    dp.startup.register(set_main_menu)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.include_router(router=user_block_bot.router)
    dp.include_router(router=close_bot_menu.router)
    dp.include_router(router=start.router)
    dp.include_router(router=id_media.router)
    dp.include_router(router=menu.router)
    dp.include_router(router=photo_gallery.router)
    dp.include_router(router=album.router)
    dp.include_router(router=slideshow.router)
    dp.include_router(router=create_product.router)
    dp.include_router(router=categories.router)
    dp.include_router(router=echo.router)

    dp.run_polling(bot)
