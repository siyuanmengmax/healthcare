import json
import anthropic
import re
from django.conf import settings
from .models import MedicalRecordAnalysis


class ClaudeMedicalAnalyzer:
    """Utilizes Claude AI to analyze medical documents and extract key information."""

    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=settings.ANTHROPIC_API_KEY,
        )

    def analyze_medical_document(self, medical_record):
        """Analyze a medical document using Claude AI and extract key information."""
        document_text = medical_record.content

        prompt = f"""
        You are a medical document analysis expert. Please analyze the following medical document and extract key information:

        Document Type: {medical_record.get_record_type_display()}
        Document Description: {medical_record.description}
        Document Content:
        {document_text}

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

        CRITICAL INSTRUCTIONS:
        1. Your entire response must be ONLY valid JSON that can be parsed by json.loads().
        2. Do not include any text before or after the JSON.
        3. Make sure all quotes, commas, brackets are properly balanced and formatted.
        4. If certain information is not present in the document, use empty arrays for those categories.
        5. Do not add any explanation, introduction, or conclusion to your response.
        """

        # try:
        # print(f"Sending request to Claude API with prompt: {prompt}")
        response = self.client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=2000,
            temperature=0,
            system="You are a medical document analysis assistant that extracts key information from medical texts and formats it as structured data.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # print(f"Received response from Claude API: {response}")
        analysis_result = response.content[0].text
        return analysis_result

    def save_analysis_result(self, medical_record, analysis_result):
        try:
            if analysis_result is None:
                print("Error: analysis_result is None")
                return None

            # print(f"Complete analysis_result: {json.dumps(analysis_result, ensure_ascii=False)}")

            # print(analysis_result)
            diagnosis_match = re.search(r'"diagnosis":\s*\[(.*?)\]', analysis_result, re.DOTALL)
            diagnosis = []
            if diagnosis_match:
                try:
                    diagnosis_str = f"[{diagnosis_match.group(1)}]"
                    diagnosis = json.loads(diagnosis_str)
                except:
                    pass
            medications = []
            medications_match = re.search(r'"medications":\s*\[(.*?)\]', analysis_result, re.DOTALL)
            if medications_match:
                med_names = re.findall(r'"name":\s*"([^"]+)"', medications_match.group(1))
                medications = [{"name": name, "dosage": "", "frequency": ""} for name in med_names]
            treatments = []
            treatments_match = re.search(r'"treatments":\s*\[(.*?)\]', analysis_result, re.DOTALL)
            if treatments_match:
                try:
                    treatments_str = f"[{treatments_match.group(1)}]"
                    treatments = json.loads(treatments_str)
                except:
                    pass
            test_results = []
            test_results_match = re.search(r'"test_results":\s*\[(.*?)\]', analysis_result, re.DOTALL)
            if test_results_match:
                try:
                    test_results_str = f"[{test_results_match.group(1)}]"
                    test_results = json.loads(test_results_str)
                except:
                    pass
            abnormal_values = []
            abnormal_values_match = re.search(r'"abnormal_values":\s*\[(.*?)\]', analysis_result, re.DOTALL)
            if abnormal_values_match:
                try:
                    abnormal_values_str = f"[{abnormal_values_match.group(1)}]"
                    abnormal_values = json.loads(abnormal_values_str)
                except:
                    pass
            print(abnormal_values)
            defaults = {
                'analysis_text': analysis_result,
                'diagnosis': diagnosis,
                'medications': medications,
                'treatments': treatments,
                'test_results': test_results,
                'abnormal_values': abnormal_values,
            }
            analysis, created = MedicalRecordAnalysis.objects.update_or_create(
                medical_record=medical_record,
                defaults=defaults
            )
            return analysis
        except Exception as e:
            import traceback
            print(f"Error saving analysis: {str(e)}")
            print(traceback.format_exc())
            return None