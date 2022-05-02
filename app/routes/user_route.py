from flask import Blueprint
from app.controllers import user_controller

bp = Blueprint("api", __name__, url_prefix="/api")

bp.post("/signup")(user_controller.register)
bp.post("/signin")(user_controller.login)
bp.get("")(user_controller.retrieve_user)
bp.put("")(user_controller.update_user)
bp.delete("")(user_controller.delete_user)