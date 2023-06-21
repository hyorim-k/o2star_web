import streamlit as st
import torch
from PIL import Image
import numpy as np
import cv2
from pathlib import Path

# Config
st.set_page_config(page_title='부착생물 탐지', page_icon='🔎', layout='wide')
st.title("굴 부착생물 탐지")

c1, c2 = st.columns(2)
c1.write('**부자(라인) 당 케이지 수를 입력하세요**')
cages = c1.number_input("케이지 수", min_value=0, value=0)
c2.write(f"**{cages*2}장의 이미지를 업로드 해 주세요**")
# Upload images
uploaded_images = c2.file_uploader("이미지를 업로드 해 주세요.", type=["jpg", "jpeg", "png"], accept_multiple_files=True, key="file_upload")


# # YOLOv5 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5_40epochs_best.pt')
def detect_objects(image):
    # Perform object detection
    results = model(image)

    # Get the detected objects
    objects = results.xyxy[0]

    # Draw bounding boxes on the image
    image = np.array(image)
    for obj in objects:
        x1, y1, x2, y2, conf, cls = obj.tolist()
        if cls == 0:
            color = (255, 0, 0)  # Red color for "barnacles" class
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
        elif cls == 1:
            color = (0, 0, 255)  # Blue color for "polychaete" class
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)

    # Return detection results
    return results, Image.fromarray(image)


if st.button("탐지 시작"):
    abnormal_cnt = 0
    row1, row2, row3 = st.columns(3)  # Create three columns for displaying images

    for i, uploaded_image in enumerate(uploaded_images):
        # Load and display the image
        image = Image.open(uploaded_image)

        # Perform object detection and draw bounding boxes
        results, annotated_image = detect_objects(np.array(image))

        if i % 3 == 0:
            with row1:
                st.image(annotated_image)
                if len(results.xyxy[0]) >= 2:
                    for result in results.xyxy[0]:
                        x1, y1, x2, y2, conf, cls = result.tolist()
                        if cls == 2:
                            pass
                        elif cls == 0:
                            st.write(f"**결과: 따개비, 신뢰도: {conf:.2f}**")
                            abnormal_cnt += 1
                        else:
                            st.write(f"**결과: 다모류, 신뢰도: {conf:.2f}**")
                            abnormal_cnt += 1
                else:
                    st.write(f"**정상**")
        elif i % 3 == 1:
            with row2:
                st.image(annotated_image)
                if len(results.xyxy[0]) >= 2:
                    for result in results.xyxy[0]:
                        x1, y1, x2, y2, conf, cls = result.tolist()
                        if cls == 2:
                            pass
                        elif cls == 0:
                            st.write(f"**결과: 따개비, 신뢰도: {conf:.2f}**")
                            abnormal_cnt += 1
                        else:
                            st.write(f"**결과: 다모류, 신뢰도: {conf:.2f}**")
                            abnormal_cnt += 1
                else:
                    st.write(f"**정상**")
        else:
            with row3:
                st.image(annotated_image)
                if len(results.xyxy[0]) >= 2:
                    for result in results.xyxy[0]:
                        x1, y1, x2, y2, conf, cls = result.tolist()
                        if cls == 2:
                            pass
                        elif cls == 0:
                            st.write(f"**결과: 따개비, 신뢰도: {conf:.2f}**")
                            abnormal_cnt += 1
                        else:
                            st.write(f"**결과: 다모류, 신뢰도: {conf:.2f}**")
                            abnormal_cnt += 1
                else:
                    st.write(f"**정상**")

    if (abnormal_cnt/(cages*2)) >= 50.0:
        st.error("부착생물이 과반수이므로 세척작업이 필요합니다.")
    else:
        st.success("부착생물이 과반수 미만이므로 세척작업이 필요 없습니다.")