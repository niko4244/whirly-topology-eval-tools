import React from "react";

type SvgElementMeta = {
  id: string,
  class: string,
  bbox: [number,number,number,number],
  confidence?: number
};

type Props = {
  svgText: string,
  elements: SvgElementMeta[],
  onElementClick: (id: string) => void
};

export default function SvgCanvas({svgText, elements, onElementClick}: Props) {
  function handleClick(e: React.MouseEvent) {
    const id = (e.target as SVGElement).id;
    if (id) onElementClick(id);
  }
  return (
    <div className="svg-canvas" style={{border: "1px solid #ccc"}}>
      <div
        dangerouslySetInnerHTML={{__html: svgText}}
        onClick={handleClick}
      />
    </div>
  );
}