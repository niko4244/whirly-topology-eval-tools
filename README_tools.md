# Whirly Training Tools

This directory contains:
- `topology_eval_hook.py`: A Detectron2 hook for running custom topology metrics evaluation post-inference during training.
- `preprocess_dataset.py`: Script to automate preprocessing vector SVG annotation JSONs into raster masks and Detectron2-style JSONs.

## Usage

### Topology Evaluation Hook

1. Import and register in your training script:

```python
from topology_eval_hook import TopologyEvalHook

def topology_metric_func(inputs, outputs):
    # Implement your topology metrics logic here.
    return {"critical_path_length": 123.4, "fault_coverage": 0.95}

eval_loader = trainer.build_test_loader(cfg, "circuit_vector_train")
eval_hook = TopologyEvalHook(
    eval_period=1000,
    model=trainer.model,
    data_loader=eval_loader,
    output_dir=cfg.OUTPUT_DIR,
    topology_metric_func=topology_metric_func,
)
trainer.register_hooks([eval_hook])
```

### Dataset Preprocessing

1. Update the file/folder paths and run:

```python
python preprocess_dataset.py
```

This will generate binary mask PNGs and JSON annotation files for Detectron2 training.

---
MIT License