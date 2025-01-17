
import torch
from PIL import Image
from open_clip import tokenizer
import open_clip
import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""

def test_inference():
    model, _, preprocess = open_clip.create_model_and_transforms('ViT-B-32-quickgelu', pretrained='laion400m_e32')
    checkpoint = torch.load("/rapids/notebooks/open_clip/src/logs/OpenAIFlickr8kTraining7/checkpoints/epoch_30.pt")
    #print(checkpoint['state_dict'])
    model.load_state_dict(checkpoint['state_dict'],strict=False)

    current_dir = os.path.dirname(os.path.realpath(__file__))

    image = preprocess(Image.open("/rapids/notebooks/host/ImagesOpenClipTrain/424379231_23f1ade134.jpg")).unsqueeze(0)
    text = tokenizer.tokenize(["a diagram", "a fox", "a cat"])

    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text)
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        
        text_probs = (100.0 * image_features @ text_features.T).softmax(dim=-1)
    

    print("Label probs:", text_probs)
    

test_inference()
