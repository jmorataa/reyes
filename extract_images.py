#!/usr/bin/env python3
"""
Extract images from Jupyter notebooks and save them as PNG files
"""
import json
import base64
import os
import sys

def extract_images_from_notebook(notebook_path, output_dir):
    """Extract all images from a Jupyter notebook"""
    with open(notebook_path, 'r') as f:
        nb = json.load(f)
    
    os.makedirs(output_dir, exist_ok=True)
    
    image_count = 0
    for cell_idx, cell in enumerate(nb['cells']):
        if cell.get('cell_type') != 'code':
            continue
        
        outputs = cell.get('outputs', [])
        for output_idx, output in enumerate(outputs):
            # Check for image data in different output formats
            image_data = None
            
            if output.get('output_type') == 'display_data':
                data = output.get('data', {})
                if 'image/png' in data:
                    image_data = data['image/png']
            elif output.get('output_type') == 'execute_result':
                data = output.get('data', {})
                if 'image/png' in data:
                    image_data = data['image/png']
            
            if image_data:
                # Decode base64 image
                img_bytes = base64.b64decode(image_data)
                
                # Save image
                img_filename = f"{output_dir}/cell_{cell_idx}_output_{output_idx}.png"
                with open(img_filename, 'wb') as img_file:
                    img_file.write(img_bytes)
                
                print(f"Extracted: {img_filename}")
                image_count += 1
    
    return image_count

if __name__ == '__main__':
    # Extract from KNN notebook
    print("Extracting images from knn_cuda_native.ipynb...")
    knn_count = extract_images_from_notebook('knn_cuda_native.ipynb', 'figures/knn')
    print(f"Total KNN images extracted: {knn_count}")
    
    # Extract from KMeans notebook
    print("\nExtracting images from kmeans_cuda_native.ipynb...")
    kmeans_count = extract_images_from_notebook('kmeans_cuda_native.ipynb', 'figures/kmeans')
    print(f"Total KMeans images extracted: {kmeans_count}")
    
    print(f"\nTotal images extracted: {knn_count + kmeans_count}")
