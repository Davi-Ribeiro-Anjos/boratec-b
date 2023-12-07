from rest_framework import serializers

from branches.serializers import BranchesSimpleSerializer
from employees.serializers import EmployeesSimpleSerializer
from roles.serializers import RolesSimpleSerializer

from .models import Vacancies


class VacanciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancies
        fields = (
            "id",
            "replacement",
            "salary_range",
            "title",
            "description",
            "observation",
            "work_schedule",
            "release_status",
            "date_expected_start",
            "date_requested",
            "date_vetta",
            "date_exam",
            "date_closed",
            "date_limit",
            "priority",
            "quantity",
            "status",
            "contract_mode",
            "department",
            "type_vacancy",
            "company",
            "motive",
            "selected",
            "initiative",
            "approval_manager",
            "comment_manager",
            "approval_regional_manager",
            "comment_regional_manager",
            "approval_rh",
            "comment_rh",
            "approval_director",
            "comment_director",
            "email_manager",
            "email_send_manager",
            "email_regional_manager",
            "email_send_regional_manager",
            "email_rh",
            "email_send_rh",
            "email_director",
            "email_send_director",
            "author",
            "recruiter",
            "role",
            "branch",
        )


class VacanciesResponseSerializer(serializers.ModelSerializer):
    author = EmployeesSimpleSerializer()
    branch = BranchesSimpleSerializer()
    role = RolesSimpleSerializer()
    date_expected_start = serializers.DateField(format="%d/%m/%Y")
    date_requested = serializers.DateField(format="%d/%m/%Y")
    date_vetta = serializers.DateField(format="%d/%m/%Y")
    date_exam = serializers.DateField(format="%d/%m/%Y")
    date_closed = serializers.DateField(format="%d/%m/%Y")
    date_limit = serializers.DateField(format="%d/%m/%Y")

    class Meta:
        model = Vacancies
        fields = (
            "id",
            "replacement",
            "salary_range",
            "title",
            "description",
            "observation",
            "work_schedule",
            "release_status",
            "date_expected_start",
            "date_requested",
            "date_vetta",
            "date_exam",
            "date_closed",
            "date_limit",
            "priority",
            "quantity",
            "status",
            "contract_mode",
            "department",
            "type_vacancy",
            "company",
            "motive",
            "selected",
            "initiative",
            "approval_manager",
            "comment_manager",
            "approval_regional_manager",
            "comment_regional_manager",
            "approval_rh",
            "comment_rh",
            "approval_director",
            "comment_director",
            "email_manager",
            "email_send_manager",
            "email_regional_manager",
            "email_send_regional_manager",
            "email_rh",
            "email_send_rh",
            "email_director",
            "email_send_director",
            "author",
            "recruiter",
            "role",
            "branch",
        )


class VacanciesEmailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancies
        fields = (
            "email_manager",
            "email_regional_manager",
            "email_rh",
            "email_director",
        )
