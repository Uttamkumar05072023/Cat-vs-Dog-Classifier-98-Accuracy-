from customtkinter import *
from PIL import Image
from tkinter import filedialog,messagebox
import torch
import torchvision.transforms as transforms

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])
model = torch.jit.load("cat_vs_dog_using_resnet18.pt",map_location=torch.device('cpu'))
model.eval()

class App(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x500")
        self.title("Cat Vs Dog Classifier (98% Accuracy)")
        self.resizable(False, False)
        self.iconbitmap("assets/icon.ico")
        self.configure(fg_color="light blue")
        self.img_label = CTkLabel(self,text="Sample Image",font=CTkFont(family='arial',size=40,weight='bold'),text_color='red',image=CTkImage(light_image=Image.open("assets/cat.247.jpg"),dark_image=Image.open("assets/cat.247.jpg"),size=(300,300)))
        self.img_label.pack(pady=20)
        self.prediction = CTkLabel(self,text="Prediction Result",font=CTkFont(family='arial',size=50,weight='bold'),text_color='green')
        self.prediction.pack(pady=10)

        select_button = CTkButton(self,text="Select Image",font=CTkFont(family='arial',size=20,weight='bold'),command=self.Select_image)
        select_button.pack(pady=10,padx=70,side='left')
        predict_button = CTkButton(self,text="Predict",font=CTkFont(family='arial',size=20,weight='bold'),command=self.Predict)
        predict_button.pack(pady=10,padx=20,side='left')

        self.filepath = ""
        self.mainloop()
    
    def Select_image(self):
        self.filepath = filedialog.askopenfilename(title="Select an image of Cat or Dog",filetypes=(("jpg files", "*.jpg"),("jpeg files", "*.jpeg"),("png files", "*.png"),("all files", "*.*")))
        if self.filepath != "":
            self.img_label.configure(text="",image=CTkImage(light_image=Image.open(self.filepath),dark_image=Image.open(self.filepath),size=(300,300)))

    def Predict(self):
        if self.filepath == "":
            messagebox.showerror("Error","Please select an image!")
            return
        img = Image.open(self.filepath).convert("RGB")
        img = transform(img).unsqueeze(0)
        with torch.no_grad():
            result = model(img)
            pred = torch.argmax(result,1)
            self.prediction.configure(text="It's a Dog" if pred.item() == 1 else "It's a Cat")

if __name__ == "__main__":
    App()