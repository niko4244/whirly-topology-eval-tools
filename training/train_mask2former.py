import detectron2
from detectron2.config import get_cfg
from detectron2.engine import DefaultTrainer
from detectron2.data import build_detection_train_loader, transforms as T

def setup(cfg_file, output_dir):
    cfg = get_cfg()
    cfg.merge_from_file(cfg_file)
    cfg.OUTPUT_DIR = output_dir
    os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
    return cfg

class Trainer(DefaultTrainer):
    @classmethod
    def build_train_loader(cls, cfg):
        mapper = detectron2.data.DatasetMapper(cfg, is_train=True, augmentations=[
            T.ResizeShortestEdge(short_edge_length=(800,1024), max_size=1333, sample_style='choice'),
            T.RandomRotation(angle=[-6,6]),
            T.RandomBrightness(0.9,1.1),
        ])
        return build_detection_train_loader(cfg, mapper=mapper)

if __name__ == "__main__":
    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument("--cfg", required=True)
    parser.add_argument("--output", default="./out")
    args = parser.parse_args()
    cfg = setup(args.cfg, args.output)
    trainer = Trainer(cfg)
    trainer.resume_or_load(resume=False)
    trainer.train()