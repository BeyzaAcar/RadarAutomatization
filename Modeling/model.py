import torch.nn as nn
import torchvision.models as models

def get_model(num_classes):
    """
    ResNet50 tabanlı model.
    """
    model = models.resnet50(pretrained=True)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    return model
