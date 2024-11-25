from object_models.arrival_pax import ArrivalPax;
from object_models.departure_pax import DeparturePax;


class PaxFactory:
    @staticmethod
    def create_config(config_type,phase):
        if config_type == "arrival":
            return ArrivalPax(phase)
        elif config_type == "departure":
            return DeparturePax(phase)
        else:
            raise ValueError("Invalid type")
