from aiogram import Router

def setup_routers() -> Router:
    from handlers import start_command, subscribe, main_cathegories
    from callbacks import get_subscribe
    
    
    from keyboards.choise_subcath import sub_cathegories
    from keyboards.choise_subcath import setup_dialogs, sub_cathegories
    
    router = Router()
    router.include_router(sub_cathegories)
    router.include_router(subscribe.router)
    router.include_router(main_cathegories.router)
    
    router.include_router(start_command.router)
    
    router.include_router(get_subscribe.router)
    
    return router