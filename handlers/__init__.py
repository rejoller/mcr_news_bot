from aiogram import Router


def setup_routers() -> Router:
    from handlers import start_command, subscribe_dialog, my_subscriptions, airflow
    from handlers.subscribe_dialog import dialog
    from callbacks import last_news, dag_control, switch_dags, dag_newrun, dag_setfail
    from aiogram_dialog import setup_dialogs
    
   
    router = Router()
    
    router.include_router(dag_setfail.router)
    router.include_router(dag_newrun.router)
    router.include_router(switch_dags.router)
    router.include_router(airflow.router)
    router.include_router(dag_control.router)
    router.include_router(start_command.router)
    router.include_router(last_news.router)

    router.include_router(my_subscriptions.router)
    router.include_router(subscribe_dialog.router)
    
    router.include_router(dialog)
    
    
    setup_dialogs(router)
    
    
    
    
    # router.include_router(subscribe_dialog.router)
    
    

    
    return router