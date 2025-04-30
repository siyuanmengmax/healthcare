import json
import anthropic
from django.conf import settings
from django.utils import timezone
from .models import MedicalRecord, MedicalRecordAnalysis


class ClaudeMedicalAnalyzer:
    """Utilizes Claude AI to analyze medical documents and extract key information."""

    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=settings.ANTHROPIC_API_KEY,
        )

    def analyze_medical_document(self, medical_record):
        """Analyze a medical document using Claude AI and extract key information."""
        document_text = medical_record.content
        attachment_filename = medical_record.attachments.name.split('/')[
            -1] if medical_record.attachments else "No attachment"

        prompt = f"""
        You are a medical document analysis expert. Please analyze the following medical document and extract key information:

        Document Type: {medical_record.get_record_type_display()}
        Document Description: {medical_record.description}
        Document Content:
        {document_text}
        Attachment Filename: {attachment_filename}

        Please extract and organize the following information:
        1. Diagnosis results
        2. Medication details
        3. Treatment plans
        4. Medical examination results
        5. Abnormal values that require attention

        Output the results in JSON format using the following structure:
        {{
            "diagnosis": ["Diagnosis 1", "Diagnosis 2", ...],
            "medications": [
                {{"name": "Medication name", "dosage": "Dosage", "frequency": "Usage frequency"}},
                ...
            ],
            "treatments": ["Treatment 1", "Treatment 2", ...],
            "test_results": [
                {{"test": "Test name", "result": "Result", "normal_range": "Normal range"}},
                ...
            ],
            "abnormal_values": ["Abnormal value 1", "Abnormal value 2", ...]
        }}

        If certain information is not present in the document, please use empty arrays for those categories.
        """

        try:
            response = self.client.messages.create(
                model="Claude 3.7 Sonnet",
                max_tokens=1000,
                temperature=0,
                system="You are a medical document analysis assistant that extracts key information from medical texts and formats it as structured data.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            analysis_result = response.content[0].text

            try:
                analysis_data = json.loads(analysis_result)
            except json.JSONDecodeError:
                import re
                json_match = re.search(r'({.*})', analysis_result.replace('\n', ''), re.DOTALL)
                if json_match:
                    analysis_data = json.loads(json_match.group(1))
                else:
                    analysis_data = {
                        "diagnosis": [],
                        "medications": [],
                        "treatments": [],
                        "test_results": [],
                        "abnormal_values": []
                    }

            return {
                'analysis_text': analysis_result,
                'diagnosis': analysis_data.get('diagnosis', []),
                'medications': analysis_data.get('medications', []),
                'treatments': analysis_data.get('treatments', []),
                'abnormal_values': analysis_data.get('abnormal_values', []),
            }

        except Exception as e:
            return {
                'analysis_text': f"Error analyzing document: {str(e)}",
                'diagnosis': [],
                'medications': [],
                'treatments': [],
                'abnormal_values': [],
            }

    def save_analysis_result(self, medical_record, analysis_result):
        try:
            analysis, created = MedicalRecordAnalysis.objects.update_or_create(
                medical_record=medical_record,
                defaults={
                    'analysis_text': analysis_result['analysis_text'],
                    'diagnosis': analysis_result['diagnosis'],
                    'medications': analysis_result['medications'],
                    'treatments': analysis_result['treatments'],
                    'abnormal_values': analysis_result['abnormal_values'],
                }
            )
            return analysis
        except Exception as e:
            print(f"Error saving analysis: {str(e)}")
            return None