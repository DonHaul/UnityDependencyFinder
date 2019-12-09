import yaml

from unityparser import UnityDocument

asset = "/media/ramiro/DATA/User/Desktop/InMotion/Inmotion--Jogo/InMotion_GameFiles/Assets/Scenes/Minigames/UpperLimb/8 Glass cleaner.unity"

doc = UnityDocument.load_yaml(asset)

print(doc.entries)