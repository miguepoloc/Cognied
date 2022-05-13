from rest_framework import serializers
from django.contrib.auth import authenticate, hashers
from .models import Usuarios
import hashlib
from api.serializers import *


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = Usuarios
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['email', 'document', 'password', 'token']

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        data = validated_data
        data['password'] = hashers.make_password(validated_data['password'])
        return Usuarios.objects.create(**data)


class LoginSerializer(serializers.Serializer):
    document = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        document = data.get('document', None)
        password = data.get('password', None)

        # Raise an exception if an
        # document is not provided.
        if document is None:
            raise serializers.ValidationError(
                'An document is required to log in.'
            )

        # Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        try:
            user = Usuarios.objects.filter(document=document).first()
        except Exception as err:
            raise serializers.ValidationError(str(err))

        if user:
            # print("encontro usuario")
            if user.is_active:
                # print("usuario activo")
                if not hashers.check_password(password, user.password):
                    # print("valido contraseña")
                    raise serializers.ValidationError('Contraseña Incorrecta')
            else:
                raise serializers.ValidationError('Usuario Inactivo')
        else:
            raise serializers.ValidationError('Usuario no existe')

        return {
            'token': user.token,
            'user': user
        }


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of Usuario objects."""

    # Passwords must be at least 8 characters, but no more than 128
    # characters. These values are the default provided by Django. We could
    # change them, but that would create extra work while introducing no real
    # benefit, so lets just stick with the defaults.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    sexo = SexoSerializer(many=False, read_only=True)
    estado_civil = Estado_CivilSerializer(many=False, read_only=True)
    escolaridad = EscolaridadSerializer(many=False, read_only=True)

    class Meta:
        model = Usuarios
        fields = '__all__'

        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        """Performs an update on a Usuario."""

        # Passwords should not be handled with `setattr`, unlike other fields.
        # Django provides a function that handles hashing and
        # salting passwords. That means
        # we need to remove the password field from the
        # `validated_data` dictionary before iterating over it.
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            # For the keys remaining in `validated_data`, we will set them on
            # the current `Usuario` instance one at a time.
            setattr(instance, key, value)

        if password is not None:
            # `.set_password()`  handles all
            # of the security stuff that we shouldn't be concerned with.
            instance.password = hashers.make_password(password)

        # After everything has been updated we must explicitly save
        # the model. It's worth pointing out that `.set_password()` does not
        # save the model.
        instance.save()

        return instance
