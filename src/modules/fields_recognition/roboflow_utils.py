from roboflow import Roboflow
#QqFIh94jbW3rDSSKjHc3
rf = Roboflow(api_key="QqFIh94jbW3rDSSKjHc3")
workspace = rf.workspace("socialv2")

workspace.deploy_model(
  model_type="yolov8",
  model_path="./weights/",
  filename="best.pt",
  project_ids=["cccd-uigxn"],
  model_name="fielddetection"
)