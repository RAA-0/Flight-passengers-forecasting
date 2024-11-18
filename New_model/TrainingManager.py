from New_model.Training.Preprocessingg import EventFeatureExtractor
from New_model.Training.Training import DataTrainer
from object_models.pax_factory import PaxFactory
import pandas as pd

def main():
    data = pd.read_csv('New_model\\data\\Training\\TrainingDataset.csv')
    process = EventFeatureExtractor()
    transformed_data = process.transform(data)
    for pax_type in ['arrival','departure']:
        config = PaxFactory.create_config(pax_type,'training')
        data = transformed_data.copy()
        trainer = DataTrainer(data,config)
        model=trainer.prophet_model()
        trainer.train(model)

if __name__=='__main__':
    main()