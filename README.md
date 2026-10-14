# Task Board

Chhoti Python (Flask) website. Is me 10 pytest cases hain jo Jenkins pipeline chalati hai.

## Local run

```bash
python -m pip install -r requirements.txt
python app.py
```

Browser: http://127.0.0.1:5000

## Tests

```bash
python -m pytest
```

`pytest.ini` result `test-results.xml` me likhta hai. Jenkins ka JUnit plugin yahi file padhta hai.

10 cases:

1. Home page load
2. Health check
3. Empty task list
4. Task add
5. Empty title reject
6. Task by id
7. Mark complete
8. Delete task
9. Stats (done / pending)
10. Missing task returns 404

## Jenkins

1. Jenkins me **Pipeline** job banao.
2. Is repo ko SCM se connect karo (Git). `Jenkinsfile` repo root me hai.
3. Job me **Pipeline script from SCM** select karo.
4. Build chalao. **Test** stage `pytest` chalata hai, phir **Test Result** me 10 cases dikhte hain.

Agent ke paas `python` (Windows) ya `python3` (Linux) PATH me hona chahiye.
