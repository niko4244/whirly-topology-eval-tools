from PIL import Image, ImageDraw
import io, json

def create_trace_overlay(image_bytes, detections):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    overlay = Image.new("RGBA", image.size)
    draw = ImageDraw.Draw(overlay)
    
    # Draw detected components
    svg_boxes = []
    graph_nodes = []
    graph_edges = []
    for i, det in enumerate(detections):
        x, y, w, h = det["bbox"]
        draw.rectangle([x, y, x+w, y+h], outline="red", width=2)
        svg_boxes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" stroke="red" fill="none" stroke-width="2"/>')
        graph_nodes.append({"id": i, "xy": [x + w//2, y + h//2], "class": det["class"]})
        if det["class"] == "wire":
            graph_edges.append({"id": i, "from": [x, y], "to": [x+w, y+h]})

    # Compose SVG overlay
    svg_content = "\n".join(svg_boxes)
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{image.size[0]}" height="{image.size[1]}">{svg_content}</svg>'
    graph_json = {"nodes": graph_nodes, "edges": graph_edges}
    return {"svg": svg, "graph_json": graph_json}