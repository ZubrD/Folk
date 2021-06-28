from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from forseti.models import Deputy, Rules


class DeputySerializer(ModelSerializer):
    # party_fraction = serializers.SlugRelatedField(slug_field='name',    # для связанных полей, чтобы отображались
    #                                               read_only=True)  # названия, а не id

    class Meta:
        model = Deputy
        fields = ['name', 'party_fraction', 'region', 'mandat_basis', 'electoral_district']


class DeputyInstantSearchSerializer(ModelSerializer):

    class Meta:
        model = Deputy
        fields = ['name']


class RuleSerializer(ModelSerializer):

    class Meta:
        model = Rules
        fields = ['rule_number', 'title']