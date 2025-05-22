from sqlalchemy.orm import Mapped, mapped_column, relationship
from train_app.db.database import Base
from typing import Optional, List
from sqlalchemy import String, Integer, DateTime, ForeignKey
from datetime import datetime
from passlib.hash import bcrypt



class UserProfile(Base):
    __tablename__ = 'user_profile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String,unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    tokens: Mapped[List['RefreshToken']] = relationship('RefreshToken', back_populates='user',
                                                  cascade='all, delete-orphan')


    def set_password(self, password: str):
        self.password = bcrypt.hash(password)

    def check_password(self, password: str):
        return bcrypt.verify(password, self.password)

    def __repr__(self):
        return f'{self.first_name}, {self.last_name}'


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))


    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='tokens')


class House(Base):
    __tablename__ = 'houses'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    GrLivArea: Mapped[int] = mapped_column(Integer)
    YearBuilt: Mapped[int] = mapped_column(Integer)
    GarageCars: Mapped[int] = mapped_column(Integer)
    TotalBsmtSF: Mapped[int] = mapped_column(Integer)
    FullBath: Mapped[int] = mapped_column(Integer)
    OverallQual: Mapped[int] = mapped_column(Integer)
    Neighborhood: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    SalePrice: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

