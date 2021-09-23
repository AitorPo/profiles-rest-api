from rest_framework import serializers

from profiles_api import models

# A serializer determines which fields are gonna be accepted in the request we make to the API
# and provides them in the browser API view
class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer a user profile object"""

    class Meta:
        model = models.UserProfile
        # List of fields that we want to work with
        fields = ('id', 'email', 'name', 'password')
        # extra keyword args
        extra_kwargs = {
            'password': {
                # You only can use the password field for create or update objects. NEVER for retrieve them
                'write_only': True,
                # Define the style of the input field
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        # We override the create function by accessing the method 'create_user(args)'
        # defined in 'objects' that is an object
        # which references UserProfileManager class into UserProfile class.
        user = models.UserProfile.objects.create_user(
            email = validated_data['email'],
            name = validated_data['name'],
            password = validated_data['password']
        )

        return user

    def update(self, instance, validated_data):
        """Handle updating user account

        The default update logic for the Django REST Framework (DRF) ModelSerializer
        code will take whatever fields are provided (in our case: email, name, password)
        and pass them directly to the model. This is fine for the email and name fields,
        however the password field requires some additional logic to hash the
        password before saving the update.Therefore, we override the Django REST Framework's
        update() method to add this logic to check for the presence password in the validated_data
        which is passed from DRF when updating an object.If the field exists, we will "pop"
        (which means assign the value and remove from the dictionary) the password
        from the validated data and set it using set_password() (which saves the password as a hash).
        Once that's done, we use super().update() to pass the values to the existing DRF
        update() method, to handle updating the remaining fields.
        """
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)
