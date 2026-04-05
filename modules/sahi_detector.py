# modules/sahi_detector.py
import streamlit as st
from sahi import AutoDetectionModel
from sahi.predict import get_sliced_prediction
from ultralytics import YOLO
import cv2
import numpy as np
from config import MODEL_PATH, BOX_RAW
from modules.image_utils import compute_optimal_slice

@st.cache_resource
def load_sahi_model(conf):
    return AutoDetectionModel.from_pretrained(
        model_type="yolov8",
        model_path=MODEL_PATH,
        confidence_threshold=conf,
        device="cpu"
    )

@st.cache_resource
def load_yolo_model():
    return YOLO(MODEL_PATH)

def get_model(use_sahi, conf_thres):
    if use_sahi:
        return load_sahi_model(conf_thres)
    return load_yolo_model()

def process_image(img_np, params):
    """Core detection function."""
    h, w = img_np.shape[:2]
    if params['use_clahe']:
        from modules.image_utils import apply_lab_clahe
        img_proc = apply_lab_clahe(img_np)
    else:
        img_proc = img_np.copy()
    
    annotated = img_proc.copy()
    boxes_all = []
    confs_all = []
    slice_previews = []
    slice_counts = []
    
    if params['use_sahi']:
        max_slices = params.get('max_slices', 25)
        min_slice = params.get('min_slice', 256)
        overlap_ratio = params.get('overlap_ratio', 0.2)
        
        slice_size = compute_optimal_slice(h, w, max_slices=max_slices, min_slice=min_slice)
        stride = int(slice_size * (1 - overlap_ratio))
        y_steps = list(range(0, h, stride))
        x_steps = list(range(0, w, stride))
        
        for yi in y_steps:
            for xi in x_steps:
                y2 = min(yi + slice_size, h)
                x2 = min(xi + slice_size, w)
                slice_img = img_proc[yi:y2, xi:x2].copy()
                slice_img_np = np.array(slice_img)
                result = get_sliced_prediction(
                    slice_img_np, params['model'],
                    slice_height=slice_size, slice_width=slice_size,
                    overlap_height_ratio=overlap_ratio,
                    overlap_width_ratio=overlap_ratio
                )
                for obj in result.object_prediction_list:
                    local_x1, local_y1 = int(obj.bbox.minx), int(obj.bbox.miny)
                    local_x2, local_y2 = int(obj.bbox.maxx), int(obj.bbox.maxy)
                    conf = obj.score.value
                    x1, y1 = local_x1 + xi, local_y1 + yi
                    x2, y2 = local_x2 + xi, local_y2 + yi
                    boxes_all.append([x1, y1, x2, y2])
                    confs_all.append(conf)
                    cv2.rectangle(slice_img, (local_x1, local_y1), (local_x2, local_y2), BOX_RAW, 2)
                slice_previews.append(slice_img)
                slice_counts.append(len(result.object_prediction_list))
    else:
        results = params['model'].predict(source=img_proc, conf=params['conf_thres'], verbose=False)
        for box in results[0].boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            boxes_all.append([int(x1), int(y1), int(x2), int(y2)])
            confs_all.append(float(box.conf[0]))
    
    thickness = max(2, int(min(h, w) / 400))
    for (x1, y1, x2, y2), conf in zip(boxes_all, confs_all):
        color = (int(255*(1-conf)), int(255*conf), 0)
        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, thickness)
    
    # DBSCAN clustering (dipanggil dari modul terpisah)
    if len(boxes_all) > 0 and params['use_dbscan']:
        from modules.dbscan_cluster import apply_dbscan
        total_trees, coords = apply_dbscan(boxes_all, params['eps_factor'], h, w)
        # gambar lingkaran
        from config import CENTROID_CLUSTER, FINAL_TREE
        radius = max(6, int(min(h, w) / 150))
        for (cx, cy) in coords:
            cv2.circle(annotated, (cx, cy), radius, CENTROID_CLUSTER, -1)
            cv2.circle(annotated, (cx, cy), radius+6, FINAL_TREE, 3)
    else:
        total_trees = len(boxes_all)
        coords = []
    
    avg_conf = float(np.mean(confs_all)) if confs_all else 0
    return {
        'annotated': annotated,
        'coords': coords,
        'total_trees': total_trees,
        'raw_detections': len(boxes_all),
        'avg_conf': avg_conf,
        'slice_previews': slice_previews,
        'slice_counts': slice_counts,
        'img_shape': (h, w)
    }