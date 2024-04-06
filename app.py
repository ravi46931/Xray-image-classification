import os
from PIL import Image
import streamlit as st

from xray.constants import *
from xray.pipeline.pred_pipeline import PredPipeline


def main():
    st.title("Xray lung classifier")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:

        # Converting images
        image = Image.open(uploaded_file)

        # save the image
        os.makedirs("images", exist_ok=True)
        os.path.join("images", "image.jpeg")
        file_path = "images/image.jpeg"
        image.save(file_path)

        prediction_pipeline = PredPipeline()
        prediction = prediction_pipeline.run_prediction(image)

        print(prediction)
        if prediction == "Normal":
            st.text_area(label="Prediction:", value="Normal", height=IMAGE_HEIGHT)
        elif prediction == "Pneumonia":
            st.text_area(label="Prediction:", value="PNEUMONIA", height=IMAGE_HEIGHT)

        # Display the uploaded image
        image_resized = image.resize(
            (TARGET_WIDTH, int(TARGET_WIDTH * image.height / image.width))
        )
        st.image(image_resized, caption="Uploaded Image", use_column_width=False)


if __name__ == "__main__":
    main()
