import pytest
from students.models import Course, Student
from rest_framework.test import APIClient

@pytest.fixture()
def create_courses():
    def factory_courses(*args, **kwargs):
        from model_bakery import baker
        baker.make(Course, *args, **kwargs)
    return factory_courses

@pytest.fixture()
def client():
    return APIClient()

@pytest.mark.django_db
def test_get_lsit_course(client, create_courses):
    count = 10
    courses = create_courses(_quantity=count)
    response = client.get("/api/v1/courses/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == count

@pytest.mark.django_db
def test_get_one_course(client, create_courses):
    count = 1
    courses = create_courses(_quantity=count)
    response = client.get("/api/v1/courses/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == count



@pytest.mark.django_db
def test_create_one_course(client):
    count = len(Course.objects.all())
    data = {
        "name": "Python",
    }
    response = client.post("/api/v1/courses/", data, format="json")
    assert response.status_code == 201
    assert count == len(Course.objects.all()) - 1


@pytest.mark.django_db
def test_get_one_course_on_id(client, create_courses):
    count = 10
    courses = create_courses(_quantity=count)
    name_course = "TEST"
    course = Course(name=name_course).save()
    course_id = Course.objects.filter(name=name_course).first().id
    URL = "/api/v1/courses/?id={id}".format(id=course_id)
    response = client.get(URL)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['id'] == course_id

@pytest.mark.django_db
def test_get_one_course_on_name(client, create_courses):
    count = 10
    courses = create_courses(_quantity=count)
    name_course = "TEST"
    course = Course(name=name_course).save()
    URL = "/api/v1/courses/?name={name}".format(name=name_course)
    response = client.get(URL)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['name'] == name_course

@pytest.mark.django_db
def test_delete_course(client, create_courses):
    count = 10
    courses = create_courses(_quantity=count)
    name_course = "TEST"
    course = Course(name=name_course).save()
    course_id = Course.objects.filter(name=name_course).first().id
    URL = "/api/v1/courses/{}/".format(course_id)
    response = client.delete(URL)
    assert response.status_code == 204


@pytest.mark.django_db
def test_update_course(client, create_courses):
    count = 10
    courses = create_courses(_quantity=count)
    name_course = "TEST"
    course = Course(name=name_course).save()
    course_id = Course.objects.filter(name=name_course).first().id
    URL = "/api/v1/courses/{}/".format(course_id)
    data_params = {
        "name": "TEST_UPDATE"
    }
    response = client.put(URL, data_params, format="json")
    assert response.status_code == 200
    data = response.json()
    assert data_params["name"] == data["name"]
