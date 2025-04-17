import yaml

data_config = {
    "path": "dataset",
    "train": "images/train",
    "val": "images/val",
    "nc": 1,
    "names": ["plane"],
}

yaml_path = "dataset/data.yaml"
with open(yaml_path, "w") as file:
    yaml.dump(data_config, file, default_flow_style=False)

print(f"YOLO config file saved as {yaml_path}")
