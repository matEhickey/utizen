import utizen

def test_cli_install_tizen(mocker):
    config_name = "refapp"
    ip = '1.2.3.4'
    port = '1111'

    mocker.patch(
        'utizen.src.cli.get_connected_tv_ip_port',
        return_value=(ip, port)
    )
    mocker.patch('utizen.src.tizen_packager.run')

    utizen.src.cli._install(config_name, True)

    utizen.src.cli.get_connected_tv_ip_port.assert_called_once_with()
    utizen.src.tizen_packager.run.assert_called_once_with(config_name, ip, port)


def test_cli_install_lg(mocker):
    config_name = "refapp"
    mocker.patch('utizen.src.lg_packager.run')

    utizen.src.cli._install(config_name, False)

    utizen.src.lg_packager.run.assert_called_once_with(config_name)