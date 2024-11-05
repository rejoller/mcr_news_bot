from aiogram import Router
from aiogram_dialog import setup_dialogs

def setup_routers() -> Router:
    from handlers import start_command
    from handlers.subscribe_dialog import dialog
    
   
    router = Router()
    
    router.include_router(start_command.router)
    router.include_router(dialog)
    setup_dialogs(router)
    
    
    # router.include_router(subscribe_dialog.router)
    
    

    
    return router