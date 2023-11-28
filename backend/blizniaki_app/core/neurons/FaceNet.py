import torch.nn as nn
import torch.nn.functional as F


class FaceNet(nn.Module):
    def __init__(self):
        super(FaceNet, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=64, kernel_size=3, stride=2),
            nn.BatchNorm2d(64),
            nn.GELU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        self.layer2 = nn.Sequential(
            nn.Conv2d(in_channels=64, out_channels=384, kernel_size=3, padding=2, stride=2),
            nn.BatchNorm2d(384),
            nn.GELU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        self.layer3 = nn.Sequential(
            nn.Conv2d(in_channels=384, out_channels=512, kernel_size=3, padding=2),
            nn.BatchNorm2d(512),
            nn.GELU()
        )
        self.layer4 = nn.Sequential(
            nn.Conv2d(in_channels=512, out_channels=128, kernel_size=3),
            nn.BatchNorm2d(128),
            nn.GELU(),
            nn.Dropout2d(0.2)
        )
        self.fc1 = nn.Sequential(
            nn.Dropout(0.2),
            nn.Linear(14 * 11 * 128, 2048),
            nn.GELU()
        )
        self.fc2 = nn.Sequential(
            nn.Linear(2048, 5)
        )

    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = x.reshape(x.size(0), -1)
        x = self.fc1(x)
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)
