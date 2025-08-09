import networkx as nx
import numpy as np
from skimage.morphology import skeletonize

def extract_graph_from_mask(wire_mask, component_terminals):
    skel = skeletonize(wire_mask > 0).astype(np.uint8)
    H, W = skel.shape
    G = nx.Graph()
    coords = np.argwhere(skel)
    from collections import defaultdict
    deg = defaultdict(int)
    neigh = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    for (r,c) in coords:
        cnt=0
        for dr,dc in neigh:
            nr, nc = r+dr, c+dc
            if 0<=nr<H and 0<=nc<W and skel[nr,nc]:
                cnt+=1
        deg[(r,c)]=cnt
    node_pixels = [p for p,d in deg.items() if d!=2]
    for t in component_terminals:
        node_id = f"term_{t['id']}_{t['term']}"
        G.add_node(node_id, type='terminal', x=t['x'], y=t['y'])
    for p in node_pixels:
        node_id = f"junction_{p[0]}_{p[1]}"
        G.add_node(node_id, type='junction', x=p[1], y=p[0])
    visited = set()
    def walk_from(p):
        path=[p]
        cur = p
        prev = None
        while True:
            neighbors=[]
            r,c=cur
            for dr,dc in neigh:
                nr,nc = r+dr,c+dc
                if 0<=nr<H and 0<=nc<W and skel[nr,nc] and (nr,nc)!=prev:
                    neighbors.append((nr,nc))
            if len(neighbors)==0:
                return None
            if len(neighbors)>1:
                return cur, path
            prev=cur
            cur=neighbors[0]
            path.append(cur)
            if cur in node_pixels:
                return cur, path
    for p in node_pixels:
        r,c=p
        for dr,dc in neigh:
            nr,nc=r+dr,c+dc
            if 0<=nr<H and 0<=nc<W and skel[nr,nc]:
                if (nr,nc) in visited:
                    continue
                res = walk_from((nr,nc))
                if not res:
                    continue
                end_pixel, path = res
                node_u = f"junction_{p[0]}_{p[1]}"
                node_v = f"junction_{end_pixel[0]}_{end_pixel[1]}"
                G.add_edge(node_u, node_v, type='wire', pixels=path)
                for pix in path:
                    visited.add(pix)
    for t in component_terminals:
        nearest = None; nearest_dist=99999
        for n in G.nodes:
            if G.nodes[n]['type']=='junction':
                d = (G.nodes[n]['x']-t['x'])**2 + (G.nodes[n]['y']-t['y'])**2
                if d<nearest_dist:
                    nearest_dist=d; nearest=n
        if nearest:
            G.add_edge(f"term_{t['id']}_{t['term']}", nearest, type='connection')
    return G