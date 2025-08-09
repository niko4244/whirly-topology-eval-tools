import React, { useState, useRef } from "react";
import { uploadCircuitImage } from "./api";
import "./CircuitUploadView.css";

export default function CircuitUploadView() {
  const [svgContent, setSvgContent] = useState("");
  const [graph, setGraph] = useState(null);
  const [highlightedEdges, setHighlightedEdges] = useState(new Set());
  const svgRef = useRef();

  async function handleFile(e) {
    const file = e.target.files[0];
    if (!file) return;
    const data = await uploadCircuitImage(file);
    setSvgContent(data.svg);
    setGraph(data.graph);
    setHighlightedEdges(new Set());
  }

  // Click-to-trace: highlight all edges from clicked node
  function handleSvgClick(e) {
    if (!graph) return;
    // Find nearest node to click
    const pt = getSvgCoords(e, svgRef.current);
    let closest = null, minDist = 1e6;
    graph.nodes.forEach(n => {
      const [x, y] = n.xy;
      const d = Math.hypot(x - pt.x, y - pt.y);
      if (d < minDist) {
        minDist = d;
        closest = n.id;
      }
    });
    if (closest !== null && minDist < 10) { // threshold px
      // BFS trace
      const que = [closest], visited = new Set([closest]);
      const newEdges = new Set();
      while (que.length) {
        const cur = que.shift();
        graph.edges.forEach(e => {
          if (e.u === cur || e.v === cur) {
            newEdges.add(edgeId(e));
            const other = e.u === cur ? e.v : e.u;
            if (!visited.has(other)) {
              visited.add(other);
              que.push(other);
            }
          }
        });
      }
      setHighlightedEdges(newEdges);
    }
  }

  function edgeId(e) {
    // Unique string for edge
    return `${e.u}-${e.v}`;
  }

  function getSvgCoords(evt, svgEl) {
    const pt = svgEl.createSVGPoint();
    pt.x = evt.clientX;
    pt.y = evt.clientY;
    const ctm = svgEl.getScreenCTM().inverse();
    const loc = pt.matrixTransform(ctm);
    return { x: loc.x, y: loc.y };
  }

  // Render SVG, highlight traced edges
  function renderSvg() {
    if (!svgContent) return null;
    const parser = new DOMParser();
    const doc = parser.parseFromString(svgContent, "image/svg+xml");
    const svgEl = doc.documentElement;
    // Highlight edges
    if (graph) {
      const edgeSet = new Set([...highlightedEdges]);
      // Find polylines (wires)
      Array.from(svgEl.querySelectorAll("polyline")).forEach((pl, idx) => {
        const e = graph.edges[idx];
        if (edgeSet.has(edgeId(e))) {
          pl.setAttribute("class", "highlighted-edge");
        }
      });
    }
    // Return SVG inside a wrapper div
    return (
      <div className="svg-wrap" onClick={handleSvgClick}>
        <svg
          ref={svgRef}
          dangerouslySetInnerHTML={{ __html: svgEl.innerHTML }}
          width={svgEl.getAttribute("width")}
          height={svgEl.getAttribute("height")}
        />
      </div>
    );
  }

  return (
    <div className="circuit-upload-view">
      <h2>Upload circuit diagram</h2>
      <input type="file" accept="image/*" onChange={handleFile} />
      {svgContent && (
        <div>
          <h3>Click a node to trace circuit</h3>
          {renderSvg()}
        </div>
      )}
    </div>
  );
}