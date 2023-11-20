from games.repository.review_repository.review_repository import ReviewRepository
from games.repository.review_repository.adapters import csv_review_repository
def create(adapter_type, testing: bool=False) -> ReviewRepository:

    if adapter_type == "csv":
        c = csv_review_repository.CSVReviewRepository()

    elif adapter_type == "database":
        c = database_review_repository.DatabaseReviewRepository()

    c.populate(testing)
    return c


review_repo_instance: ReviewRepository = None
