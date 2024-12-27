from flask import Flask, render_template
from services.vote_service import VoteService

def create_app():
    app = Flask(__name__)
    vote_service = VoteService()

    @app.route('/')
    def index():
        votes = vote_service.get_votes()
        total_votes = votes["sim"] + votes["nao"]
        percentages = {
            "sim": round((votes["sim"] / total_votes) * 100, 2) if total_votes > 0 else 0,
            "nao": round((votes["nao"] / total_votes) * 100, 2) if total_votes > 0 else 0
        }
        return render_template("vote_template.html", votes=votes, percentages=percentages)

    return app
