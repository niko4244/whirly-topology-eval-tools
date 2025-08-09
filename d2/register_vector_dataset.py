from detectron2.data import DatasetCatalog, MetadataCatalog
from d2.dataset_vector import load_circuit_dataset

label_map = {"wire": 0, "resistor": 1, "capacitor": 2}  # Example label to ID

def get_circuit_dicts():
    return load_circuit_dataset("/path/to/json_annotations", label_map)

DatasetCatalog.register("circuit_vector_train", get_circuit_dicts)
MetadataCatalog.get("circuit_vector_train").set(thing_classes=list(label_map.keys()))