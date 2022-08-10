from dataclasses import asdict

from flask import Flask
from flask import jsonify
from flask import request
from flask import Response

from input_validator import job_info_validator
from scrapers.jobs_scraper import get_job_info
from scrapers.jobs_scraper import InvalidJobURL


app = Flask(__name__)


@app.route("/job-info", methods=["GET"])
def job_info() -> Response:
    validation_result = job_info_validator.validate_input_args(request.args)
    if validation_result:
        return validation_result, 400

    url_or_id: str = request.args.get("job_url_or_id")

    job = int(url_or_id) if url_or_id.isnumeric() else url_or_id
    try:
        job_info = get_job_info(job)
    except InvalidJobURL as error:
        return (
            job_info_validator.invalid_job_url_result(error.url, isinstance(job, int)),
            400,
        )

    return jsonify(
        {
            "success": True,
            "data": [asdict(job_info)],
        }
    )


if __name__ == "__main__":
    app.run()
