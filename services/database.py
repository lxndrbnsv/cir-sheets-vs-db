from sqlalchemy import create_engine, text
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from config import Config as cfg


class Database:
    def __init__(self) -> None:
        base = automap_base()
        self.engine = create_engine(
            f"mysql+pymysql://{cfg.DATABASE_USER}"
            f":{cfg.DATABASE_PASSWORD}@{cfg.DATABASE_HOST}/{cfg.DATABASE_NAME}"
            "?charset=utf8mb4"
        )
        base.prepare(autoload_with=self.engine)
        self.companies = base.classes.companies
        self.leads = base.classes.leads
        self.pipelines = base.classes.pipelines

    def company_exists(self, phone_number):
        session = Session(self.engine)
        company = (
            session.query(self.companies)
            .filter(self.companies.Telefon.contains([phone_number]))
            .first()
        )
        session.close()
        if company:
            return True
        else:
            return False
