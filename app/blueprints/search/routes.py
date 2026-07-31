from flask import Blueprint, render_template, request

from app.models.search_log import SearchLog
from app.services import search_service
from app.utils import slugify

search_bp = Blueprint("search", __name__)


@search_bp.route("/")
def search_page():
    query = request.args.get("q", "")
    SearchLog.record(query)
    hits = search_service.search(query)
    new_slug = slugify(query) if query else ""
    return render_template("search/results.html", hits=hits, query=query, new_slug=new_slug)
