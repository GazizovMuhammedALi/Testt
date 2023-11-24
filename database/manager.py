from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from .models import Service, Category, LastWork

class DBManager:

    def __init__(self, enigne: Engine):
        self.engine = enigne

    def get_all_categories(self):
        with Session(self.engine) as session:
            categories = select(Category)
            categories = session.scalars(categories).all()
        
        return categories
    
    def get_services_by_category(self, category_id):
        with Session(self.engine) as session:
            services = select(Service).filter(Service.category_id==category_id)
            services = session.scalars(services).all()
        
        return services
    
    def get_service(self, service_id):
        with Session(self.engine) as session:
            service = select(Service).filter(Service.id==service_id)
            service = session.scalar(service)
        
        return service
    

    def get_last_works(self):
        with Session(self.engine) as session:
            works = select(LastWork).order_by(LastWork.date)
            works = session.scalars(works).all()

        return works
    

    def insert_work(self, path):
        with open(path, "rb") as file:
            data = file.read()
            with Session(self.engine) as session:
                session.add(
                    LastWork(
                        image = data
                    )
                )
                session.commit()

            
