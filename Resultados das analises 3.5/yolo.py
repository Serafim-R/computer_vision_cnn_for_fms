from ultralytics import YOLO
import os
# Load a pretrained YOLOv8x model
model = YOLO('/scratch/global/jidsilva/cnn_gemeos/runs/detect/p1080/weights/best.pt')
print('model loaded successfully')
source='/scratch/global/jidsilva/testes_iluminacoes/PDPETRO/Experimento_luz/'

results = list()
def analyzes_files_in_directory(directory):
    for root, dirs, files in os.walk(directory):
        if len(files) > 0:
            print(root)
            results = model(root, stream=False, save_txt=True, save_conf=True, conf=0.5)


analyzes_files_in_directory(source)
print('finishing the predictions')

for r in results:
   print(r.path,': ',r.probs.top1,'with: ', r.probs.top1conf, ' confidence')

