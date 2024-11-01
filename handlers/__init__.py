from aiogram import Router

def setup_routers() -> Router:
    from handlers import start_command, subscribe_dialog
    from callbacks import get_subscribe
    from handlers.subscribe_dialog import dialog
    
    

    
    router = Router()
    router.include_router(start_command.router)
    router.include_router(subscribe_dialog.router)
    router.include_router(dialog)
    
    
    router.include_router(get_subscribe.router)
    
    return router