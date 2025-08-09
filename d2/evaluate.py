# evaluate.py - runs inference, extracts graphs, scores topology
from d2.topology_eval import extract_graph_from_mask, score_topology
import numpy as np
import json

def load_mask(file_path):
    from PIL import Image
    return np.array(Image.open(file_path).convert("L")) > 128

def load_terminals(json_path):
    with open(json_path) as f:
        data = json.load(f)
    return data['terminals']

def main(gt_mask_path, gt_term_json, pred_mask_path, pred_term_json):
    gt_mask = load_mask(gt_mask_path)
    pred_mask = load_mask(pred_mask_path)
    gt_terminals = load_terminals(gt_term_json)
    pred_terminals = load_terminals(pred_term_json)
    G_gt = extract_graph_from_mask(gt_mask, gt_terminals)
    G_pred = extract_graph_from_mask(pred_mask, pred_terminals)
    metrics = score_topology(G_pred, G_gt)
    print("Topology metrics:", metrics)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--gt_mask", required=True)
    parser.add_argument("--gt_terms", required=True)
    parser.add_argument("--pred_mask", required=True)
    parser.add_argument("--pred_terms", required=True)
    args = parser.parse_args()
    main(args.gt_mask, args.gt_terms, args.pred_mask, args.pred_terms)