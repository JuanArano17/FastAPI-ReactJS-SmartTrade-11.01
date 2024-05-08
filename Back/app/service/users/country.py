from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.crud_repository import CRUDRepository
from app.models.users.country import Country
from app.schemas.users.country import CountryCreate, CountryUpdate

class CountryService:
    def __init__(self, session: Session):
        self.session = session
        self.country_repo = CRUDRepository(session=session, model=Country)

    def add(self, country: CountryCreate) -> Country:
        country_obj = Country(**country.model_dump())
        country_obj = self.country_repo.add(country_obj)
        return country_obj

    def get_all(self) -> list[str]:
        countries=self.country_repo.get_all()
        country_names=[]
        for country in countries:
            country_names.append(country.name)
        return(country_names)

    def get_by_id(self, id) -> Country:
        if country := self.country_repo.get_by_id(id):
            return country

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Country with id {id} not found.",
        )

    def update(self, country_id, new_data: CountryUpdate) -> Country:
        country = self.get_by_id(country_id)
        return self.country_repo.update(country, new_data)

    def delete_by_id(self, country_id):
        self.get_by_id(country_id)
        self.country_repo.delete_by_id(country_id)

    def delete_all(self):
        self.country_repo.delete_all()
