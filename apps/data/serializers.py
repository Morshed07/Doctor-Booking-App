from rest_framework import serializers
from .models import IntakeData


class IntakeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntakeData
        fields = '__all__'
        extra_kwargs = {
            'appointment': {'read_only': True},
        }

    def validate(self, data):
        # 1. Existing consent checks
        if not data.get('agreed_to_telehealth'):
            raise serializers.ValidationError("You must agree to all consents.")

        # 2. Check the conditional peptide logic
        used_peptides = data.get('used_peptides_before')
        peptide_details = data.get('previous_peptides_details')

        if used_peptides and not peptide_details:
            # If they checked 'Yes' but left the text box empty
            raise serializers.ValidationError({
                "previous_peptides_details": "Please specify which peptides you have used before."
            })
        
        # 3. Clean up: If they checked 'No', ensure the text field is wiped 
        # (in case they typed something, then changed their mind and clicked 'No')
        if not used_peptides:
            data['previous_peptides_details'] = ""

        return data