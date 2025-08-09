def score_topology(G_pred, G_gt, tol_px=6):
    import numpy as np
    from scipy.spatial import cKDTree
    gt_nodes = [(n, G_gt.nodes[n]['x'], G_gt.nodes[n]['y']) for n in G_gt.nodes]
    pred_nodes = [(n, G_pred.nodes[n]['x'], G_pred.nodes[n]['y']) for n in G_pred.nodes]
    if not gt_nodes or not pred_nodes:
        return {'node_prec':0,'node_rec':0,'edge_prec':0,'edge_rec':0}
    gt_coords = np.array([[x,y] for _,x,y in gt_nodes])
    pred_coords = np.array([[x,y] for _,x,y in pred_nodes])
    gt_kd = cKDTree(gt_coords)
    pred_kd = cKDTree(pred_coords)
    matched_pred = set()
    matched_gt = set()
    for i,p in enumerate(pred_coords):
        d,idx = gt_kd.query(p)
        if d<=tol_px:
            matched_pred.add(i); matched_gt.add(idx)
    node_prec = len(matched_pred)/len(pred_coords)
    node_rec = len(matched_gt)/len(gt_coords)
    # Edge scoring can be implemented with set comparison (see main message)
    return {'node_prec':node_prec,'node_rec':node_rec}