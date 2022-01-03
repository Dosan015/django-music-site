from rest_framework import serializers

from home.models  import Audio, Singer


class SingerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Singer
        fields = '__all__'

class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = ['id', 'file']


class AudioPrivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['singer'] = SingerSerializer(read_only=True)
        return super(AudioPrivateSerializer, self).to_representation(instance)

