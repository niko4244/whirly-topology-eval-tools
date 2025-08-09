import detectron2
from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg
from detectron2.data import build_detection_train_loader

def setup_cfg():
    cfg = get_cfg()
    cfg.merge_from_file("configs/Mask2Former.yaml")  # Path to Mask2Former config
    cfg.DATASETS.TRAIN = ("whirly_train",)
    cfg.DATASETS.TEST = ()
    cfg.DATALOADER.NUM_WORKERS = 4
    cfg.SOLVER.IMS_PER_BATCH = 4
    cfg.SOLVER.MAX_ITER = 30000
    cfg.SOLVER.BASE_LR = 0.00025
    cfg.MODEL.WEIGHTS = "pretrained_mask2former.pth"
    cfg.INPUT.MIN_SIZE_TRAIN = (1024, 1333)
    cfg.INPUT.MAX_SIZE_TRAIN = 1333
    cfg.INPUT.MIN_SIZE_TEST = 1024
    cfg.INPUT.MAX_SIZE_TEST = 1333
    cfg.MODEL.META_ARCHITECTURE = "Mask2Former"
    cfg.OUTPUT_DIR = "./output"
    return cfg

if __name__ == "__main__":
    cfg = setup_cfg()
    trainer = DefaultTrainer(cfg)
    trainer.resume_or_load(resume=False)
    trainer.train()