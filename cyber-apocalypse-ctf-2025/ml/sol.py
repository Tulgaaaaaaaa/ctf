import torch

data = torch.load("eldorian_artifact.pth", map_location="cpu")  # Load file on CPU
print(type(data))  # Check what type of object it contains

