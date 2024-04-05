
from xray.pipeline.train_pipeline import TrainPipeline

def main():
    # training the pipeline
    train_pipeline = TrainPipeline()
    train_pipeline.run_pipeline()

if __name__=="__main__":
    main()