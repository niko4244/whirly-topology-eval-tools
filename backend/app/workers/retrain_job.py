# retrain_job.py - simplified retrain orchestrator (calls training container/script)
import subprocess
import os
import json

# Example: this script exports curated examples and triggers training in a trainer container
DATASET_DIR = os.getenv('DATASET_DIR', '/data/datasets/whirly')
TRAIN_SCRIPT = os.getenv('TRAIN_SCRIPT', '/workspace/train_mask2former.py')
OUTPUT_DIR = os.getenv('MODEL_OUT', '/models')

def export_curated_examples(limit=500):
    # In production we would query Postgres, write COCO dataset to disk
    print('Exporting curated examples - stub')

def run_training():
    cmd = ["python", TRAIN_SCRIPT, "--output", OUTPUT_DIR]
    print('Running training:', ' '.join(cmd))
    subprocess.run(cmd, check=True)

if __name__ == '__main__':
    export_curated_examples()
    try:
        run_training()
    except subprocess.CalledProcessError as e:
        print('Training failed', e)