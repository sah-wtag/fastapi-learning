import json
import pytest
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    posts = [schemas.PostResponse(**post) for post in res.json()]

    assert res.status_code == 200
    assert len(res.json()) == len(test_posts)

    for response_post, db_post in zip(posts, test_posts):
        assert response_post.id == db_post.id
        assert response_post.title == db_post.title
        assert response_post.content == db_post.content
        assert response_post.published == db_post.published


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/111111")
    assert res.status_code == 404


def test_get_one_post_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostResponse(**res.json())

    assert res.status_code == 200
    assert post.id == test_posts[0].id
    assert post.title == test_posts[0].title
    assert post.content == test_posts[0].content
    assert post.published == test_posts[0].published
    assert post.owner_id == test_posts[0].owner_id
    assert post.owner.email == "sandman@gmail.com"


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("Awesome new title", "New content", True),
        ("Awesome new title 2nd", "New content 2nd", False),
        ("Awesome new title 3rd", "New content 3rd", True),
    ],
)
def test_create_post(
    authorized_client, test_user, test_posts, title, content, published
):
    res = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published}
    )
    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]


def test_create_post_for_default_published(authorized_client, test_user, test_posts):

    res = authorized_client.post(
        "/posts/", json={"title": "new post", "content": "new content"}
    )
    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == "new post"
    assert created_post.content == "new content"
    assert created_post.published is True
    assert created_post.owner_id == test_user["id"]


def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post("/posts/", json={"title": "new post", "content": "new content"})

    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401


def test_delete_post_successfully(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 204


def test_delete_non_exist_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete("/posts/2222")

    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[2].id}")

    assert res.status_code == 403
