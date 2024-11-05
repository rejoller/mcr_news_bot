from aiogram import Router


def setup_routers() -> Router:
    from handlers import start_command, subscribe_dialog, my_subscriptions
    from handlers.subscribe_dialog import dialog
    from callbacks import last_news
    from aiogram_dialog import setup_dialogs
    
   
    router = Router()
    router.include_router(last_news.router)

    router.include_router(my_subscriptions.router)
    router.include_router(subscribe_dialog.router)
    
    router.include_router(dialog)
    
    router.include_router(start_command.router)
    setup_dialogs(router)
    
    
    
    
    # router.include_router(subscribe_dialog.router)
    
    

    
    return router