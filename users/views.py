import requests
import pytesseract
from PIL import Image
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from django.views import generic
import openai

from .forms import CustomUserCreationForm
from .forms import ImageToTextForm


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class TextGeneratorView(LoginRequiredMixin, View):
    template_name = 'text_generator.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        title = request.POST.get('product_title', '')
        try:
            generated_text = self.generate_text(title)
            context = {'title': title, 'generated_text': generated_text}
            return render(request, self.template_name, context)

        except Exception as e:
            # Handle errors appropriately
            print(f"Error: {str(e)}")
            error_message = "An error occurred while processing your request."
            context = {'title': title, 'generated_text': error_message}
            return render(request, self.template_name, context)

    def generate_text(self, title):
        # Use the SDK provided by Google AI Studio or the equivalent service
        # Make sure to replace 'openai' with the correct library if needed
        openai.api_key = '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'  # Replace with your API key
        prompt = f"Generate a product description for a product with the title: {title}"
        response = openai.Completion.create(
            engine="text-davinci-003",  # Replace with the correct engine
            prompt=prompt,
            max_tokens=200
        )
        return response.choices[0].text.strip()

class ImageToTextView(LoginRequiredMixin, View):
    template_name = 'image_to_text.html'

    def get(self, request):
        form = ImageToTextForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ImageToTextForm(request.POST, request.FILES)
        if form.is_valid():
            image_text = self.process_image(request.FILES['image'])
            context = {'form': form, 'image_text': image_text}
        else:
            context = {'form': form}

        return render(request, self.template_name, context)

    def process_image(self, image):
        try:
            # Provide the path to the Tesseract executable
            pytesseract.pytesseract.tesseract_cmd = r'C:\Users\ASUS\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
            img = Image.open(image)
            extracted_text = pytesseract.image_to_string(img)
            return extracted_text.strip()
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return "An error occurred while processing the image."