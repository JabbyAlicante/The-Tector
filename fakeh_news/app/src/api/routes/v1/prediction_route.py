from fastapi import APIRouter

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


from controllers.v1.prediction_controller import PredictionController, PredictionRequest, PredictionResponse



router = APIRouter()
controller = PredictionController()


@router.post("/predict", response_model = PredictionResponse)
async def get_prediction(request: PredictionRequest):
    return await controller.get_prediction(request)


        


