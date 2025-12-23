
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))



from fastapi.concurrency import run_in_threadpool
from model.prediction_model import PredictionModel
from schemas.prediction_schema import PredictionRequest, PredictionResponse


class PredictionController:
    
    def __init__(self):
        self.predictionModel = PredictionModel()
        print("Controller Initialized")
        
        
    async def get_prediction(self, request: PredictionRequest):
        print("LINK: ",request.link)
        
        if request.link:  
       
            prediction, label, text, final = await run_in_threadpool(
                self.predictionModel.prediction, request.text, request.link
            )
            
        else:
            
            
            prediction, label, text, final = await run_in_threadpool(self.predictionModel.prediction, request.text)
        
      
        fake_score = final["fake"]["score"]
        fake_percentage = final["fake"]["percentage"]
        real_score = final["real"]["score"]
        real_percentage = final["real"]["percentage"]
        
        
        return PredictionResponse(
            
    final_prediction=prediction,
    prediction_class=label,
    user_input=text,
    fake_score=fake_score,
    fake_percentage=fake_percentage,
    real_score=real_score,
    real_percentage=real_percentage
)

        
        
         
        
        
        
# pc = PredictionController()