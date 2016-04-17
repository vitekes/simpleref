#-*- coding: utf-8 -*-
from core.db.models import Categories, Referat
from core.db.database import Database


def get_articles_from_db(category_id, page=1, page_size=20):
    if page > 0:
        page = page - 1
    db_offset = page * page_size

    referat = Database(table=Referat)
    query = referat.session.query(Referat).filter(Referat.category_id == category_id)
    referat_list = query.limit(db_offset).offset(page_size).all()
    return referat_list


def get_category_by_url(category_url):
    db_categories = Database(table="categories")
    found_category = db_categories.session.query(Categories).filter(
            Categories.url == category_url
        ).one()
    return found_category.id, found_category.category_name, found_category.download_count



