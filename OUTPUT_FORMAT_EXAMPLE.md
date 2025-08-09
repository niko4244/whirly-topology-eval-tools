```json
{
  "image_id": "img_0001",
  "svg": "<svg> ... layered SVG with per-element data-id ...</svg>",
  "components": [
    {"id": "C1", "type": "Resistor", "bbox": [x1,y1,x2,y2], "terminals":[[x,y],[x,y]], "confidence": 0.93, "mask_rle": "..."},
    {"id": "U1", "type": "IC_SOIC8", "bbox": [...], "pins": 8, "confidence": 0.88}
  ],
  "wires": [
    {"id": "w1", "path": "M ...", "junctions":[{"x":..., "y":...}], "confidence": 0.82}
  ],
  "graph": {
    "nodes": [{"id":"n1", "type":"junction", "x":..., "y":...}, {"id":"U1.pwr", ...}],
    "edges": [{"u":"U1.pwr","v":"n1","type":"wire"}, {"u":"R1.p1","v":"n1","type":"component"}]
  },
  "analysis": [
    {"type":"short","severity":"high","message":"Possible VCC-GND short at junction (x,y)","evidence": {"nodes":["n3","n4"]}},
    {"type":"open_circuit","severity":"low","message":"Node n7 is floating (no ground or VCC)","evidence": {"node":"n7"}}
  ]
}
```