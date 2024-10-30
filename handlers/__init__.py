from aiogram import Router

def setup_routers() -> Router:
    from handlers import start_command, my_subscriptions, subscribe
    from callbacks import get_subscribe
    
    
    from keyboards.choise_cath import setup_dialogs, dialog
    
    router = Router()
    
    
    router.include_router(dialog)
    router.include_router(start_command.router)
    router.include_router(my_subscriptions.router)
    # router.include_router(subscribe.router)
    
    router.include_router(get_subscribe.router)
    
    return router