import utizen
from mock import mock_open, patch

config_name = "refapp"
filename = "configs/projects/refapp.json"
app = {
    "app_name": "aa",
    "app_path": "aa/aa",
    "tizen": {}
}
app_str = '{"app_name": "aa", "app_path": "aa/aa"}'

# def test_mock_get_config(mocker):
#     mocker.patch('utizen.src.utils.get_config', return_value=(app, filename))
#
#     res = utizen.src.utils.get_config(config_name)
#     assert res == (app, filename)

def test_mock_open(mocker):
    m = mock_open(read_data=app_str)
    with patch('utizen.src.utils.open', m):
        res = utizen.src.utils.get_config(config_name)

    m.assert_called_once()
    assert res[0] == app

    relative_filename = "/".join(res[1].split("/")[-3:])
    assert relative_filename == filename

