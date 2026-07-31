from flask import Blueprint, render_template, redirect, url_for, request, abort, flash, jsonify
from flask_login import login_required, current_user

from app.decorators import admin_required
from app.models.document import Document
from app.models.page_view import PageView
from app.models.revision import Revision
from app.services import document_service, markup_service
from app.utils import slugify

wiki_bp = Blueprint("wiki", __name__)

HOME_SLUG = "꾹문위키:대문"


@wiki_bp.route("/")
def index():
    document, revision = document_service.get_document_with_content(HOME_SLUG)
    if document is None:
        return redirect(url_for("wiki.new", slug=HOME_SLUG))

    PageView.record(document.id)
    content_html = markup_service.to_html(revision.content)
    return render_template("wiki/view.html", document=document, content_html=content_html)


@wiki_bp.route("/wiki/<slug>")
def view(slug):
    document, revision = document_service.get_document_with_content(slug)
    if document is None:
        return redirect(url_for("wiki.new", slug=slug))

    PageView.record(document.id)
    content_html = markup_service.to_html(revision.content)
    return render_template("wiki/view.html", document=document, content_html=content_html)


@wiki_bp.route("/wiki/<slug>/new", methods=["GET", "POST"])
@login_required
def new(slug):
    if Document.get_by_slug(slug):
        return redirect(url_for("wiki.view", slug=slug))

    if request.method == "POST":
        title = request.form.get("title", slug).strip() or slug
        content = request.form.get("content", "")
        document, _ = document_service.save_new_document(title, slug, content, current_user.id)
        return redirect(url_for("wiki.view", slug=document.slug))

    return render_template("wiki/edit.html", slug=slug, document=None, content="")


@wiki_bp.route("/wiki/<slug>/edit", methods=["GET", "POST"])
@login_required
def edit(slug):
    document = Document.get_by_slug(slug)
    if document is None:
        return redirect(url_for("wiki.new", slug=slug))

    if request.method == "POST":
        content = request.form.get("content", "")
        edit_comment = request.form.get("edit_comment", "")
        document_service.save_edit(document, content, current_user.id, edit_comment)
        return redirect(url_for("wiki.view", slug=document.slug))

    revision = document.current_revision
    return render_template(
        "wiki/edit.html", slug=slug, document=document, content=revision.content if revision else ""
    )


@wiki_bp.route("/wiki/_suggest")
@login_required
def suggest():
    query = request.args.get("q", "")
    return jsonify(Document.search_by_title(query, limit=8))


@wiki_bp.route("/wiki/<slug>/history")
def history(slug):
    document = Document.get_by_slug(slug)
    if document is None:
        abort(404)

    revisions = Revision.list_by_document(document.id)
    return render_template("wiki/history.html", document=document, revisions=revisions)


@wiki_bp.route("/wiki/<slug>/delete", methods=["POST"])
@login_required
@admin_required
def delete(slug):
    document = Document.get_by_slug(slug)
    if document is None:
        abort(404)

    document_service.delete_document(document)
    flash(f"'{document.title}' 문서를 삭제했습니다.")
    return redirect(url_for("wiki.index"))


@wiki_bp.route("/wiki/<slug>/history/<int:revision_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_revision(slug, revision_id):
    document = Document.get_by_slug(slug)
    if document is None:
        abort(404)

    try:
        document_service.delete_revision(document, revision_id)
        flash("리비전을 삭제했습니다.")
    except ValueError as e:
        flash(str(e))

    return redirect(url_for("wiki.history", slug=slug))
