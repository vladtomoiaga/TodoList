import uuid
from flask import Blueprint, render_template, request, redirect, url_for
from html2docx import html2docx

routes = Blueprint("routes", __name__)

todolist = []

@routes.route("/", methods=["GET", "POST"])
def home():
    global todolist
    if request.method == "POST":
        task = request.form.get("task")
        task_date = request.form.get("event_date")

        # Add
        if task:
            task_id = str(uuid.uuid4())  # generate a unique ID. Help when delete a certain task.
            todolist.append({
                "id": task_id,
                "task": task,
                "date": task_date
            })

        # Edit
        for task in todolist:
            new_val = request.form.get(f"task_done_{task['id']}")
            new_text = request.form.get(f"task_text_{task['id']}")
            new_date = request.form.get(f"task_date_{task['id']}")

            if new_val is not None:
                task["done"] = (new_val == "on")

            if new_text is not None:
                task["task"] = new_text

            if new_date is not None:
                task["date"] = new_date


        # Delete
        if "delete" in request.form:
            task_id = request.form.get("delete")
            todolist[:] = [task for task in todolist if task["id"] != task_id]

        # Save
        if "save" in request.form:
            save_file()

        return redirect(url_for("routes.home"))

    return render_template("index.html", todolist=todolist)

def save_file():
    html_list = []
    for task in todolist:
        new_val = request.form.get(f"task_done_{task['id']}")
        new_text = request.form.get(f"task_text_{task['id']}")
        new_date = request.form.get(f"task_date_{task['id']}")
        html_list.append({
            "done": new_val,
            "task": new_text,
            "date": new_date
        })
    html = render_template("index.html", todolist=html_list)

    # html2docx() returns an io.BytesIO() object. The HTML must be valid.
    buf = html2docx(html, title="My Document")

    with open("todolist.docx", "wb") as fp:
        fp.write(buf.getvalue())