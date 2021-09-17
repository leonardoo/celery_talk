from datetime import datetime, timedelta

from celery.result import AsyncResult
from flask import Blueprint, Flask, jsonify, url_for

from apps.tasks import long_task, celery

home = Blueprint("home", __name__)


@home.route("/")
def index():
    """Add a new task and start running it after 10 seconds."""
    eta = datetime.utcnow() + timedelta(seconds=10)
    task = long_task.apply_async(eta=eta)
    return (
        jsonify(
            {"_links": {"task": url_for("status.get", task_id=task.id, _external=True)}}
        ),
        201,
    )


status = Blueprint("status", __name__, url_prefix="/status")


@status.route("/<task_id>/", methods=["GET"])
def get(task_id):
    task = AsyncResult(task_id, app=celery)
    if task.state == "PENDING":
        # job did not start yet
        response = {"state": task.state, "status": "Pending..."}
    elif task.state != "FAILURE":
        response = {
            "state": task.state,
            "current": task.info.get("current", 0),
            "total": task.info.get("total", 1),
            "status": task.info.get("status", ""),
        }
        if "result" in task.info:
            response["result"] = task.info["result"]
    else:
        # something went wrong in the background job
        response = {
            "state": task.state,
            "current": 1,
            "total": 1,
            "status": str(task.info),  # this is the exception raised
        }
    return jsonify(response)


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(home)
    app.register_blueprint(status)
