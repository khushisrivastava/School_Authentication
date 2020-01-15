import jwt
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, school_name, school_code, principal, teacher_count, affiliated_board, address, sub_district, district,  phone, email, password):
        if not school_code:
            raise ValueError("Provide a School Code!")
        if not school_name:
            raise ValueError("Provide a School Name!")
        if not principal:
            raise ValueError("Provide a Principal's Name !")
        if not teacher_count:
            raise ValueError("Provide a Number of Teachers!")
        if not address:
            raise ValueError("Provide a Address!")
        if not affiliated_board:
            raise ValueError("Provide a Board School is Affiliated to!")
        if not sub_district:
            raise ValueError("Provide a Sub District!")
        if not district:
            raise ValueError("Provide a District!")
        if not phone:
            raise ValueError("Provide a Phone Number!")
        if not email:
            raise ValueError("Provide an Email!")
        if not password:
            raise ValueError("Enter Password!")
        user = self.model(
            school_code = school_code,
            school_name = school_name,
            principal = principal,
            teacher_count = teacher_count,
            affiliated_board = affiliated_board,
            address = address,
            sub_district = sub_district,
            district = district,
            phone = phone,
            email = self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, school_name, school_code, principal, teacher_count, affiliated_board, address, sub_district, district,  phone, email, password):
        if password is None:
            raise ValueError("Superuser must have a Password!")
        user = self.create_user(school_name, school_code, principal, teacher_count, affiliated_board, address, sub_district, district,  phone, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user