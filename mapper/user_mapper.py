


from models.user_models import UserModel
from models.db.user_entity import UserEntity




def map_entity_to_model(entity: UserEntity) -> UserModel:
    return UserModel(
     username=entity.username,
     password=entity.password,
     email_address=entity.email_address,
     phone_number=entity.phone_number,
     is_activate=entity.is_active,
     id=entity.id
    )


def map_model_to_entity(model: UserModel) -> UserEntity:
    return UserEntity(
        id=model.id,
        username=model.username,
        password=model.password,
        email_address=model.email_address,
        phone_number=model.phone_number,
        is_active=model.is_activate
        )
