import pathlib
from django.core.files import File as _File
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from courses.models import Course, Subject, Module, Content, ItemBase, Text, File, Image, Video, Test, VideoURL


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug']

    def create(self, validated_data):

        subject = Subject(
            title=validated_data['title'],
            slug=validated_data['slug']
        )
        subject.save()
        return subject


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'owner', 'subject', 'title', 'slug', 'overview')
        required = ('title', 'slug', 'overview')
        extra_kwargs = {'owner': {'read_only': True}}

    def validate(self, attrs):
        credentials = {
            'subject': attrs.get('subject'),
            'title': attrs.get('title'),
            'slug': attrs.get('slug'),
            'overview': attrs.get('overview')
        }

        if all(credentials.values()):
            return credentials
        else:
            msg = "Must include all fields"
            raise serializers.ValidationError(msg)

    def create(self, validated_data):
        validated_data.data['subject'] = Subject.objects.get(id=validated_data.data['subject'])
        course = Course(
            owner=validated_data.user,
            subject=validated_data.data['subject'],
            title=validated_data.data['title'],
            slug=validated_data.data['slug'],
            overview=validated_data.data['overview']
        )
        course.save()
        return course


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('id', 'course', 'title', 'description', "order")
        required = ('course', 'title', 'description')
        extra_kwargs = {'course': {'read_only': True}, 'order': {'read_only': True}}

    def validate(self, attrs):
        credentials = {
            'title': attrs.get('title'),
            'description': attrs.get('description'),
        }

        if all(credentials.values()):
            return credentials
        else:
            msg = "Must include all fields"
            raise serializers.ValidationError(msg)

    def create(self, validated_data, course_id):
        course = Course.objects.get(id=course_id)
        module = Module(
            course=course,
            title=validated_data.data['title'],
            description=validated_data.data['description'],
        )
        module.save()
        return module


# class ItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ItemBase
#         fields = ('owner','title', 'created','updated' )
#         extra_kwargs = {'owner': {'read_only': True},'created': {'read_only': True},'updated': {'read_only': True},}


class ItemRelatedField(serializers.RelatedField):

    def to_representation(self, value):
        return value.render()


class ContentTypeSerializer(serializers.RelatedField):
    class Meta:
        model = ContentType

    def to_representation(self, value):
        return value.model


class ContentSerializer(serializers.ModelSerializer):
    item = ItemRelatedField(read_only=True)
    content_type = ContentTypeSerializer(read_only=True)

    # title=serializers.CharField(max_length=255)
    class Meta:
        model = Content
        fields = ['id','order', 'item', 'content_type']






class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemBase
        fields = ["owner", "title"]

    def validate(self, attrs):
        credentials = {
            'owner': attrs.get('owner'),
            'title': attrs.get('title'),
        }

        if all(credentials.values()):
            return credentials
        else:
            msg = "Must include all fields"
            raise serializers.ValidationError(msg)


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ["title", "content"]

    def create(self, validated_data, request):
        validated_data["owner"] = request.user
        text = Text.objects.create(**validated_data)
        text.save()
        return text

    def validate(self, attrs):
        credentials = {
            'content': attrs.get('content'),
            'title': attrs.get('title'),
        }

        if all(credentials.values()):
            return credentials
        else:
            msg = "Must include all fields"
            raise serializers.ValidationError(msg)


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ["title"]

    def create(self, validated_data, request):
        validated_data["owner"] = request.user
        print(request.data['file'])
        validated_data["file"] = request.data['file']
        file = File.objects.create(**validated_data)
        file.save()
        return file

    def validate(self, attrs):
        credentials = {
            'title': attrs.get('title'),
        }

        if all(credentials.values()):
            return credentials
        else:
            msg = "Must include all fields"
            raise serializers.ValidationError(msg)


class ImageSerializer(ItemSerializer):
    class Meta:
        model = Image
        fields = ['title']



    def create(self, validated_data, request):
        validated_data['owner'] = request.user
        validated_data['image'] = request.data['image']
        image=Image(**validated_data)
        # video = Video.objects.create(**validated_data)

        image.save()
        return image

    def validate(self, attrs):
        credentials = {
            'title': attrs.get('title'),
        }

        if all(credentials.values()):
            return credentials
        else:
            msg = "Must include all fields"
            raise serializers.ValidationError(msg)


class TestSerializer(ItemSerializer):
    class Meta:
        model = Test
        fields=['title','answer']

    def create(self, validated_data, request):
        print(validated_data)
        validated_data['owner'] = request.user
        test = Test.objects.create(**validated_data)

        test.save()
        return test

    def validate(self, attrs):
        print(attrs)
        credentials = {
            'title': attrs.get('title'),
            'answer': attrs.get('answer'),
        }

        if all(credentials.values()):
            return credentials
        else:
            msg = "Must include all fields"
            raise serializers.ValidationError(msg)

class VideoSerializer(ItemSerializer):
    class Meta:
        model = Video
        fields = ['title']



    def create(self, validated_data, request):
        validated_data['owner'] = request.user
        validated_data['video'] = request.data['video']
        video=Video(**validated_data)
        # video = Video.objects.create(**validated_data)

        video.save()
        return video

    def validate(self, attrs):
        credentials = {
            'title': attrs.get('title'),
        }

        if all(credentials.values()):
            return credentials
        else:
            msg = "Must include all fields"
            raise serializers.ValidationError(msg)



class VideoSerializerUrl(ItemSerializer):
    class Meta:
        model = VideoURL
        fields = ['title','url']



    def create(self, validated_data, request):
        validated_data['owner'] = request.user
        print(validated_data)
        video=VideoURL(**validated_data)
        # video = Video.objects.create(**validated_data)

        video.save()
        return video

    def validate(self, attrs):
        credentials = {
            'title': attrs.get('title'),
            'url':attrs.get('url')
        }

        if all(credentials.values()):
            return credentials
        else:
            msg = "Must include all fields"
            raise serializers.ValidationError(msg)

# class TextSerializer(ItemSerializer):
#     class Meta:
#         model:Text
#         fields = ('content')
#
#     def validate(self, attrs):
#         credentials = {
#             'content': attrs.get('content'),
#             'title':attrs.get('title'),
#         }
#
#         if all(credentials.values()):
#             return credentials
#         else:
#             msg = "Must include all fields"
#             raise serializers.ValidationError(msg)
#
# class VideoItem(ItemSerializer):
#     class Meta:
#         model:Text
#         fields = ('content')
#
#     def validate(self, attrs,file):
#         credentials = {
#             'content': attrs.get('content'),
#             'file':attrs.get('file'),
#         }
#
#         if all(credentials.values()):
#             return credentials
#         else:
#             msg = "Must include all fields"
#             raise serializers.ValidationError(msg)
#
# class ItemRelatedField(serializers.RelatedField):
#     def to_representation(self, value):
#         return value.render()
#
#
# class ContentSerializer(serializers.ModelSerializer):
#     item = ItemRelatedField(read_only=True)
#
#     class Meta:
#         model = Content
#         fields = ['order', 'item']
#
#
class ModuleWithContentsSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)

    class Meta:
        model = Module
        fields = ['order', 'title', 'description', 'contents']

class CourseWithModuleSerializer(serializers.ModelSerializer):
    modules=ModuleSerializer

    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug',
                  'overview', 'created', 'owner', 'modules']


#
#
class CourseWithContentsSerializer(serializers.ModelSerializer):
    modules = ModuleWithContentsSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug',
                  'overview', 'created', 'owner', 'modules']
