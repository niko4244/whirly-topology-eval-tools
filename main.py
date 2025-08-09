from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import io
from PIL import Image
import numpy as np
import cv2
from skimage.morphology import skeletonize
import networkx as nx
import base64

app = FastAPI()

def preprocess_image(img_bytes):
    img = Image.open(io.BytesIO(img_bytes)).convert('L')
    arr = np.array(img)
    arr = cv2.bilateralFilter(arr, 9, 75, 75)  # Denoise
    arr = cv2.adaptiveThreshold(arr, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY, 31, 10)
    # Deskew (optional, not implemented here)
    return arr

def wires_to_graph(binary_img):
    sk = skeletonize(binary_img > 0).astype(np.uint8)
    h, w = sk.shape
    offsets = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
    G = nx.Graph()
    node_map = {}
    for y in range(h):
        for x in range(w):
            if sk[y,x]:
                neighbors = sum(1 for dx,dy in offsets if 0<=x+dx<w and 0<=y+dy<h and sk[y+dy,x+dx])
                if neighbors != 2:
                    node_id = len(node_map)
                    node_map[(x,y)] = node_id
                    G.add_node(node_id, xy=(x,y))
    # Walk edges
    for (sx,sy), nid in node_map.items():
        for dx,dy in offsets:
            nxp, nyp = sx+dx, sy+dy
            path = [(sx,sy)]
            if 0<=nxp<w and 0<=nyp<h and sk[nyp,nxp]:
                cx,cy = nxp,nyp
                while True:
                    path.append((cx,cy))
                    if (cx,cy) in node_map and (cx,cy) != (sx,sy):
                        G.add_edge(nid, node_map[(cx,cy)], pixels=path)
                        break
                    found = False
                    for ddx,ddy in offsets:
                        tx,ty = cx+ddx, cy+ddy
                        if 0<=tx<w and 0<=ty<h and sk[ty,tx] and (tx,ty) not in path:
                            cx,cy = tx,ty
                            found = True
                            break
                    if not found:
                        break
    return G, sk

def graph_to_svg(G, sk):
    # Simple SVG render: wires as polylines, nodes as circles
    h, w = sk.shape
    svg_lines = []
    for u, v, data in G.edges(data=True):
        points = data['pixels']
        pts = " ".join([f"{x},{y}" for x,y in points])
        svg_lines.append(f'<polyline points="{pts}" style="fill:none;stroke:#000;stroke-width:2"/>')
    for n, data in G.nodes(data=True):
        x, y = data['xy']
        svg_lines.append(f'<circle cx="{x}" cy="{y}" r="2" fill="#f00"/>')
    svg = f'<svg width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">\n' + "\n".join(svg_lines) + "\n</svg>"
    return svg

def graph_to_json(G):
    nodes = []
    edges = []
    for n, data in G.nodes(data=True):
        nodes.append({"id": n, "xy": data["xy"]})
    for u, v, data in G.edges(data=True):
        edges.append({"u": u, "v": v, "pixels": data["pixels"]})
    return {"nodes": nodes, "edges": edges}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    img_bytes = await file.read()
    bin_img = preprocess_image(img_bytes)
    G, sk = wires_to_graph(bin_img)
    svg = graph_to_svg(G, sk)
    json_graph = graph_to_json(G)
    # Optionally encode SVG as data-uri for frontend
    svg_b64 = base64.b64encode(svg.encode()).decode()
    return JSONResponse({
        "svg": svg,
        "svg_base64": f"data:image/svg+xml;base64,{svg_b64}",
        "graph": json_graph,
        "width": sk.shape[1],
        "height": sk.shape[0]
    })