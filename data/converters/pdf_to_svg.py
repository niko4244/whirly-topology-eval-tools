import os
import subprocess

def pdf_to_svg(pdf_path, output_dir):
    """
    Convert each page of a PDF to an SVG file using pdf2svg.

    Args:
        pdf_path (str): Path to the PDF file.
        output_dir (str): Directory to save SVG files.

    Returns:
        List[str]: List of SVG file paths.
    """
    os.makedirs(output_dir, exist_ok=True)
    # pdf2svg syntax: pdf2svg input.pdf output_page_%d.svg all
    base = os.path.splitext(os.path.basename(pdf_path))[0]
    output_pattern = os.path.join(output_dir, f"{base}_page_%d.svg")
    cmd = ["pdf2svg", pdf_path, output_pattern, "all"]
    subprocess.run(cmd, check=True)
    # Find output SVGs
    svg_files = sorted([
        os.path.join(output_dir, f)
        for f in os.listdir(output_dir)
        if f.startswith(base) and f.endswith(".svg")
    ])
    return svg_files

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert PDF pages to SVG files")
    parser.add_argument("pdf_path", type=str, help="Path to input PDF")
    parser.add_argument("output_dir", type=str, help="Directory to save SVGs")
    args = parser.parse_args()
    svgs = pdf_to_svg(args.pdf_path, args.output_dir)
    print("SVG files:")
    for svg in svgs:
        print(svg)