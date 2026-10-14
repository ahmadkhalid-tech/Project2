from flask import Flask, jsonify, render_template, request


def create_app():
    app = Flask(__name__)
    tasks = []
    next_id = {"value": 1}

    @app.get("/")
    def home():
        return render_template("index.html")

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.get("/api/tasks")
    def list_tasks():
        return jsonify(tasks)

    @app.post("/api/tasks")
    def add_task():
        data = request.get_json(silent=True) or {}
        title = str(data.get("title") or "").strip()
        if not title:
            return jsonify({"error": "title is required"}), 400
        if len(title) > 80:
            return jsonify({"error": "title is too long"}), 400

        task = {"id": next_id["value"], "title": title, "done": False}
        next_id["value"] += 1
        tasks.append(task)
        return jsonify(task), 201

    @app.get("/api/tasks/<int:task_id>")
    def get_task(task_id):
        task = _find(tasks, task_id)
        if task is None:
            return jsonify({"error": "not found"}), 404
        return jsonify(task)

    @app.post("/api/tasks/<int:task_id>/complete")
    def complete_task(task_id):
        task = _find(tasks, task_id)
        if task is None:
            return jsonify({"error": "not found"}), 404
        task["done"] = True
        return jsonify(task)

    @app.delete("/api/tasks/<int:task_id>")
    def delete_task(task_id):
        task = _find(tasks, task_id)
        if task is None:
            return jsonify({"error": "not found"}), 404
        tasks.remove(task)
        return jsonify({"deleted": task_id})

    @app.get("/api/stats")
    def stats():
        total = len(tasks)
        done = sum(1 for task in tasks if task["done"])
        return jsonify({"total": total, "done": done, "pending": total - done})

    return app


def _find(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
