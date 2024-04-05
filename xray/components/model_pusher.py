import sys
from xray.constants import *
from xray.logger import logging
from xray.exception import CustomException
from xray.cloud_storage.s3_ops import UploadFile

class ModelPusher:

    def __init__(self):
        
        self.s3 = UploadFile()

    def initiate_model_pusher(self):

        """
        Method Name :   initiate_model_pusher

        Description :   This method initiates model pusher. 
        
        Output      :    Model pusher artifact 
        """
        logging.info("Entered initiate_model_pusher method of Modelpusher class")

        try:
            
            self.s3.upload_file(
                "model/model.pt",
                "model.pt",
                BUCKET_NAME,
                remove=False,
            )
            logging.info("Uploaded best model to s3 bucket")
            logging.info("Exited initiate_model_pusher method of ModelTrainer class")


        except Exception as e:
            raise CustomException(e, sys)
