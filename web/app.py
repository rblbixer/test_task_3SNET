import os
import subprocess
import time
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, send_from_directory

from web.db import init_db, save_run, get_run, get_all_runs
from core.constants import LIST_TESTS


app = Flask(__name__)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ALLURE_RESULTS_DIR = os.path.join(os.path.dirname(__file__), "allure-results")
ALLURE_REPORTS_DIR = os.path.join(os.path.dirname(__file__), "allure-reports")


def run_pytest(test_name: str, run_id: int) -> "tuple[str, str, float]":
    results_dir = os.path.join(ALLURE_RESULTS_DIR, str(run_id))
    reports_dir = os.path.join(ALLURE_REPORTS_DIR, str(run_id))

    if test_name == "all":
        cmd = ["pytest", "tests/test_eventswidget.py", "-v", f"--alluredir={results_dir}"]
    else:
        cmd = ["pytest", f"tests/test_eventswidget.py::{test_name}", "-v", f"--alluredir={results_dir}"]

    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_ROOT)
    duration = round(time.time() - start, 2)

    subprocess.run(
        ["allure", "generate", results_dir, "-o", reports_dir, "-c"],
        capture_output=True,
        cwd=PROJECT_ROOT,
    )

    output = result.stdout + (result.stderr if result.stderr else "")
    status = "passed" if result.returncode == 0 else "failed"
    return output, status, duration


@app.route("/")
def index():
    return render_template("index.html", tests=LIST_TESTS)


@app.route("/run", methods=["POST"])
def run():
    test_name = request.form.get("test_name", "all")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    run_id = save_run(timestamp, test_name, "running", 0.0, "")
    output, status, duration = run_pytest(test_name, run_id)
    save_run(timestamp, test_name, status, duration, output, run_id=run_id)
    return redirect(url_for("result", run_id=run_id))


@app.route("/result/<int:run_id>")
def result(run_id: int):
    run = get_run(run_id)
    if run is None:
        return "Запуск не найден", 404
    has_allure = os.path.isfile(os.path.join(ALLURE_REPORTS_DIR, str(run_id), "index.html"))
    return render_template("result.html", run=run, has_allure=has_allure)


@app.route("/allure/<int:run_id>/")
@app.route("/allure/<int:run_id>/<path:filepath>")
def allure_report(run_id: int, filepath: str = "index.html"):
    report_dir = os.path.join(ALLURE_REPORTS_DIR, str(run_id))
    return send_from_directory(report_dir, filepath)


@app.route("/history")
def history():
    runs = get_all_runs()
    return render_template("history.html", runs=runs)
