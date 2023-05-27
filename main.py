from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()
engine = create_engine("mysql+pymysql://{user}:{password}@{host}/{database}")

# Clase del modelo:
class User(Base):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    created_ad = Column(DateTime, default=datetime.now())


    def __init__(self, username, email):
        self.username = username
        self.email = email


    def __str__(self) -> str:
        return self.username


Session = sessionmaker(engine)
session = Session()


def list_user():
    return session.query(User).all()


def add_user(username, email):
    users = list_user()
    users = [user.username for user in users]
    if username in users:
        print("El usuario ya fue registrado.") 
    else:
        user = User(username, email)
        session.add(user)
        session.commit()


def update_user(id, username, email):
    users = list_user()
    users_id = [user.id for user in users]
    if id not in users_id:
        print("El id ingresado no esta registrado")
    else:
        users_new = session.query(User).filter(
            User.id != id
        )
        users_name = [user.username for user in users_new]
        if username in users_name:
            print("El nombre de usuario ya esta registrado")
        else:
            users_email = [user.email for user in users_new]
            if email in users_email:
                print("El email ingresado ya ha sido registrado.")
            else:
                session.query(User).filter(User.id == id).update(
                    {
                        User.username: username,
                        User.email: email,
                        User.created_ad: datetime.now() 
                    }
                )
                session.commit()
        

def drop_user(id):
    users = list_user()
    users_id = [user.id for user in users]
    if id in users_id:
        session.query(User).filter(User.id == id).delete()
        session.commit()
    else:
        print("El id ingresado no se encuentra en la tabla.")



if __name__ == "__main__":
    Base.metadata.create_all(engine)

    drop_user(7)

    session.close()
