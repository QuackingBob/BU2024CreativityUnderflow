# app/forms.py
from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'content', 'img_content']
        widgets = {
            'title': forms.TextInput(attrs={
                'id': 'documentTitle',
                'placeholder': 'Document Title',
            }),
            'content': forms.Textarea(attrs={
                'id': 'editable-code',
                'placeholder': 'Type your code or LaTeX here...',
            }),
        }
        
