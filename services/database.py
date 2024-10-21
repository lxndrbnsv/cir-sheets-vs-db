import json
from sqlalchemy import create_engine, text
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from services.utils import Phone, BasicLogger as logger
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
        self.contacts = base.classes.contacts
        self.leads = base.classes.leads
        self.pipelines = base.classes.pipelines


class Company(Database):
    def find_companies_by_phone(self, phone_number: str):
        """Находим ID всех компаний с одинаковыми номерами телефонов"""
        session = Session(self.engine)
        companies = (
            session.query(self.companies)
            .filter(self.companies.Telefon.contains([phone_number]))
            .all()
        )
        session.close()
        data = list()
        for company in companies:
            company_id, name, website, company_type = (
                company.id,
                company.name,
                company.Web,
                company.Tip_organizatsii_2gis,
            )
            print(company_id)
            print(name)
            print(website)
            print(company_type)
            print("--- --- ---")

    def duplicates(self, company_id: int):
        """Находим дубликаты записей по ID компании"""
        pass

    def update_phone_numbers(self):
        """Приводит номера телефонов в базе данных к единому формату."""
        session = Session(self.engine)
        companies = session.query(self.companies).all()
        for num, company in enumerate(companies):
            logger(
                "Форматирование номеров телефонов в таблице companies: "
                f"{num + 1} из {len(companies)} записей изменено."
            )
            if company.Telefon:
                phones = json.loads(company.Telefon)
                transformed_phones = [
                    Phone(phone).transform_phone() for phone in phones
                ]
                company.Telefon = json.dumps(transformed_phones)

        logger("Сохранение изменений в таблице companies")
        session.commit()
        session.close()
        logger("Изменения в таблице companies сохранены")


class Contact(Database):
    def update_phone_numbers(self):
        session = Session(self.engine)

        # Обновляем номера телефонов в таблице contacts
        contacts = session.query(self.contacts).all()
        for num, contact in enumerate(contacts):
            logger(
                "Форматирование номеров телефонов в таблице contacts: "
                f"{num + 1} из {len(contacts)} записей изменено."
            )
            if contact.Telefon:
                phones = json.loads(contact.Telefon)
                transformed_phones = [
                    Phone(phone).transform_phone() for phone in phones
                ]
                contact.Telefon = json.dumps(
                    transformed_phones, ensure_ascii=False
                )
        logger("Сохранение изменений в таблице contacts")
        session.commit()
        session.close()
        logger("Изменения в таблице contacts сохранены")
