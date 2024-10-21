from services.database import Contact, Company


def update_contacts() -> None:
    Contact().update_phone_numbers()


def update_companies() -> None:
    Company().update_phone_numbers()


def main():
    update_contacts()
    update_companies()


if __name__ == "__main__":
    main()
