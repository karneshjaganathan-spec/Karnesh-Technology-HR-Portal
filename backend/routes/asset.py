from flask import Blueprint, request, jsonify

from middleware.auth_middleware import login_required, hr_required
from services.asset_service import AssetService

asset_bp = Blueprint(
    "asset",
    __name__,
    url_prefix="/api/assets"
)


# ==========================================
# Get All Assets
# ==========================================

@asset_bp.route("/", methods=["GET"])
@login_required
def get_assets():

    assets = AssetService.get_all()

    return jsonify({

        "success": True,
        "count": len(assets),
        "data": assets

    })


# ==========================================
# Get Asset By ID
# ==========================================

@asset_bp.route("/<int:asset_id>", methods=["GET"])
@login_required
def get_asset(asset_id):

    asset = AssetService.get(asset_id)

    if asset is None:

        return jsonify({

            "success": False,
            "message": "Asset not found."

        }), 404

    return jsonify({

        "success": True,
        "data": asset

    })


# ==========================================
# Add Asset
# ==========================================

@asset_bp.route("/", methods=["POST"])
@hr_required
def add_asset():

    data = request.get_json()

    required = [

        "asset_code",
        "asset_name",
        "category",
        "brand",
        "model",
        "serial_number",
        "purchase_date",
        "purchase_cost",
        "warranty_expiry",
        "status"

    ]

    for field in required:

        if field not in data:

            return jsonify({

                "success": False,
                "message": f"{field} is required."

            }), 400

    asset_id = AssetService.add(data)

    return jsonify({

        "success": True,
        "asset_id": asset_id,
        "message": "Asset added successfully."

    }), 201


# ==========================================
# Update Asset
# ==========================================

@asset_bp.route("/<int:asset_id>", methods=["PUT"])
@hr_required
def update_asset(asset_id):

    asset = AssetService.get(asset_id)

    if asset is None:

        return jsonify({

            "success": False,
            "message": "Asset not found."

        }), 404

    AssetService.update(

        asset_id,

        request.get_json()

    )

    return jsonify({

        "success": True,
        "message": "Asset updated successfully."

    })


# ==========================================
# Delete Asset
# ==========================================

@asset_bp.route("/<int:asset_id>", methods=["DELETE"])
@hr_required
def delete_asset(asset_id):

    asset = AssetService.get(asset_id)

    if asset is None:

        return jsonify({

            "success": False,
            "message": "Asset not found."

        }), 404

    AssetService.delete(asset_id)

    return jsonify({

        "success": True,
        "message": "Asset deleted successfully."

    })


# ==========================================
# Asset Dashboard Summary
# ==========================================

@asset_bp.route("/summary", methods=["GET"])
@login_required
def asset_summary():

    summary = AssetService.summary()

    return jsonify({

        "success": True,
        "data": summary

    })