from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import ForeignKey, String, BIGINT, TIMESTAMP, DateTime, BOOLEAN, INTEGER

class Base(DeclarativeBase):
    pass



class Users(Base):
    __tablename__ = 'users'
    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(200), nullable=True)
    username: Mapped[str] = mapped_column(String(255), nullable=True)
    joined_at: Mapped[DateTime] = mapped_column(TIMESTAMP)
    is_admin: Mapped[bool] = mapped_column(BOOLEAN)

    
    
class Main_categories(Base):
    __tablename__ = 'main_categories'
    main_category_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    main_category_short_name: Mapped[str] = mapped_column(String(255))
    main_category_name: Mapped[str] = mapped_column(String(255))
    main_category_description: Mapped[str] = mapped_column(String(255), nullable=True)
    
    
    
class Subcategories(Base):
    __tablename__ = 'subcategories'
    main_category_id: Mapped[int] = mapped_column(ForeignKey('main_categories.main_category_id'), autoincrement=True)
    subcategory_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    subcategory_short_name: Mapped[str] = mapped_column(String(255))
    subcategory_name: Mapped[str] = mapped_column(String(255))
    subcategory_description: Mapped[str] = mapped_column(String(255), nullable=True)
    
    
    
class Subscriptions(Base):
    __tablename__ = 'subscriptions'
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('subcategories.subcategory_id'), primary_key=True)
    
    
class Messages(Base):
    __tablename__ = 'messages'
    message_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('users.user_id'))
    email_id: Mapped[str] = mapped_column(String(225))
    date_send: Mapped[DateTime] = mapped_column(TIMESTAMP)
    message_text: Mapped[str] = mapped_column(String, nullable=True)
    subcategory_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('subcategories.subcategory_id'))
    
    
class Manager(Base):
    __tablename__ = 'category_manager'
    manager_id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('users.user_id'))
    subcategory_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('subcategories.subcategory_id'))
    
    
    
    
    





    
    
    
    
    
    
    
    
    
    
    
    
