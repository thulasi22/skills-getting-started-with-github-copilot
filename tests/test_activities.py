def test_get_activities(client):
    resp = client.get('/activities')
    assert resp.status_code == 200
    data = resp.json()
    # Expect some known activities present
    assert 'Chess Club' in data
    assert isinstance(data['Chess Club']['participants'], list)


def test_signup_and_duplicate(client):
    email = 'test.student@mergington.edu'
    activity = 'Chess Club'

    # Ensure signup succeeds
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert 'Signed up' in resp.json().get('message', '')

    # Signing up again should return 400
    resp2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp2.status_code == 400


def test_unregister_success_and_errors(client):
    # Use an existing participant from the initial fixtures
    activity = 'Programming Class'
    email = 'emma@mergington.edu'

    # Unregister should succeed
    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp.status_code == 200
    assert 'Unregistered' in resp.json().get('message', '')

    # Unregistering again should return 400
    resp2 = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp2.status_code == 400

    # Unregister from nonexistent activity
    resp3 = client.delete(f"/activities/NoSuch/activity/participants?email={email}")
    # path will be treated literally; expect 404
    assert resp3.status_code in (404,)
