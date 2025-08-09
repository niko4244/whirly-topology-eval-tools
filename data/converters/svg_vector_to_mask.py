import cairocffi as cairo  # or import cairo from pycairo if you prefer
from svgpathtools import svg2paths2, parse_path
from shapely.geometry import Polygon, MultiPolygon
from PIL import Image
import numpy as np
import os

def svg_path_to_shapely(svg_path_str, samples=100):
    """
    Convert SVG path string to a Shapely Polygon by sampling points.
    If the path is closed, treats as a filled area; otherwise, returns None.
    """
    path = parse_path(svg_path_str)
    points = []
    for segment in path:
        for t in np.linspace(0, 1, samples):
            pt = segment.point(t)
            points.append((pt.real, pt.imag))
    # Detect closure
    if len(points) < 3 or points[0] != points[-1]:
        points.append(points[0])
    poly = Polygon(points)
    if not poly.is_valid:
        poly = poly.buffer(0)
    return poly

def rasterize_geometries_to_mask(geometries, img_size=(1024, 1024), scale=1.0, translate=(0,0)):
    """
    Rasterize a list of polygons to a binary mask using Cairo.
    """
    width, height = img_size
    surface = cairo.ImageSurface(cairo.FORMAT_A8, width, height)
    ctx = cairo.Context(surface)
    ctx.set_source_rgb(0, 0, 0)
    ctx.paint()
    ctx.set_source_rgb(1, 1, 1)

    for geom in geometries:
        if geom.is_empty: continue
        if isinstance(geom, Polygon):
            polygons = [geom]
        elif isinstance(geom, MultiPolygon):
            polygons = geom.geoms
        else:
            continue
        for poly in polygons:
            coords = [(scale * x + translate[0], scale * y + translate[1]) for x, y in poly.exterior.coords]
            ctx.move_to(*coords[0])
            for x, y in coords[1:]:
                ctx.line_to(x, y)
            ctx.close_path()
            ctx.fill_preserve()
            for interior in poly.interiors:
                icoords = [(scale * x + translate[0], scale * y + translate[1]) for x, y in interior.coords]
                ctx.move_to(*icoords[0])
                for x, y in icoords[1:]:
                    ctx.line_to(x, y)
                ctx.close_path()
                ctx.fill_preserve()
            ctx.new_path()
    buf = surface.get_data()
    mask = np.frombuffer(buf, np.uint8).reshape((height, width))
    return mask

def svg_file_to_class_masks(svg_path, output_mask_dir, classes, img_size=(1024,1024), scale=1.0):
    """
    Given a labeled SVG, generates per-class binary mask PNGs.
    Expects SVG paths to have 'data-label' attribute.
    """
    os.makedirs(output_mask_dir, exist_ok=True)
    paths, attribs, _ = svg2paths2(svg_path)
    class_geoms = {cls: [] for cls in classes}
    for path, attr in zip(paths, attribs):
        label = attr.get('data-label')
        if label in classes:
            poly = svg_path_to_shapely(path.d())
            if poly: class_geoms[label].append(poly)
    for cls, geoms in class_geoms.items():
        if geoms:
            mask = rasterize_geometries_to_mask(geoms, img_size, scale)
            mask_img = Image.fromarray(mask)
            mask_img.save(os.path.join(output_mask_dir, f"{cls}_mask.png"))
        else:
            # Empty mask
            Image.new('L', img_size, 0).save(os.path.join(output_mask_dir, f"{cls}_mask.png"))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Rasterize SVG vector labels to per-class mask PNGs")
    parser.add_argument("svg_path", type=str, help="Input SVG file")
    parser.add_argument("output_mask_dir", type=str, help="Output mask directory")
    parser.add_argument("--classes", type=str, nargs="+", required=True, help="List of class labels to extract")
    parser.add_argument("--img_size", type=int, nargs=2, default=[1024,1024], help="Output mask size")
    parser.add_argument("--scale", type=float, default=1.0, help="Coordinate scale factor")
    args = parser.parse_args()
    svg_file_to_class_masks(
        args.svg_path,
        args.output_mask_dir,
        args.classes,
        tuple(args.img_size),
        args.scale
    )
    print(f"Saved masks for classes {args.classes} to {args.output_mask_dir}")