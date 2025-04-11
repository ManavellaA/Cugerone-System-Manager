from flask import Flask

# ---------------------- GET --------------------------
from app.routes.get.main.index import index_bp
from app.routes.get.upload.upload import upload_bp
from app.routes.get.pantografos.pantografos import pantografos_bp
from app.routes.get.materials.materials import materials_bp
from app.routes.get.chapa.chapa import chapa_bp
from app.routes.get.chapa_danes.chapa_danes import chapa_danes_bp
from app.routes.get.oc.oc import oc_create_bp
from app.routes.get.graph_client.graph_client import graph_client_bp

# --- BUDGETs ---
from app.routes.get.budget.budget.budget import budget_bp
from app.routes.get.list.budget_list import budget_list_bp
from app.routes.get.follow.budget_follow import budget_follow_bp
from app.routes.get.view.budget_view import budget_view_bp
from app.routes.get.edit.budget_edit import budget_edit_bp
from app.routes.get.graph.budget_graph import budget_graph_bp
# ---------------

from app.routes.post.cortes.cortes import corte_bp

# ----------------------------------------------------

# ---------------------- POST --------------------------
from app.routes.post.post_upload.upload import post_upload_bp
from app.routes.post.download.download import download_bp
from app.routes.post.save_state.save_state import save_state_bp
from app.routes.post.upstream.budget_upstream import budget_upstream_bp
from app.routes.post.save_entry.save_entry import save_entry_bp
from app.routes.post.update_record.update_record import update_record_bp

# ----------------------------------------------------

# ---------------------- ADM --------------------------

from app.routes.get.payments.payments import payments_bp

app = Flask(__name__)

def create_app():
    app.register_blueprint(index_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(download_bp)
    app.register_blueprint(pantografos_bp)
    app.register_blueprint(materials_bp)
    app.register_blueprint(chapa_bp)     
    app.register_blueprint(chapa_danes_bp)     
    app.register_blueprint(budget_bp)
    app.register_blueprint(budget_list_bp)
    app.register_blueprint(budget_follow_bp)
    app.register_blueprint(budget_view_bp)
    app.register_blueprint(budget_upstream_bp)
    app.register_blueprint(budget_graph_bp)
    app.register_blueprint(budget_edit_bp)
    app.register_blueprint(post_upload_bp)
    app.register_blueprint(save_state_bp)
    app.register_blueprint(save_entry_bp)
    app.register_blueprint(oc_create_bp)
    app.register_blueprint(update_record_bp)
    app.register_blueprint(corte_bp)
    app.register_blueprint(graph_client_bp)
    app.register_blueprint(payments_bp)
    
    return app
