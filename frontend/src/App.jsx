import React, {useState, useRef} from 'react';
import axios from 'axios';

export default function App() {
  const [svgText, setSvgText] = useState(null);
  const [graph, setGraph] = useState(null);
  const [highlightedEdges, setHighlightedEdges] = useState(new Set());
  const fileRef = useRef();

  async function handleUpload(e){
    const f = e.target.files[0];
    const fd = new FormData();
    fd.append('file', f);
    const resp = await axios.post('/upload', fd, { headers: { 'Content-Type': 'multipart/form-data' } });
    setSvgText(resp.data.svg);
    setGraph(resp.data.graph);
    setHighlightedEdges(new Set());
  }

  function handleSvgClick(evt){
    if(!graph) return;
    // Find nearest node to click
    const svg = evt.currentTarget;
    const pt = svg.createSVGPoint();
    pt.x = evt.clientX;
    pt.y = evt.clientY;
    const ctm = svg.getScreenCTM().inverse();
    const loc = pt.matrixTransform(ctm);
    let closest = null, minDist = 1e6;
    graph.nodes.forEach(n => {
      const [x, y] = n.xy;
      const d = Math.hypot(x - loc.x, y - loc.y);
      if (d < minDist) { minDist = d; closest = n.id; }
    });
    if (closest !== null && minDist < 12) { // threshold px
      // BFS trace
      const queue = [closest], visited = new Set([closest]);
      const newEdges = new Set();
      while(queue.length) {
        const cur = queue.shift();
        graph.edges.forEach(e => {
          if (e.u === cur || e.v === cur) {
            newEdges.add(`${e.u}-${e.v}`);
            const other = e.u === cur ? e.v : e.u;
            if (!visited.has(other)) { visited.add(other); queue.push(other); }
          }
        });
      }
      setHighlightedEdges(newEdges);
    }
  }

  function renderSvg() {
    if(!svgText) return null;
    // Parse SVG string and inject highlights
    const parser = new DOMParser();
    const doc = parser.parseFromString(svgText, "image/svg+xml");
    const svgEl = doc.documentElement;
    if(graph) {
      // Highlight edges as blue
      graph.edges.forEach((e, idx) => {
        const poly = svgEl.querySelector(`#edge${idx}`);
        if (poly && highlightedEdges.has(`${e.u}-${e.v}`)) {
          poly.setAttribute("stroke", "#00f");
          poly.setAttribute("stroke-width", "4");
          poly.setAttribute("opacity", "0.7");
        }
      });
      // Highlight clicked component rectangles if you wish
    }
    return (
      <div style={{border:'1px solid #ccc', marginTop: 16}}>
        <svg
          width={svgEl.getAttribute("width")}
          height={svgEl.getAttribute("height")}
          ref={fileRef}
          onClick={handleSvgClick}
          dangerouslySetInnerHTML={{__html: svgEl.innerHTML}}
          style={{cursor:'pointer'}}
        />
      </div>
    );
  }

  return (
    <div style={{padding:24,maxWidth:680,margin:'auto'}}>
      <h2>Whirly Traceable Circuit MVP</h2>
      <input type="file" accept="image/*" onChange={handleUpload} />
      {svgText && (
        <>
          <h4>Click a node (red box or wire endpoint) to trace</h4>
          {renderSvg()}
        </>
      )}
    </div>
  );
}