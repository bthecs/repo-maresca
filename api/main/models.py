import base64

import bson, requests
from werkzeug.local import LocalProxy
from werkzeug.security import check_password_hash, generate_password_hash
from flask_pymongo import PyMongo
from flask import current_app, g


def get_db():
    """
    Configuration method to return db instance
    """
    database = getattr(g, "_database", None)

    if database is None:
        try:
            database = g._database = PyMongo(current_app).db
        except Exception as e:
            print(f"Error al conectar con la base de datos: {str(e)}")
            database = None
    return database


# LocalProxy para leer la instancia global db con solo `db`
db = LocalProxy(get_db)


class User:
    """User model"""

    def __init__(self):
        return

    def create(self, name: str = "", cuil: str = "", password: str = "", matricle: str = "",
               is_professional: bool = False):
        """Create a user"""
        user = self.get_by_cuil(cuil)
        if user:
            return
        new_user = db.users.insert_one({
            "name": name,
            "cuil": cuil,
            "password": self.encrypt_password(password),
            "matricle": matricle,
            "is_professional": is_professional,
        })
        return self.get_by_id(new_user.inserted_id)

    def get_by_id(self, user_id):
        """Get a user by id"""
        user = db.users.find_one({"_id": bson.ObjectId(user_id)})
        if not user:
            return
        user["_id"] = str(user["_id"])
        user.pop("password")
        return user

    def get_by_cuil(self, cuil):
        """Get a user by cuil"""
        user = db.users.find_one({"cuil": cuil})
        if not user:
            return
        user["_id"] = str(user["_id"])
        return user

    def encrypt_password(self, password):
        """Encrypt password"""
        return generate_password_hash(password)

    def login(self, cuil, password):
        """Login a user"""
        user = self.get_by_cuil(cuil)
        if not user or not check_password_hash(user["password"], password):
            return
        user.pop("password")
        return user


class Contract:
    """Contract model"""

    def __init__(self):
        return

    def create(self, cuil: str = "", contract: object = None):
        """Create a contract"""
        if contract is None:
            contract = {}

        existing_contract = self.get_by_cuil(cuil)
        if existing_contract:
            return

        contract.seek(0)
        contract_content = contract.read()

        # Codificar el contenido como base64
        encoded_content = base64.b64encode(contract_content).decode('utf-8')

        new_contract = db.contracts.insert_one({
            "cuil": cuil,
            "contract": encoded_content,
        })

        return self.get_by_id(new_contract.inserted_id)

    def get_by_id(self, contract_id):
        """Get a contract by id"""
        contract = db.contracts.find_one({"_id": bson.ObjectId(contract_id)})
        if not contract:
            return
        contract["_id"] = str(contract["_id"])
        return contract

    def get_by_cuil(self, cuil):
        """Get a contract by cuil"""
        contract = db.contracts.find_one({"cuil": cuil})
        if not contract:
            return
        contract["_id"] = str(contract["_id"])
        return contract

    def get_by_contract(self, contract):
        """Get a contract by contract"""
        contract = db.contracts.find_one({"contract": contract})
        if not contract:
            return
        contract["_id"] = str(contract["_id"])
        return contract

    def update(self, cuil, new_contract):
        """Update a contract"""

        existing_contract = self.get_by_cuil(cuil)
        if not existing_contract:
            return

        new_contract.seek(0)
        contract_content = new_contract.read()

        # Codificar el contenido como base64
        encoded_content = base64.b64encode(contract_content).decode('utf-8')

        # Actualizar y devolver el contrato actualizado
        db.contracts.update_one({"cuil": cuil}, {"$set": {"contract": encoded_content}})
        return self.get_by_cuil(cuil)

    def delete(self, contract_id):
        """Delete a contract"""
        contract = self.get_by_id(contract_id)
        if not contract:
            return
        db.contracts.delete_one({"_id": bson.ObjectId(contract_id)})
        return contract
