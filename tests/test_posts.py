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
        assert response_post.owner_id == db_post.owner_id
        assert response_post.owner.email == "sandman@gmail.com"


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
