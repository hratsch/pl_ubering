from alembic import command, config as alembic_config
cfg = alembic_config.Config("alembic.ini")
print("Current revision:", command.current(cfg))