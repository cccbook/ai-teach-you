from sqlalchemy import create_engine, inspect
from alembic.config import Config
from alembic import command

engine = create_engine("sqlite:///./app.db")

def create_migration():
    alembic_cfg = Config("alembic.ini")
    command.init(alembic_cfg, "migrations")
    
def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

def rollback_migration():
    alembic_cfg = Config("alembic.ini")
    command.downgrade(alembic_cfg, "-1")

def show_tables():
    inspector = inspect(engine)
    return inspector.get_table_names()

if __name__ == "__main__":
    print("Tables:", show_tables())
