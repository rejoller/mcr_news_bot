from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import ForeignKey, String, BIGINT, TIMESTAMP, DateTime, BOOLEAN

class Base(DeclarativeBase):
    pass



class Users(Base):
    __tablename__ = 'users'
    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    username: Mapped[str] = mapped_column(String(255))
    joined_at: Mapped[DateTime] = mapped_column(TIMESTAMP)
    is_admin: Mapped[bool] = mapped_column(BOOLEAN)

    
    
class News_cathegories(Base):
    __tablename__ = 'news_cathegories'
    cathegory_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    cathegory_short_name: Mapped[str] = mapped_column(String(255))
    cathegory_name: Mapped[str] = mapped_column(String(255))
    cathegory_description: Mapped[str] = mapped_column(String(255), nullable=True)
    
    
    
class Subscriptions(Base):
    __tablename__ = 'subscriptions'
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), primary_key=True)
    cathegory_id: Mapped[int] = mapped_column(ForeignKey('news_cathegories.cathegory_id'), primary_key=True)
    
    
class Messages(Base):
    __tablename__ = 'messages'
    message_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('users.user_id'))
    email_id: Mapped[str] = mapped_column(String(225))
    date_send: Mapped[DateTime] = mapped_column(TIMESTAMP)
    message_text: Mapped[str] = mapped_column(String)
    





    
    
    
    
    
    
    
    
    
    
    
    
